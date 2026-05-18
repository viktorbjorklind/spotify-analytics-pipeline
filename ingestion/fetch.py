import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import psycopg2
from dotenv import load_dotenv

load_dotenv()

auth_manager = SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-read-recently-played"
)

# Use refresh token directly — no browser needed
auth_manager.refresh_access_token(os.getenv("SPOTIFY_REFRESH_TOKEN"))

sp = spotipy.Spotify(auth_manager=auth_manager)

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS played_tracks (
        played_at TIMESTAMP PRIMARY KEY,
        track_id TEXT,
        track_name TEXT,
        artist_name TEXT,
        album_name TEXT,
        duration_ms INT
    )
""")
conn.commit()

results = sp.current_user_recently_played(limit=50)
tracks = results["items"]

for item in tracks:
    played_at = item["played_at"]
    track = item["track"]

    cur.execute("""
        INSERT INTO played_tracks (
            played_at, track_id, track_name, artist_name, album_name, duration_ms
        ) VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (played_at) DO NOTHING
    """, (
        played_at,
        track["id"],
        track["name"],
        track["artists"][0]["name"],
        track["album"]["name"],
        track["duration_ms"]
    ))

conn.commit()
cur.close()
conn.close()
print(f"Done — {len(tracks)} tracks processed")