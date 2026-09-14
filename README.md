# VideoLang (Usearch)

> Semantic AI search engine for YouTube video transcripts. Find exact moments and answers across entire channels in seconds.

---

## Overview

**VideoLang** (also known as **Usearch**) is a full-stack platform that enables natural language semantic search inside YouTube video transcripts. Instead of relying solely on keyword matches, it extracts video subtitles, computes vector embeddings via OpenAI, and leverages vector search in MongoDB to return ranked results with exact, clickable timestamps.

---

## Key Features

- **Semantic Search**: Ask questions in natural language and find precise video segments where the topic is discussed.
- **Timestamp Navigation**: Direct, clickable links jump right to the exact second in the video.
- **Channel & Video Indexing**: Index complete YouTube channels or individual videos on demand via YouTube Data API and `youtube-transcript-api`.
- **Hybrid Storage & Vector Search**:
  - **MongoDB**: Video metadata, transcript chunks, vector embeddings, and API usage tracking.
  - **Firebase & Firestore**: Authentication, user accounts, and tier-based quota management.
- **API Key & Rate Limiting**: Secure API key authentication with per-tier request tracking and limits.
- **Modern Web Interface**: Responsive, dark-themed UI built with Next.js and Tailwind CSS.

---

## Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | [Next.js](https://nextjs.org/) (React 19, TypeScript), Tailwind CSS, Radix UI, Lucide Icons |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+), Uvicorn, Pydantic |
| **AI / Embeddings** | [OpenAI API](https://platform.openai.com/) (`text-embedding-3-small` / text embeddings) |
| **Databases** | MongoDB (Vector Search & Cache), Firebase Firestore |
| **Auth & Billing** | Firebase Authentication, Firebase Admin SDK |
| **External APIs** | YouTube Data API v3, `youtube-transcript-api` |
| **DevOps** | Docker Compose |

---

## Project Structure

```text
videolang/
├── backend/              # FastAPI Python backend
│   ├── database/         # MongoDB and Firestore database connectors
│   ├── dependencies/     # Auth and security dependencies
│   ├── models/           # Pydantic data schemas
│   ├── routers/          # API endpoints (/youtube, /auth)
│   ├── services/         # Indexing, embedding, search, transcript logic
│   ├── app.py            # Application entrypoint
│   └── requirements.txt  # Python package dependencies
├── frontend/             # Next.js web application
│   ├── src/
│   │   ├── app/          # App router pages (search, pricing, profile, docs)
│   │   ├── components/   # UI components
│   │   └── viewmodels/   # State & client-side logic
│   └── package.json      # Frontend dependencies
├── docker-compose.yml    # Local services (MongoDB)
└── README.md
```

---

## Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** & **pnpm** (or npm)
- **Docker & Docker Compose** (for running MongoDB locally)
- API keys: **OpenAI API Key**, **YouTube Data API Key**, and a **Firebase project**

---

### 1. Database (Docker)

Start the local MongoDB instance:

```bash
docker compose up -d
```

---

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables in backend/.env
# Required: OPENAI_API_KEY, YOUTUBE_API_KEY, MONGO_URI, FIREBASE_CREDENTIALS

# Start the API server
uvicorn app:app --reload --port 8000
```

Backend will be available at `http://localhost:8000` (interactive docs at `http://localhost:8000/docs`).

---

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install

# Configure environment variables in frontend/.env.local
# (Firebase client config, backend API URL)

# Start development server
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## License

This project is developed for educational and research purposes.