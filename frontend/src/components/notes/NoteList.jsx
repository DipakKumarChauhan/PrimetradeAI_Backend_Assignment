import { motion } from "framer-motion";
import { useAuth } from "../../auth/AuthContext";

export default function NoteList({ notes, loading, error, onEdit, onDelete }) {
  const { user } = useAuth();

  if (loading) return <p>Loading...</p>;
  if (error) return <div className="error">{error}</div>;
  if (notes.length === 0)
    return <p style={{ color: "var(--muted)" }}>No notes found</p>;

  return (
    <div style={{ display: "grid", gap: "1rem", marginTop: "1rem" }}>
      {notes.map((note) => {
        const isOwner = user && note.owner_id === user.id;

        return (
          <motion.div key={note.id} className="card">
            <h3>{note.title}</h3>

            <p style={{ color: "var(--muted)" }}>{note.content}</p>

            <span className="badge">{note.visibility}</span>

            {/* Metadata: Created by and Created at */}
            {note.created_at && (
              <p style={{ fontSize: "0.8rem", color: "var(--muted)", marginTop: "0.5rem" }}>
                Created by <strong>{note.owner_email || note.owner_id}</strong> ·{" "}
                {new Date(note.created_at).toLocaleString()}
              </p>
            )}

            {/* Only show Edit/Delete buttons for note owner */}
            {isOwner && (
              <div style={{ display: "flex", gap: "0.5rem", marginTop: "0.75rem" }}>
                <button onClick={() => onEdit(note)}>Edit</button>
                <button onClick={() => onDelete(note.id)}>Delete</button>
              </div>
            )}
          </motion.div>
        );
      })}
    </div>
  );
}
