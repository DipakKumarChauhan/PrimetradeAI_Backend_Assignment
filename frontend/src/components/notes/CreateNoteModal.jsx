import { motion } from "framer-motion";

export default function CreateNoteModal({
  open,
  onClose,
  title,
  setTitle,
  content,
  setContent,
  visibility,
  setVisibility,
  sharedEmails,
  setSharedEmails,
  onCreate,
}) {
  if (!open) return null;

  return (
    <div className="modal-overlay">
      <motion.div className="modal-card" style={{ width: "520px" }}>
        <h3>Create Note</h3>

        <label>Title</label>
        <input
          className="input"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Short descriptive title"
        />
        <small style={{ color: "var(--muted)" }}>
          A brief name to identify this note
        </small>

        <label>Content</label>
        <textarea
          className="input"
          rows={5}
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Write your note here..."
        />
        <small style={{ color: "var(--muted)" }}>
          The main content of your note
        </small>

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
        <small style={{ color: "var(--muted)" }}>
          Private: only you · Shared: selected users · Public: everyone
        </small>

        {visibility === "shared" && (
          <>
            <label>Shared With (Emails)</label>
            <input
              className="input"
              value={sharedEmails}
              onChange={(e) => setSharedEmails(e.target.value)}
              placeholder="user1@example.com, user2@example.com"
            />
            <small style={{ color: "var(--muted)" }}>
              Comma-separated email addresses
            </small>
          </>
        )}

        <div style={{ display: "flex", gap: "0.5rem", marginTop: "1rem" }}>
          <button className="btn-primary" onClick={onCreate}>
            Create
          </button>
          <button onClick={onClose}>Cancel</button>
        </div>
      </motion.div>
    </div>
  );
}
