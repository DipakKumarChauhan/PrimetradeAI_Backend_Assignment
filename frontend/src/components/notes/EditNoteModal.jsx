import { motion } from "framer-motion";

export default function EditNoteModal({
  note,
  onClose,
  title,
  setTitle,
  content,
  setContent,
  visibility,
  setVisibility,
  sharedEmails,
  setSharedEmails,
  onUpdate,
}) {
  if (!note) return null;

  return (
    <div className="modal-overlay">
      <motion.div className="modal-card">
        <h3>Edit Note</h3>

        <label>Title</label>
        <input
          className="input"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <label>Content</label>
        <textarea
          className="input"
          rows={5}
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />

        <label>Visibility</label>
        <select
          className="input"
          value={visibility}
          onChange={(e) => setVisibility(e.target.value)}
        >
          <option value="private">Private</option>
          <option value="shared">Shared</option>
          <option value="public">Public</option>
        </select>

        {visibility === "shared" && (
          <>
            <label>Shared With (Emails)</label>
            <input
              className="input"
              value={sharedEmails}
              onChange={(e) => setSharedEmails(e.target.value)}
            />
          </>
        )}

        <div style={{ display: "flex", gap: "0.5rem", marginTop: "1rem" }}>
          <button className="btn-primary" onClick={onUpdate}>
            Update
          </button>
          <button onClick={onClose}>Cancel</button>
        </div>
      </motion.div>
    </div>
  );
}
