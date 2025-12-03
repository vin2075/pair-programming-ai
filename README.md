Pair Programming AI – Real-Time Collaborative Coding Platform
Overview

Pair Programming AI is a simplified real-time collaborative coding web application. The platform allows two users to join the same room, edit code simultaneously, and see each other’s changes instantly. The system also provides a mocked AI-style autocomplete suggestion for code assistance.

This project demonstrates a full-stack implementation using FastAPI for the backend and React + TypeScript for the frontend, with real-time updates handled via WebSockets.

Features
1. Room Creation & Joining

Users can create a new coding room, which generates a unique room ID.

Users can join an existing room by navigating to a URL containing the room ID.

No authentication is required, making it easy to start coding instantly.

2. Real-Time Collaborative Coding

Real-time code updates between users in the same room.

Each keystroke from one user is instantly reflected in the other user's editor.

In-memory storage maintains the current state of each room’s code.

3. AI Autocomplete (Mocked)

Provides a POST /autocomplete endpoint that accepts the current code, cursor position, and programming language.

Returns a mocked suggestion for the user’s code.

Frontend triggers this endpoint when the user pauses typing for ~600ms, displaying suggestions in the editor.

Backend

The backend is built using Python and FastAPI, with WebSockets for real-time updates and PostgreSQL for persistent storage.

Key Endpoints:

POST /rooms – Create a new room and return its room ID.

POST /autocomplete – Return a mocked autocomplete suggestion for the code.

WebSocket /ws/{room_id} – Handle real-time code updates between users in the same room.

Design Choices

Room state is maintained in-memory for low latency and instant synchronization.

Database is used to persist code for each room for recovery and long-term storage.

Simple last-write-wins strategy for code synchronization ensures simplicity while maintaining collaboration.

Frontend

The frontend is built using React, TypeScript, and optionally Redux Toolkit for state management.

Users interact with a code editor to type and see live updates from collaborators.

Autocomplete suggestions are displayed in-line, enhancing the coding experience.

Minimal design to focus on core collaboration functionality.

How to Run
Backend

Install dependencies with pip install -r requirements.txt.

Configure environment variables for database connection and allowed frontend origins.

Start the FastAPI server with:

uvicorn app.main:app --host 0.0.0.0 --port <PORT>

Frontend

Install dependencies with npm install or yarn.

Configure environment variables for API and WebSocket URLs.

Start the React development server:

npm start

Future Improvements

Implement proper conflict resolution for simultaneous edits using operational transforms or CRDTs.

Enhance AI autocomplete with a real AI model instead of static suggestions.

Add multi-language support and syntax highlighting improvements.

Implement user authentication and persistent user sessions for better collaboration tracking.

Limitations

The autocomplete is mocked and not AI-powered.

Current synchronization strategy is simple; rapid simultaneous edits may overwrite changes.

Designed for two users per room; scaling to many users requires additional optimisations.

Demo

You can access the deployed frontend demo here:   https://pair-programming-ai-or7d.vercel.app/

Pair Programming AI Demo

This README focuses on general project details, design decisions, and deployment instructions without exposing local URLs or project-specific secrets.
