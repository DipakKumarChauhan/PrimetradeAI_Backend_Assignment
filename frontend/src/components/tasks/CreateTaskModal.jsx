import { motion } from "framer-motion";

export default function CreateTaskModal({
  open,
  onClose,
  title,
  setTitle,
  description,
  setDescription,
  status,
  setStatus,
  assigneeId,
  setAssigneeId,
  onCreate,
}) {
  if (!open) return null;

  return (
    <div className="modal-overlay">
      <motion.div className="modal-card" style={{ width: "520px" }}>
        <h3>Create Task</h3>

        <input 
          className="input" 
          placeholder="Enter task title" 
          value={title} 
          onChange={(e) => setTitle(e.target.value)} 
        />
        <textarea 
          className="input" 
          rows={7} 
          placeholder="Enter task description" 
          value={description} 
          onChange={(e) => setDescription(e.target.value)} 
        />

        <select className="input" value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="" disabled>Select status</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>

        <textarea  
          className="input" 
          rows={3} 
          placeholder="Enter assignee email (e.g. user@test.com) or ID. This Works for Admin Only. for Normal Users even passing email wil create a private task" 
          value={assigneeId} 
          onChange={(e) => setAssigneeId(e.target.value)} 
        />

        <div style={{ display: "flex", gap: "0.5rem" }}>
          <button className="btn-primary" onClick={onCreate}>Create</button>
          <button onClick={onClose}>Cancel</button>
        </div>
      </motion.div>
    </div>
  );
}
