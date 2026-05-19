# Spotify Analytics Pipeline

A end-to-end data engineering portfolio project that ingests personal Spotify listening history into a cloud database using a fully automated pipeline.

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
| Transformation | dbt (coming soon) |
| Visualisation | Power BI (coming soon) |

## Features

- Pulls the 50 most recently played Spotify tracks daily via the Spotify Web API
- Deduplicates records using `played_at` as primary key — no duplicate entries on reruns
- Fully cloud-based — no local dependencies, runs without any machine being on
- Credentials stored securely as GitHub Secrets

## Pipeline Flow

1. GitHub Actions triggers the ingestion script every morning at 7am UTC
2. Python script authenticates with Spotify using a refresh token
3. Recently played tracks are fetched and loaded into Neon PostgreSQL
4. dbt will transform raw data into analytics-ready models *(in progress)*
5. Power BI connects to Neon for dashboarding *(in progress)*

## Project Structure

```
spotify-analytics-pipeline/
├── ingestion/
│   └── fetch.py           # Spotify API ingestion script
├── .github/
│   └── workflows/
│       └── daily_ingest.yml  # GitHub Actions workflow
├── .env.example           # Environment variable template
├── requirements.txt
└── README.md
```

## Setup

### Prerequisites
- Python 3.11+
- A Spotify Developer account and app
- A Neon account

### Environment Variables

Create a `.env` file based on `.env.example`:

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

### GitHub Actions

Add the environment variables above as repository secrets under **Settings → Secrets and variables → Actions**.

The pipeline runs automatically every day at 7am UTC. You can also trigger it manually from the **Actions** tab.
