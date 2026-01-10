import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

import api from "../api/axios";

export default function Dashboard() {
  const navigate = useNavigate();

  const [tasks, setTasks] = useState([]);
  const [notes, setNotes] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [tasksRes, notesRes] = await Promise.all([
          api.get("/tasks"),
          api.get("/notes"),
        ]);

        setTasks(tasksRes.data.slice(0, 3));
        setNotes(notesRes.data.slice(0, 3));
      } catch (err) {
        setError("Failed to load dashboard data");
      }
    };

    fetchData();
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      style={{ padding: "2rem" }}
    >
      <h1 style={{ marginBottom: "1.5rem" }}>Dashboard</h1>

      {error && <div className="error">{error}</div>}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "1.5rem",
        }}
      >
        {/* Tasks Preview */}
        <motion.div
          className="card"
          whileHover={{ scale: 1.02 }}
          transition={{ duration: 0.2 }}
        >
          <h3>Tasks</h3>
          <p style={{ color: "var(--muted)", marginBottom: "0.75rem" }}>
            {tasks.length} recent tasks
          </p>

          {tasks.length === 0 && (
            <p style={{ color: "var(--muted)" }}>No tasks yet</p>
          )}

          <ul style={{ paddingLeft: "1rem" }}>
            {tasks.map((task) => (
              <li key={task.id}>{task.title}</li>
            ))}
          </ul>

          <button
            className="btn-primary"
            style={{ marginTop: "1rem" }}
            onClick={() => navigate("/tasks")}
          >
            View All Tasks →
          </button>
        </motion.div>

        {/* Notes Preview */}
        <motion.div
          className="card"
          whileHover={{ scale: 1.02 }}
          transition={{ duration: 0.2 }}
        >
          <h3>Notes</h3>
          <p style={{ color: "var(--muted)", marginBottom: "0.75rem" }}>
            {notes.length} recent notes
          </p>

          {notes.length === 0 && (
            <p style={{ color: "var(--muted)" }}>No notes yet</p>
          )}

          <ul style={{ paddingLeft: "1rem" }}>
            {notes.map((note) => (
              <li key={note.id}>{note.title}</li>
            ))}
          </ul>

          <button
            className="btn-primary"
            style={{ marginTop: "1rem" }}
            onClick={() => navigate("/notes")}
          >
            View All Notes →
          </button>
        </motion.div>
      </div>
    </motion.div>
  );
}
