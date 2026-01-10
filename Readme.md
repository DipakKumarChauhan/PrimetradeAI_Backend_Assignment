# 📘 PrimeTrade AI — Internship Assignment

## 📖 Project Overview

This repository contains a **full-stack implementation** of an internship assignment focused on building a secure, scalable backend system with a supporting frontend UI.

### Primary Focus

- **Backend** is the primary deliverable and demonstrates production-grade engineering practices
- **Frontend** exists to interact with and demonstrate the backend APIs

---

## 🎯 What This Project Does

The system enables authenticated users to:

- ✅ **Register and authenticate** securely using JWT tokens
- ✅ **Manage tasks** with status tracking and assignment capabilities
- ✅ **Manage notes** with advanced visibility rules (private, shared, public)
- ✅ **Interact with the system** through a clean, intuitive UI

### Backend Enforces

- 🔐 Secure authentication and authorization
- 👥 Role-based access control (User vs Admin)
- 🔒 Data ownership and access rules
- 📊 Audit trails for data modifications
- 🛡️ Defensive API design patterns

---

## 🛠️ Tech Stack

### Backend

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Modern Python web framework |
| **MongoDB Atlas** | NoSQL database for flexible data storage |
| **JWT** | Stateless authentication (access tokens) |
| **Pydantic** | Data validation and serialization |
| **bcrypt** | Secure password hashing |
| **Python 3.10+** | Programming language |

### Frontend

| Technology | Purpose |
|------------|---------|
| **React.js** | Modern UI framework (Vite-based) |
| **React Router** | Client-side routing |
| **Axios** | HTTP client for API communication |
| **Plain CSS** | Styling with CSS variables (light/dark theme) |

---

## 📂 Repository Structure

```
primetrade_ai/
│
├── backend/
│   ├── README.md           # Backend-specific documentation
│   ├── requirements.txt    # Python dependencies
│   └── app/                # FastAPI application
│       ├── main.py         # Application entry point
│       ├── core/           # Core configuration & security
│       ├── api/v1/         # API endpoints
│       ├── models/         # MongoDB document models
│       ├── schemas/        # Pydantic schemas for validation
│       ├── services/       # Business logic layer
│       └── utils/          # Utility functions
│
├── frontend/
│   ├── README.md           # Frontend-specific documentation
│   ├── package.json        # Node.js dependencies
│   └── src/                # React application
│       ├── api/            # API client configuration
│       ├── auth/           # Authentication context & routes
│       ├── pages/          # Page components
│       ├── components/     # Reusable UI components
│       └── main.jsx        # Application entry point
│
└── README.md               # (This file) Project overview
```

**Note:** Each major part of the system has its own detailed README explaining internal architecture and usage.

---

## 🔐 Authentication & Authorization

### Authentication Flow

1. Users authenticate using **email and password**
2. Passwords are securely **hashed using bcrypt**
3. Login returns a **JWT access token**
4. Token is required for all protected endpoints
5. Token is sent in `Authorization: Bearer <token>` header

### Role-Based Access Control

The system supports two roles:

#### User
- Can manage own tasks and notes
- Can view assigned tasks
- Subject to note visibility rules

#### Admin
- Can manage **all tasks** (override ownership)
- Can view all users
- **Same note permissions as regular users** (admins do not bypass note visibility rules)

---

## ⚙️ Core Features

### 📋 Tasks Management

- ✅ Create, read, update, delete tasks
- ✅ Status-based filtering (pending, in_progress, completed)
- ✅ Task assignment to other users
- ✅ Admin can manage all tasks
- ✅ Users can manage own or assigned tasks
- ✅ Audit fields track who updated and when

### 📝 Notes Management

- ✅ Create, read, update, delete notes
- ✅ **Visibility levels:**
  - `private` - Only visible to owner
  - `shared` - Visible to owner + selected users (by email)
  - `public` - Visible to all authenticated users
- ✅ Notes are filtered based on visibility rules at query level
- ✅ Admins **cannot bypass** note permissions (same as regular users)
- ✅ Audit fields track modifications

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (for backend)
- **Node.js 18+** (for frontend)
- **MongoDB Atlas** account (or local MongoDB instance)

### Setup Instructions

Detailed setup instructions are provided in:

- 📘 **[Backend README](./backend/README.md)** - Complete backend setup guide
- 📘 **[Frontend README](./frontend/README.md)** - Complete frontend setup guide

These documents explain:
- Installation steps
- Environment variable configuration
- Running the applications
- API usage and endpoints

### Quick Commands

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Access Points

- **Backend API:** http://localhost:8000
- **API Documentation (Swagger):** http://localhost:8000/docs
- **Frontend App:** http://localhost:5173 (or port assigned by Vite)

---

## 🔑 Default Admin Credentials (Development Only)

```
Email: admin
Password: admin123
```

**⚠️ Important:** These credentials are for **local testing only**. Change them in production by updating the environment variables in the backend configuration.

---

## 🏗️ Architecture Highlights

### Backend Architecture

- **Layered Architecture:** Models → Schemas → Services → API Routes
- **Separation of Concerns:** Business logic separated from HTTP handling
- **Defensive Design:** PATCH semantics prevent accidental data loss
- **Audit Trail:** Automatic tracking of data modifications
- **Stateless Authentication:** JWT enables horizontal scaling

### Frontend Architecture

- **Component-Based:** Reusable, modular React components
- **Context API:** Global state management (no Redux needed)
- **Protected Routes:** Client-side route protection for UX
- **Centralized API Client:** Axios instance with automatic token injection
- **Theme Support:** Light/dark mode with localStorage persistence

---

## 🔒 Security Features

- ✅ **Password Hashing:** bcrypt with cost factor 12
- ✅ **JWT Authentication:** Stateless, secure token-based auth
- ✅ **Token Expiration:** 120-minute expiry for access tokens
- ✅ **Input Validation:** Pydantic schemas validate all inputs
- ✅ **Role-Based Authorization:** Enforced at service layer
- ✅ **Ownership Checks:** Users can only modify their own resources
- ✅ **No Sensitive Data Leakage:** Internal fields excluded from API responses

---

## 📊 API Endpoints

### Authentication
- `POST /api/v1/register` - Register new user
- `POST /api/v1/login` - Login and get JWT token

### Users (Admin Only)
- `GET /api/v1/users` - Get all users

### Tasks
- `POST /api/v1/tasks` - Create task(s)
- `GET /api/v1/tasks` - Get tasks (with optional status filter)
- `PATCH /api/v1/tasks/{task_id}` - Update task (partial)
- `DELETE /api/v1/tasks/{task_id}` - Delete task

### Notes
- `POST /api/v1/notes` - Create note
- `GET /api/v1/notes` - Get notes (respects visibility rules)
- `PATCH /api/v1/notes/{note_id}` - Update note (partial)
- `DELETE /api/v1/notes/{note_id}` - Delete note

**Full API documentation available at:** http://localhost:8000/docs

---

## 🧪 Testing

### Backend
- Manual testing via Swagger UI at `/docs`
- All endpoints require authentication (except register/login)
- Test with JWT token in Authorization header

### Frontend
- Manual testing of user flows
- Authentication state persistence
- Route protection and redirects
- Theme persistence

---

## 📈 Scalability Considerations

### Backend
- ✅ Stateless JWT auth → enables horizontal scaling
- ✅ MongoDB indexing on frequently queried fields
- ✅ Modular architecture → easy microservices split
- ✅ Ready for Redis caching layer
- ✅ Load balancer compatible

### Frontend
- ✅ Optimistic UI updates possible
- ✅ Pagination ready for large datasets
- ✅ Component extraction for reusability
- ✅ Caching layer integration ready

---

## 🎓 Project Philosophy

This project is intentionally kept **simple and readable**:

- ✅ No unnecessary abstractions
- ✅ Clear, understandable code structure
- ✅ Easy to follow and extend
- ✅ Focus on best practices over complexity
- ✅ Production-ready patterns

The code is structured to be easily reviewed, understood, and extended by team members.

---

## 📚 Documentation

- **[Backend README](./backend/README.md)** - Complete backend documentation
- **[Frontend README](./frontend/README.md)** - Complete frontend documentation
- **API Documentation** - Interactive Swagger UI at `/docs` when backend is running

---

## 🤝 Contributing

This is an internship assignment project. For questions or improvements, please refer to the project guidelines.

---

## 📄 License

This project is part of an internship assignment for PrimeTrade AI.

---

## 👥 Contact & Support

For questions about this project, please refer to:
- Backend documentation: `backend/README.md`
- Frontend documentation: `frontend/README.md`
- API documentation: http://localhost:8000/docs (when backend is running)
