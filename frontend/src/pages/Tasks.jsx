import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import api from "../api/axios";

import TaskList from "../components/tasks/TaskList";
import CreateTaskModal from "../components/tasks/CreateTaskModal";
import EditTaskModal from "../components/tasks/EditTaskModal";

export default function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const [showCreate, setShowCreate] = useState(false);
  const [editingTask, setEditingTask] = useState(null);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState("pending");
  const [assigneeId, setAssigneeId] = useState("");

  /* ---------- API ---------- */

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const res = await api.get("/tasks", {
        params: statusFilter ? { status: statusFilter } : {},
      });
      setTasks(res.data);
    } catch {
      setError("Failed to load tasks");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [statusFilter]);

  const createTask = async () => {
    await api.post("/tasks", {
      title,
      description,
      status,
      ...(assigneeId && { assignee_id: assigneeId }),
    });
    resetForm();
    fetchTasks();
  };

  const updateTask = async () => {
    await api.patch(`/tasks/${editingTask.id}`, {
      title,
      description,
      status: editingTask.status,
    });
    resetForm();
    setEditingTask(null);
    fetchTasks();
  };

  const deleteTask = async (id) => {
    await api.delete(`/tasks/${id}`);
    fetchTasks();
  };

  const resetForm = () => {
    setTitle("");
    setDescription("");
    setStatus("pending");
    setAssigneeId("");
  };

  /* ---------- UI ---------- */

  return (
    <motion.div style={{ padding: "2rem" }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h1>Tasks</h1>
        <button className="btn-primary" onClick={() => setShowCreate(true)}>
          + Create Task
        </button>
      </div>

      <TaskList
        tasks={tasks}
        loading={loading}
        error={error}
        setEditingTask={(task) => {
          setEditingTask(task);
          setTitle(task.title);
          setDescription(task.description || "");
        }}
        deleteTask={deleteTask}
        statusFilter={statusFilter}
        setStatusFilter={setStatusFilter}
      />

      <CreateTaskModal
        open={showCreate}
        onClose={() => setShowCreate(false)}
        title={title}
        setTitle={setTitle}
        description={description}
        setDescription={setDescription}
        status={status}
        setStatus={setStatus}
        assigneeId={assigneeId}
        setAssigneeId={setAssigneeId}
        onCreate={createTask}
      />

      <EditTaskModal
        task={editingTask}
        onClose={() => setEditingTask(null)}
        title={title}
        setTitle={setTitle}
        description={description}
        setDescription={setDescription}
        onUpdate={updateTask}
        setTask={setEditingTask}
      />
    </motion.div>
  );
}
