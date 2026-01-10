import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { motion } from "framer-motion";

export default function Navbar() {
  const auth = useAuth();
  const navigate = useNavigate();

  // Safety check: if auth context is not available, provide defaults
  const user = auth?.user ?? null;
  const logout = auth?.logout ?? (() => {});

  const handleLogout = () => {
    logout();
    navigate("/login");
  };
  const toggleTheme = () => {
    const current = document.body.getAttribute("data-theme") || "light";
    const next = current === "dark" ? "light" : "dark";
    document.body.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  };
  

  return (
    <motion.nav
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "0.75rem 1.5rem",
        background: "var(--card)",
        borderBottom: "1px solid var(--border)",
      }}
    >
      <h3 style={{ margin: 0 }}>Primetrade.ai</h3>

      <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
        {!user && (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
        <motion.button
              onClick={toggleTheme}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              title="Toggle theme"
              style={{
                background: "transparent",
                border: "1px solid var(--border)",
                padding: "0.3rem 0.75rem",
                borderRadius: "6px",
                cursor: "pointer",
              }}
            >
              🌗
            </motion.button>

        {user && (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/tasks">Tasks</Link>
            <Link to="/notes">Notes</Link>

            {/* <motion.button
              onClick={toggleTheme}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              title="Toggle theme"
              style={{
                background: "transparent",
                border: "1px solid var(--border)",
                padding: "0.3rem 0.75rem",
                borderRadius: "6px",
                cursor: "pointer",
              }}
            >
              🌗
            </motion.button> */}

            <motion.button
              onClick={handleLogout}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              style={{
                background: "transparent",
                border: "1px solid var(--border)",
                padding: "0.3rem 0.75rem",
                borderRadius: "6px",
                cursor: "pointer",
                color: "var(--text)",
              }}
            >
              Logout
            </motion.button>
          </>
        )}
      </div>
    </motion.nav>
  );
}
