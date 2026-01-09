# 📘 Internship Backend Assignment
## FastAPI + MongoDB | Production-Oriented Backend System

---

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone <repo-url>
cd backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create `.env` file in the `backend/` directory:

```env
MONGODB_URI=<mongodb-atlas-uri>
DATABASE_NAME=internship_db
JWT_SECRET_KEY=<your-secret-key>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=120
ADMIN_EMAIL=<admin-email>
ADMIN_PASSWORD=<admin-password>
CORS_ORIGINS=*
```

**Note:** Generate a secure JWT secret key. You can use:
```python
import secrets
secrets.token_urlsafe(32)
```

### 5. Run Server
```bash
uvicorn app.main:app --reload
```

### 6. Access API Documentation
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## 📌 Project Overview

This project is a production-grade backend system built as part of an internship assignment.
The goal is to demonstrate real-world backend engineering practices, not just CRUD APIs.

The system provides:

- ✅ Secure authentication using JWT
- ✅ Role-Based Access Control (User vs Admin)
- ✅ Ownership-based authorization
- ✅ Tasks management
- ✅ Notes management with privacy, public visibility, and sharing
- ✅ Defensive API design (PATCH semantics, audit fields)
- ✅ Clean, scalable, modular architecture

A minimal frontend exists only to demonstrate API usage.
**The backend is the primary focus.**

---

## 🧠 High-Level System Capabilities

### What this backend does

- ✅ Authenticates users securely
- ✅ Issues JWT access tokens
- ✅ Enforces role-based and ownership-based access
- ✅ Allows users to manage tasks
- ✅ Allows users to manage notes with advanced visibility rules
- ✅ Prevents accidental data loss during updates
- ✅ Records audit metadata for updates
- ✅ Is structured for future scalability

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend Framework | FastAPI (Python) |
| Database | MongoDB Atlas |
| Authentication | JWT (Access Tokens) |
| Password Hashing | bcrypt |
| Frontend | React.js (basic) |
| Deployment | Local (Docker intentionally skipped) |

---

## 📂 Project Structure (VERY IMPORTANT)

```
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── tasks.py
│   │       └── notes.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── task.py
│   │   └── note.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── task.py
│   │   └── note.py
│   │
│   ├── services/
│   │   ├── task_services.py
│   │   └── note_service.py
│   │
│   └── utils/
│       └── dependencies.py
│
├── requirements.txt
├── .env
└── README.md
```

---

## 🔍 How to Read This Codebase (IMPORTANT)

This project follows a **layered architecture**.
Each layer has **one responsibility**.

### Recommended reading order:

1. `main.py`
2. `core/`
3. `models/`
4. `schemas/`
5. `services/`
6. `api/v1/`

If you read in this order, the system will make sense naturally.

---

## 🚀 Entry Point — main.py

### Purpose
- Creates FastAPI app
- Registers API routers
- Manages MongoDB lifecycle

### Imports
- `app.core.database`
- `app.api.v1.*`

### Responsibilities
- Application startup & shutdown
- Health check endpoint
- API versioning (`/api/v1`)

---

## 🧱 Core Layer (app/core)

### database.py

**Purpose:**
Manages MongoDB connection lifecycle.

**Used by:**
- Services (task_services, note_services)
- Health check
- Admin seeding

**Why centralized:**
Prevents multiple MongoDB clients, ensures clean startup/shutdown.

### security.py

**Purpose:**
All cryptographic and token-related logic.

**Contains:**
- Password hashing
- Password verification
- JWT creation
- JWT decoding

**Used by:**
- Auth services
- Dependency injection

### config.py

**Purpose:**
Environment variable management using Pydantic Settings.

**Contains:**
- Database configuration
- JWT settings
- Admin credentials
- CORS configuration

---

## 📦 Models Layer (app/models)

These represent **MongoDB documents**, NOT API payloads.

### user.py

Defines how users are stored internally:
- `_id`
- `email`
- `password_hash`
- `role`
- `created_at`

### task.py

Defines task structure:
- Ownership (`owner_id`)
- Status enum
- Audit fields:
  - `updated_at`
  - `updated_by`

### note.py

Defines note structure:
- Owner
- Visibility (`private`, `public`, `shared`)
- Shared user IDs
- Audit fields

---

## 🧾 Schemas Layer (app/schemas)

Schemas define **API contracts**, not DB structure.

### Why schemas exist
- Input validation
- Output shaping
- Prevent leaking internal fields
- Enforce PATCH semantics

### Update Schemas (Important Design)

Update schemas do **not** have default values.

This prevents Swagger or clients from:
- Accidentally overwriting data
- Sending placeholder values

**This is a defensive backend design choice.**

---

## 🧠 Services Layer (app/services)

This is the **brain of the system**.

### Responsibilities
- Business logic
- Authorization checks
- Ownership enforcement
- Audit field injection
- Database operations

### What services do NOT do
- Handle HTTP requests
- Parse headers
- Format responses

### task_services.py

Handles:
- Task creation
- Task retrieval
- Status filtering
- PATCH updates
- Admin overrides
- Audit fields

### note_service.py

Handles:
- Note creation
- Visibility enforcement
- Email-based sharing
- Query-level access control
- PATCH updates
- Audit fields

---

## 🌐 API Layer (app/api/v1)

Routers are **thin by design**.

### Responsibilities
- HTTP routing
- Dependency injection
- Request/response mapping

### What routers do NOT do
- Business logic
- Database access
- Authorization decisions

### Example: tasks.py

Imports:
- `app.schemas.task`
- `app.services.task_services`
- `app.utils.dependencies`

Calls service methods and returns responses.

---

## 🔐 Authentication Flow (Step-by-Step)

1. **User registers**
   - Password is hashed using bcrypt

2. **User logs in**
   - JWT access token is generated

3. **Token is sent in:**
   ```
   Authorization: Bearer <token>
   ```

4. **`get_current_user`:**
   - Decodes token
   - Fetches user
   - Attaches user object to request

---

## 🛂 Role-Based Access Control (RBAC)

### User
- Can manage own tasks
- Can manage own notes
- Can see public/shared notes

### Admin
- Can view all users
- Can manage all tasks
- Treated as normal user for notes
- Cannot see others' private notes

**This separation avoids privilege escalation.**

---

## 📋 Tasks Module Rules

- Tasks are owned by users
- Admin can override ownership
- Status is enum-based
- Supports filtering
- Supports PATCH updates
- Audit fields are injected automatically

---

## 📝 Notes Module Rules

### Visibility
- **private:** only owner
- **public:** all authenticated users
- **shared:** owner + selected users

### Sharing
- Uses email addresses
- IDs are never exposed
- Emails are resolved internally

---

## 🔄 PATCH Semantics (IMPORTANT)

- Only fields explicitly sent are updated
- Missing fields are untouched
- Prevents accidental data loss
- Audit fields always updated server-side

---

## 📈 Scalability & Future Improvements

- ✅ Stateless JWT auth → horizontal scaling
- ✅ MongoDB indexing on:
  - `email`
  - `owner_id`
- ✅ Easy microservices split
- ✅ Redis caching can be added
- ✅ Load balancers supported

---

## 📝 API Endpoints

### Authentication
- `POST /api/v1/register` - Register new user
- `POST /api/v1/login` - Login and get JWT token

### Users
- `GET /api/v1/users` - Get all users (Admin only)

### Tasks
- `POST /api/v1/tasks` - Create task(s)
- `GET /api/v1/tasks` - Get tasks (with optional status filter)
- `PATCH /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task

### Notes
- `POST /api/v1/notes` - Create note
- `GET /api/v1/notes` - Get notes (respects visibility rules)
- `PATCH /api/v1/notes/{note_id}` - Update note
- `DELETE /api/v1/notes/{note_id}` - Delete note

---

## 🔒 Security Best Practices

- Passwords are hashed with bcrypt (cost factor 12)
- JWT tokens expire after 120 minutes
- All endpoints (except auth) require authentication
- Role-based and ownership-based authorization enforced
- Input validation via Pydantic schemas
- No sensitive data in API responses

---

## 🧪 Testing

To test the API:

1. Register a user or login
2. Copy the JWT token from response
3. Use it in the Authorization header: `Bearer <token>`
4. Test endpoints via Swagger UI at `/docs`

---

## 📚 Additional Notes

- The system uses MongoDB ObjectId internally but exposes string IDs in API
- All timestamps are in UTC
- Error responses follow consistent format
- API versioning allows for future breaking changes

---

## 🤝 Contributing

This is an internship assignment project. For questions or improvements, please refer to the project guidelines.

---

## 📄 License

This project is part of an internship assignment.
