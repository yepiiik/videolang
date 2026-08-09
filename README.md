# Ucontext

## Intelligent search on YouTube

This script is analysing(indexing) YouTube video which contain subtitles, save it to further usage

## Tech Stack

- Java
- NextJS
- MongoDB
- Docker
- Firebase
- Github actions

Software Requirements Specification (SRS)
Project: YouTube AI Research Platform ("Projekt SE")
1. Introduction
1.1 Purpose
The purpose of this document is to define the software requirements for "Projekt SE," an AI-powered research platform and browser extension. The system allows users to search for specific concepts within the video transcripts of selected YouTube channels.
1.2 Scope
The system comprises a web-based SaaS platform and a browser extension. It utilizes Natural Language Processing (OpenAI Text Embeddings) to search YouTube video transcripts. Key features include:
Intelligent, semantic search across specific YouTube channels.
Timestamped video results returned asynchronously.
A community forum (similar to Twitter/Threads) for sharing insights and search queries.
A browser extension for direct search on YouTube channel pages.
1.3 Technology Stack
Backend: Java (REST API)
Frontend: NextJS
Database: MongoDB (for caching and data storage)
Authentication/Monetization: Firebase
External APIs: YouTube Data API (channels, videos, captions), OpenAI Text Embedding API

2. Overall Description
2.1 Product Perspective
The system operates as a distributed web application. The Java backend acts as the orchestrator between the NextJS frontend/Browser Extension, the MongoDB database, and external APIs (YouTube and OpenAI).
2.2 User Classes and Characteristics
Guest User: Unauthenticated user. Can perform basic searches (subject to rate limits) and is served advertisements to cover infrastructure costs.
Registered User (Free): Authenticated via Firebase. Has access to the community forum to post and interact, subject to standard search limitations.
Premium User (Subscriber): Authenticated via Firebase with an active subscription. Has increased/unlimited search quotas and full browser extension capabilities.

3. Specific Requirements
3.1 Functional Requirements
3.1.1 Core Search Engine & Caching (Backend)
REQ-1.1: The system shall accept a YouTube channel identifier and a natural language query.
REQ-1.2: Upon receiving a request, the backend shall query the YouTube API for the channel's latest videos and fetch their generated captions (supporting all available YouTube caption languages).
REQ-1.3: The backend shall cache fetched video transcripts and metadata in MongoDB to minimize redundant YouTube API calls.
REQ-1.4: The system shall synchronize data by checking for and fetching new, uncached videos from the requested channel during each search request.
REQ-1.5: The system shall convert transcripts into vector embeddings using the OpenAI Text Embedding API for semantic search matching.
3.1.2 Search Results & UI (Frontend)
REQ-2.1: The frontend shall display the most relevant search results sorted by accuracy.
REQ-2.2: Search results must provide direct, clickable timecodes (timestamps) linking to the exact moment the answer is discussed in the video.
REQ-2.3: The system shall implement asynchronous data rendering (e.g., via Server-Sent Events or WebSockets). Processed video results must stream into the UI as they are ready, rather than waiting for the entire channel backlog to process.
REQ-2.4: If a user searches a previously queried channel, the UI shall display a contextual prompt connecting them to the community (e.g., "You are not the only one who is interested in [channel name]. Connect with these people!").
3.1.3 Browser Extension
REQ-3.1: The extension shall inject an intelligent search interface directly into the YouTube.com channel page layout.
REQ-3.2: The extension shall allow users to execute a semantic search against the currently viewed channel.
REQ-3.3: The extension shall return and display clickable timecodes directly within the YouTube interface.
3.1.4 Community Forum
REQ-4.1: The system shall provide a threaded discussion forum where users can create and react to posts.
REQ-4.2: Users shall be able to attach specific YouTube videos, channels, timestamps, and their original search query directly into a post.
REQ-4.3: The system shall implement automated content moderation. Post content must be analyzed using OpenAI embeddings to detect and flag/block harassment or inappropriate behavior before publication.
3.1.5 Monetization & Access Control
REQ-5.1: The system shall track the number of searches performed by an IP address or Session ID for Guest Users.
REQ-5.2: The system shall inject ad-placements into the NextJS UI for Guest Users to offset API costs.
REQ-5.3: Firebase shall handle subscription state, granting Premium Users extended search limits and ad-free access.
3.2 Non-Functional Requirements
3.2.1 Performance Requirements
PERF-1: The system must return the first batch of search results to the user within 5 seconds of the query execution.
PERF-2: Processing of historical channel data must not block the UI; asynchronous streaming must ensure immediate visual feedback for the user.
3.2.2 Scalability & API Management
SCAL-1: The backend must efficiently manage YouTube API quotas, prioritizing MongoDB cache lookups before executing live fetch requests to prevent API rate limiting.
3.2.3 Security Requirements
SEC-1: All authentication and session management must be securely handled via Firebase Auth.
SEC-2: Forum input must be sanitized to prevent XSS attacks, in addition to the AI-driven harassment moderation.