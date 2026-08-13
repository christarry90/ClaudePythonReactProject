import type { Task } from './types';

export default function TaskItem({ task, onToggle, onDelete }: { task: Task; onToggle: (id: number) => void; onDelete: (id: number) => void; }) {
  return (
    <div>
      <h1>{task.title}</h1>
      <h2>{String(task.completed)}</h2>
      <button onClick={() => onToggle(task.id)}>Change State</button>
      <button onClick={() => onDelete(task.id)}>Delete</button>
    </div>
  );
}