import { motion } from "framer-motion";

export default function EditTaskModal({
  task,
  onClose,
  title,
  setTitle,
  description,
  setDescription,
  onUpdate,
  setTask,
}) {
  if (!task) return null;

  return (
    <div className="modal-overlay">
      <motion.div className="modal-card">
        <h3>Edit Task</h3>

        <input className="input" value={title} onChange={(e) => setTitle(e.target.value)} />
        <textarea className="input" rows={4} value={description} onChange={(e) => setDescription(e.target.value)} />

        <select
          className="input"
          value={task.status}
          onChange={(e) => setTask({ ...task, status: e.target.value })}
        >
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>

        <div style={{ display: "flex", gap: "0.5rem" }}>
          <button className="btn-primary" onClick={onUpdate}>Update</button>
          <button onClick={onClose}>Cancel</button>
        </div>
      </motion.div>
    </div>
  );
}
