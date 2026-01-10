import { motion } from "framer-motion";

export default function TaskList({
  tasks,
  loading,
  error,
  setEditingTask,
  deleteTask,
  statusFilter,
  setStatusFilter,
}) {
  return (
    <>
      <select
        className="input"
        value={statusFilter}
        onChange={(e) => setStatusFilter(e.target.value)}
        style={{ maxWidth: "200px", margin: "1rem 0" }}
      >
        <option value="">All</option>
        <option value="pending">Pending</option>
        <option value="in_progress">In Progress</option>
        <option value="done">Done</option>
      </select>

      {error && <div className="error">{error}</div>}
      {loading && <p>Loading...</p>}

      <div style={{ display: "grid", gap: "1rem" }}>
        {tasks.map((task) => (
          <motion.div key={task.id} className="card">
            <h3>{task.title}</h3>
            <p>{task.description}</p>

            <p style={{ margin: "0.5rem 0", color: "var(--muted)" }}>
              Status: <strong>{task.status.replace("_", " ").replace(/\b\w/g, (l) => l.toUpperCase())}</strong>
            </p>

            <div style={{ display: "flex", gap: "0.5rem" }}>
              <button onClick={() => setEditingTask(task)}>Edit</button>
              <button onClick={() => deleteTask(task.id)}>Delete</button>
            </div>
          </motion.div>
        ))}
      </div>
    </>
  );
}
