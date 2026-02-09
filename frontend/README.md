# 📌 Frontend README — SecureTasker AI Internship Assignment

## 📖 Overview

This is the frontend application for the SecureTasker AI internship assignment.

The frontend is **not a standalone product** — it exists to:

- ✅ Demonstrate backend APIs
- ✅ Validate authentication & authorization logic
- ✅ Provide a clean, usable UI for Tasks & Notes
- ✅ Show real-world frontend-backend integration

The frontend follows clean architecture, avoids over-engineering, and focuses on clarity, correctness, and UX.

---

## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure API Base URL

Update `src/api/axios.js` if your backend runs on a different port:

```javascript
const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",  // Update if needed
});
```

### 3. Run Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173` (or the port Vite assigns).

### 4. Build for Production

```bash
npm run build
```

### 5. Development Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

---

## 🧱 Tech Stack

| Technology | Purpose |
|------------|---------|
| React.js | UI framework (Vite-based setup) |
| React Router | Client-side routing |
| Axios | HTTP client for API calls |
| Framer Motion | Light animations only |
| Plain CSS | Styling with CSS variables for theming |

### ❌ What We Don't Use

- ❌ Redux
- ❌ Heavy UI frameworks
- ❌ Complex state managers


---

## 🗺️ High-Level Frontend Architecture

```
User
 │
 │ Browser (React App)
 │
 ├─ AuthContext (JWT, user state)
 │
 ├─ Pages (Login, Tasks, Notes)
 │
 ├─ Components (Modals, Lists)
 │
 └─ Axios Client
      └─ FastAPI Backend
```

---

## 📂 Directory Structure (Explained File-by-File)

```
frontend/
│
├── src/
│   ├── main.jsx                    # Entry point
│   ├── App.jsx                     # Route definitions
│   │
│   ├── api/
│   │   └── axios.js                # Centralized API client
│   │
│   ├── auth/
│   │   ├── AuthContext.jsx         # JWT & user state management
│   │   └── ProtectedRoute.jsx      # Route protection
│   │
│   ├── pages/
│   │   ├── Home.jsx                # Landing page
│   │   ├── Login.jsx               # Login page
│   │   ├── Register.jsx            # Registration page
│   │   ├── Dashboard.jsx           # Main dashboard
│   │   ├── Tasks.jsx               # Tasks page
│   │   └── Notes.jsx               # Notes page
│   │
│   ├── components/
│   │   ├── Navbar.jsx              # Navigation bar
│   │   │
│   │   ├── tasks/
│   │   │   ├── TaskList.jsx        # Task display component
│   │   │   ├── CreateTaskModal.jsx # Task creation modal
│   │   │   └── EditTaskModal.jsx   # Task editing modal
│   │   │
│   │   └── notes/
│   │       ├── NoteList.jsx        # Note display component
│   │       ├── CreateNoteModal.jsx # Note creation modal
│   │       └── EditNoteModal.jsx   # Note editing modal
│   │
│   └── index.css                   # Global styles & theming
│
└── README.md
```

---

## 🚀 Entry Points

### `main.jsx`

**Purpose:**
- Bootstraps the React app
- Initializes theme (light/dark) from localStorage
- Ensures theme works even before login

**Key Code:**
```javascript
const savedTheme = localStorage.getItem("theme") || "light";
document.body.setAttribute("data-theme", savedTheme);
```

### `App.jsx`

**Purpose:**
- Defines all routes
- Wraps protected routes with `ProtectedRoute`
- Mounts `Navbar` globally

**Routes:**
- `/` → `Home`
- `/login` → `Login`
- `/register` → `Register`
- `/dashboard` → `Protected` (requires auth)
- `/tasks` → `Protected` (requires auth)
- `/notes` → `Protected` (requires auth)

---

## 🔐 Authentication System (Frontend)

### `AuthContext.jsx`

**Responsible for:**
- Storing logged-in user info
- Storing JWT access token
- Exposing `login`, `logout`, `user` methods

**localStorage Keys:**
- `access_token` - JWT token
- `user` - User object

### Auth Flow

1. User logs in
2. Backend returns JWT
3. Token stored in `localStorage`
4. Axios attaches token automatically
5. Protected routes unlock

### `ProtectedRoute.jsx`

**Ensures:**
- User must be authenticated
- Otherwise redirected to `/login`

**Key Code:**
```javascript
if (!user) return <Navigate to="/login" />;
```

---

## 🌐 API Communication

### `api/axios.js`

**Purpose:**
Centralized Axios instance for all API calls.

**Features:**
- Base URL points to backend
- Automatically attaches JWT token from `localStorage`
- Keeps API calls consistent

**Authorization Header:**
```
Authorization: Bearer <token>
```

---

## 🏠 Pages Explained

### `Home.jsx`

**Purpose:**
- Landing page (first impression)
- Shown when user is not logged in
- Explains app purpose
- Links to Login / Register
- Redirects logged-in users to Dashboard

### `Login.jsx` / `Register.jsx`

**Features:**
- Simple, centered card UI
- Shows backend validation errors
- On success → redirects to dashboard

### `Dashboard.jsx`

**Purpose:**
- Lightweight page
- Entry point to Tasks & Notes
- Exists mainly for UX clarity

---

## 📌 Tasks Page (`Tasks.jsx`)

### Purpose

Acts as orchestrator:
- Holds API calls
- Manages state
- Passes callbacks to child components

### Task Capabilities

- ✅ Create task
- ✅ Update status
- ✅ Edit task (owner/admin)
- ✅ Delete task
- ✅ Filter by status

### Component Breakdown

#### `TaskList.jsx`

**Features:**
- Displays tasks
- Shows Edit/Delete only if allowed
- Calls callbacks passed from parent

#### `CreateTaskModal.jsx`

**Features:**
- Floating modal
- Supports:
  - `title`
  - `description`
  - `status`
  - `assignee_id`
- Sends backend-compliant payload

#### `EditTaskModal.jsx`

**Features:**
- Allows partial update
- Uses PATCH semantics
- Prefills existing values

---

## 📝 Notes Page (`Notes.jsx`)

Follows same refactor pattern as Tasks.

### Notes Capabilities

- ✅ Create note
- ✅ Edit own notes only
- ✅ Delete own notes only
- ✅ Visibility handling:
  - `private`
  - `shared`
  - `public`

### Visibility Rules (Frontend)

- Edit/Delete buttons shown only to owner
- Unauthorized actions blocked at backend
- Frontend adds UX-level guard

### Notes Components

#### `NoteList.jsx`

**Features:**
- Displays notes user is allowed to see
- Shows:
  - Title
  - Content
  - Visibility badge
  - Created by + created at
- Hides Edit/Delete for non-owners

#### `CreateNoteModal.jsx`

**Features:**
- Supports visibility-based form
- Shared emails input appears only when needed
- Includes helper text for clarity

#### `EditNoteModal.jsx`

**Features:**
- Same schema as Create
- Prefilled values
- PATCH-based update

---

## 🎨 Theming (Light / Dark)

### Implementation

- Uses CSS variables
- Theme stored in `localStorage`
- Toggle works:
  - Before login
  - After login
  - Across refreshes

### CSS Variables Example

```css
body[data-theme="dark"] {
  --bg: #0f172a;
  --text: #e5e7eb;
}
```

---

## 🧠 Design Decisions (Why This Way)

### Why No Redux?

- App state is simple
- Context + local state sufficient
- Redux would add unnecessary complexity

### Why Modals Instead of Pages?

- Faster UX
- No route explosion
- Matches real-world dashboards

### Why Frontend Guards if Backend Already Checks?

- **Backend = security**
- **Frontend = UX**
- Both are needed

---

## 🧪 Manual Testing Strategy

Frontend was tested by:

- ✅ Login/logout flows
- ✅ Access control on routes
- ✅ Creating/editing/deleting tasks
- ✅ Notes visibility rules
- ✅ Unauthorized edit attempts
- ✅ Theme persistence
- ✅ Refresh behavior

---

## 📈 Scalability (Frontend Perspective)

This frontend can scale by:

- ✅ Adding pagination
- ✅ Extracting shared UI components
- ✅ Adding optimistic UI
- ✅ Introducing caching layer if needed

---

## 📚 Additional Notes

- The frontend communicates with the FastAPI backend running on `http://127.0.0.1:8000`
- All API endpoints are versioned under `/api/v1`
- JWT tokens are stored in `localStorage` (consider httpOnly cookies for production)
- Theme preference persists across sessions

---

## 🤝 Contributing

This is an internship assignment project. For questions or improvements, please refer to the project guidelines.

---

## 📄 License

This project is part of an internship assignment.
