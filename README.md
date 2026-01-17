# ChatBot Platform 🤖

A production-ready, full-stack AI chatbot platform with user authentication, project management, and intelligent conversation memory. Built with FastAPI backend and React frontend.

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.13-green)
![React](https://img.shields.io/badge/react-19.2-61dafb)

---

## ✨ Features

### 🔐 Authentication System
- **User Registration & Login** — Secure authentication powered by Supabase Auth
- **JWT Token Validation** — ES256 algorithm with JWKS public key verification
- **Protected Routes** — Frontend route guards for authenticated access

### 📁 Project Management
- **Create Projects** — Define chatbot projects with custom names and descriptions
- **System Prompts** — Set custom AI behavior per project
- **CRUD Operations** — Full create, read, update, and delete functionality
- **User Isolation** — Each user sees only their own projects

### 💬 AI Chat System
- **Real-time Streaming** — Token-by-token response streaming via Server-Sent Events (SSE)
- **Multiple Chat Sessions** — Create multiple conversations per project
- **Model Selection** — Choose from multiple free LLM models:
  - `meta-llama/llama-3.3-70b-instruct:free`
  - `deepseek/deepseek-r1-0528:free`
  - `qwen/qwen3-coder:free`
- **Chat History** — Persistent message storage and retrieval
- **Session Rename/Delete** — Manage chat sessions from the UI

### 🧠 Intelligent Memory System
- **Summarization Memory** — Automatic conversation summarization to maintain context
- **Configurable Threshold** — Triggers summarization after N messages
- **Background Processing** — Non-blocking summarization for low latency
- **Database Persistence** — All messages and summaries stored in Supabase



---

## 🏗️ Architecture

![db.png](https://github.com/CaptainRedCodes/Chatbot-Platform/blob/main/db.png)

![architecture.png](https://github.com/CaptainRedCodes/Chatbot-Platform/blob/main/architecture.png)


### Component Overview

| Layer | Component | Purpose |
|-------|-----------|---------|
| **Frontend** | `App.jsx` | React Router with protected routes |
| | `Dashboard.jsx` | Project list and CRUD operations |
| | `ProjectChat.jsx` | Main chat interface with sidebar |
| | `useChat.js` | Hook for chat messaging and streaming |
| | `useSession.js` | Hook for session management |
| | `client.js` | Axios instance with auth interceptors |
| **Backend** | `main.py` | FastAPI app with CORS middleware |
| | `auth_api.py` | Authentication endpoints |
| | `project_api.py` | Project CRUD endpoints |
| | `session.py` | Chat session and messaging endpoints |
| | `SessionManager` | Manages chat sessions in memory + DB |
| | `OpenAIProvider` | LLM integration with streaming |
| | `SummarizationMemory` | Intelligent conversation memory |
| **Database** | `sessions` | Chat session metadata |
| | `messages` | Individual chat messages |
| | `projects` | User project configurations |

---

## 📁 Project Structure

```
Chatbot Platform/
├── backend/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth_api.py      # Auth endpoints
│   │   │   ├── project_api.py   # Project CRUD
│   │   │   └── session.py       # Chat sessions & messaging
│   │   ├── dependencies.py      # JWT validation, DI
│   │   └── router.py            # API router aggregation
│   ├── core/
│   │   ├── config.py            # Settings from environment
│   │   ├── messages.py          # Centralized error/success messages
│   │   ├── openai_client.py     # OpenRouter client factory
│   │   ├── supabase_client.py   # Supabase client factory
│   │   └── interfaces/          # Abstract base classes
│   ├── models/
│   │   ├── auth.py              # User/Token Pydantic models
│   │   ├── chat.py              # Session/Message models
│   │   └── project.py           # Project models
│   ├── services/
│   │   ├── auth_service.py      # Auth business logic
│   │   ├── project_service.py   # Project business logic
│   │   ├── session_manager.py   # Session lifecycle management
│   │   ├── llm/
│   │   │   ├── openai_service.py  # LLM provider implementation
│   │   │   ├── provider.py        # Provider factory
│   │   │   └── summarizer.py      # Summarization utility
│   │   └── memory/
│   │       └── summarization_memory.py  # Memory strategy
│   ├── main.py                  # FastAPI app entry
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile               # Container configuration
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js        # Axios client with interceptors
│   │   ├── components/
│   │   │   ├── chats/
│   │   │   │   ├── ChatHeader.jsx
│   │   │   │   ├── ChatInput.jsx
│   │   │   │   ├── ChatsMessages.jsx
│   │   │   │   ├── ChatsSidebar.jsx
│   │   │   │   ├── ProjectChat.jsx
│   │   │   │   └── modals/
│   │   │   │       ├── NewChatModal.jsx
│   │   │   │       └── SystemPromptModal.jsx
│   │   │   ├── ui/              # Reusable UI components
│   │   │   └── ProtectedRoute.jsx
│   │   ├── hooks/
│   │   │   ├── useChat.js       # Chat state & streaming
│   │   │   ├── useSession.js    # Session management
│   │   │   └── useSystemPrompt.js
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   └── NotFound.jsx
│   │   ├── App.jsx              # Root component with routing
│   │   └── main.jsx             # Entry point
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── .env.example                 # Environment template
├── pyproject.toml               # Python project config
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+**
- **Node.js 18+**
- **Supabase Account** ([supabase.com](https://supabase.com))
- **OpenRouter API Key** ([openrouter.ai](https://openrouter.ai))

### 1. Clone & Setup Environment

```bash
git clone <repository-url>
cd "Chatbot Platform"

# Copy environment template
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` with your credentials:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_JWT_SECRET=your-jwt-secret

# OpenRouter Configuration
OPENROUTER_API_KEY=your-api-key
OPENROUTER_URL=https://openrouter.ai/api/v1
```

Create `frontend/.env`:
```env
VITE_BASE_URL=http://127.0.0.1:8000/api/v1
```

### 3. Database Setup (Supabase)

Create these tables in your Supabase dashboard:

```sql
-- Projects table
CREATE TABLE Projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    project_name TEXT NOT NULL,
    project_description TEXT,
    system_prompt TEXT DEFAULT '',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Sessions table
CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    title TEXT DEFAULT 'New Chat',
    model TEXT DEFAULT 'meta-llama/llama-3.3-70b-instruct:free',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- RLS Policies (users can only access their own data)
CREATE POLICY "Users can manage own projects" ON projects
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own sessions" ON sessions
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can manage messages in own sessions" ON messages
    FOR ALL USING (session_id IN (
        SELECT id FROM sessions WHERE user_id = auth.uid()
    ));
```

### 4. Install & Run Backend

```bash
# Using uv (recommended)
uv sync
uv run uvicorn backend.main:app --reload

# Or using pip
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`

### 5. Install & Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 📡 API Reference

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/signup` | Register new user |
| POST | `/api/v1/auth/login` | Login and get tokens |
| POST | `/api/v1/auth/logout` | Logout current user |
| POST | `/api/v1/auth/reset-password` | Request password reset |
| GET | `/api/v1/auth/session-check` | Validate current session |

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/project/` | Create project |
| GET | `/api/v1/project/` | List all projects |
| GET | `/api/v1/project/{id}` | Get single project |
| PATCH | `/api/v1/project/{id}` | Update project |
| DELETE | `/api/v1/project/{id}` | Delete project |
| GET | `/api/v1/project/available-models` | Get supported AI models |

### Chat Sessions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/sessions/` | Create chat session |
| GET | `/api/v1/sessions/` | List sessions (optional: `?project_id=`) |
| POST | `/api/v1/sessions/{id}/chat` | Send message (non-streaming) |
| POST | `/api/v1/sessions/{id}/chat/stream` | Send message (SSE streaming) |
| GET | `/api/v1/sessions/{id}/history` | Get chat history |
| PATCH | `/api/v1/sessions/{id}` | Rename session |
| DELETE | `/api/v1/sessions/{id}` | Delete session |

---

## 🧪 Health Check

```bash
curl http://127.0.0.1:8000/health
# Response: {"status": "healthy", "version": "1.1.1"}
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Supabase project URL | ✅ |
| `SUPABASE_KEY` | Supabase anon/public key | ✅ |
| `SUPABASE_JWT_SECRET` | JWT secret for token verification | ✅ |
| `OPENROUTER_API_KEY` | OpenRouter API key | ✅ |
| `OPENROUTER_URL` | OpenRouter base URL | ✅ |
| `VITE_BASE_URL` | Backend API URL for frontend | ✅ |



---

## 🚢 Deployment


### Frontend (Static Build)

```bash
cd frontend
npm run build
# Deploy dist/ folder to any static host
```

### Production Considerations

1. Update CORS origins in `backend/main.py`
2. Set proper environment variables
3. Enable Supabase RLS policies
4. Use production database pooling

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend Framework** | FastAPI 0.115+ |
| **Authentication** | Supabase Auth + JWT (ES256) |
| **Database** | Supabase (PostgreSQL) |
| **LLM Provider** | OpenRouter (Llama, DeepSeek, Qwen) |
| **Frontend Framework** | React 19 + Vite 7 |
| **Styling** | Tailwind CSS 4 |
| **HTTP Client** | Axios |
| **Icons** | Lucide React |

---

## 📝 License

This project is private and proprietary.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request
