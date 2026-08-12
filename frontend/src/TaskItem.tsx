import type { Task } from './types';

export default function TaskItem({ task, onToggle }: { task: Task; onToggle: (id: string) => void; }) {
  return (
    <div>
      <h1>{task.title}</h1>
      <h2>{String(task.completed)}</h2>
      <button onClick={() => onToggle(task.id)}>Change State</button>
    </div>
  );
}