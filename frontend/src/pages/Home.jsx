import { Link, Navigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { motion } from "framer-motion";

export default function Home() {
  const { user } = useAuth();

  // If already logged in, go to dashboard
  if (user) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      style={{
        minHeight: "80vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div className="card" style={{ maxWidth: "420px", textAlign: "center" }}>
        <h1>SecureTasker</h1>

        <p style={{ color: "var(--muted)", marginBottom: "1.5rem" }}>
          Secure task & notes management with role-based access
        </p>

        <div style={{ display: "flex", gap: "1rem", justifyContent: "center" }}>
          <Link to="/login" className="btn-primary">
            Login
          </Link>

          <Link to="/register" className="btn-primary">
            Register
          </Link>
        </div>
      </div>
    </motion.div>
  );
}
