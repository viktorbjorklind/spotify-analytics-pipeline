# Spotify Analytics Pipeline

An end-to-end data engineering portfolio project that ingests personal Spotify listening history into a cloud database using a fully automated daily pipeline, transforms it with dbt, and visualises it in Power BI.

## Architecture

```
Spotify API → Python (ingestion) → Neon (PostgreSQL) → dbt (transforms) → Power BI
```

## Stack

| Layer | Tool |
|-------|------|
| Ingestion | Python + Spotipy |
| Orchestration | GitHub Actions (daily cron) |
| Database | Neon (hosted PostgreSQL) |
| Transformation | dbt |
| Visualisation | Power BI |

## Features

- Pulls the 50 most recently played Spotify tracks daily via the Spotify Web API
- Deduplicates records using `played_at` as primary key — no duplicate entries on reruns
- Fully cloud-based — no local dependencies, runs without any machine being on
- Credentials stored securely as GitHub Secrets
- dbt staging model cleans and enriches raw data with derived fields
- dbt mart models aggregate data for Power BI consumption
- Power BI dashboard with drill-down from artist → album → track, and daily listening trends with date filtering

## Project Structure

```
spotify-analytics-pipeline/
├── ingestion/
│   └── fetch.py                        # Spotify API ingestion script
├── transform/
│   └── models/
│       ├── staging/
│       │   ├── stg_played_tracks.sql   # Cleans and enriches raw data
│       │   └── sources.yml
│       └── marts/
│           ├── mart_top_artists.sql
│           ├── mart_listening_by_hour.sql
│           ├── mart_listening_by_day.sql
│           └── mart_listening_by_date_hour.sql
├── .github/
│   └── workflows/
│       └── daily_ingest.yml            # GitHub Actions workflow
├── .env.example
├── requirements.txt
└── README.md
```

## Pipeline Flow

1. GitHub Actions triggers the ingestion script every morning at 7am UTC
2. Python authenticates with Spotify using a refresh token — no browser needed
3. Recently played tracks are fetched and loaded into Neon PostgreSQL
4. dbt transforms raw data into clean staging and mart models
5. Power BI connects to Neon and visualises listening trends

## Setup

### Environment Variables

Create a `.env` file:

```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
SPOTIFY_REFRESH_TOKEN=your_refresh_token
DATABASE_URL=your_neon_connection_string
```

### Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python ingestion/fetch.py
```

### dbt

```bash
cd transform
dbt run
```

### GitHub Actions

Add the environment variables above as repository secrets under **Settings → Secrets and variables → Actions**.

The pipeline runs automatically every day at 7am UTC. You can also trigger it manually from the **Actions** tab.
