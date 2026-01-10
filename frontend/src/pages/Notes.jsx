import { useEffect, useState } from "react";
import api from "../api/axios";

import NoteList from "../components/notes/NoteList";
import CreateNoteModal from "../components/notes/CreateNoteModal";
import EditNoteModal from "../components/notes/EditNoteModal";

export default function Notes() {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [showCreate, setShowCreate] = useState(false);
  const [editingNote, setEditingNote] = useState(null);

  // Shared form state
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [visibility, setVisibility] = useState("private");
  const [sharedEmails, setSharedEmails] = useState("");

  /* ===================== API ===================== */

  const fetchNotes = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await api.get("/notes");
      setNotes(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load notes");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  const createNote = async () => {
    try {
      setError(null);
      await api.post("/notes", {
        title,
        content,
        visibility,
        shared_with_emails:
          visibility === "shared"
            ? sharedEmails.split(",").map((e) => e.trim())
            : [],
      });

      resetForm();
      setShowCreate(false);
      fetchNotes();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create note");
    }
  };

  const updateNote = async () => {
    try {
      setError(null);
      await api.patch(`/notes/${editingNote.id}`, {
        title,
        content,
        visibility,
        shared_with_emails:
          visibility === "shared"
            ? sharedEmails.split(",").map((e) => e.trim())
            : [],
      });

      resetForm();
      setEditingNote(null);
      fetchNotes();
    } catch (err) {
      if (err.response?.status === 403 || err.response?.status === 401) {
        setError("You are not allowed to edit this note");
      } else {
        setError(err.response?.data?.detail || "Failed to update note");
      }
      // Keep modal open so user can see the error
    }
  };

  const deleteNote = async (id) => {
    if (!window.confirm("Delete this note?")) return;
    try {
      setError(null);
      await api.delete(`/notes/${id}`);
      fetchNotes();
    } catch (err) {
      if (err.response?.status === 403 || err.response?.status === 401) {
        setError("You are not allowed to delete this note");
      } else {
        setError(err.response?.data?.detail || "Failed to delete note");
      }
    }
  };

  const resetForm = () => {
    setTitle("");
    setContent("");
    setVisibility("private");
    setSharedEmails("");
  };

  /* ===================== UI ===================== */

  return (
    <div style={{ padding: "2rem" }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h1>Notes</h1>
        <button className="btn-primary" onClick={() => setShowCreate(true)}>
          + Create Note
        </button>
      </div>

      {/* Display error messages */}
      {error && (
        <div className="error" style={{ marginTop: "1rem", marginBottom: "1rem" }}>
          {error}
        </div>
      )}

      <NoteList
        notes={notes}
        loading={loading}
        error={error}
        onEdit={(note) => {
          setError(null);
          setEditingNote(note);
          setTitle(note.title);
          setContent(note.content);
          setVisibility(note.visibility);
          setSharedEmails("");
        }}
        onDelete={deleteNote}
      />

      <CreateNoteModal
        open={showCreate}
        onClose={() => {
          setShowCreate(false);
          setError(null);
          resetForm();
        }}
        title={title}
        setTitle={setTitle}
        content={content}
        setContent={setContent}
        visibility={visibility}
        setVisibility={setVisibility}
        sharedEmails={sharedEmails}
        setSharedEmails={setSharedEmails}
        onCreate={createNote}
      />

      <EditNoteModal
        note={editingNote}
        onClose={() => {
          setEditingNote(null);
          setError(null);
          resetForm();
        }}
        title={title}
        setTitle={setTitle}
        content={content}
        setContent={setContent}
        visibility={visibility}
        setVisibility={setVisibility}
        sharedEmails={sharedEmails}
        setSharedEmails={setSharedEmails}
        onUpdate={updateNote}
      />
    </div>
  );
}
