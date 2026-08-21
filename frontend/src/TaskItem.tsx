import type { Task } from './types';
import type { Tag } from './types';

export default function TaskItem({ task, onToggle, onDelete, onAttach, onDetach, allTags }: { task: Task; onToggle: (id: number) => void; onDelete: (id: number) => void; onAttach: (task_id: number, tag_id: number) => void; onDetach: (task_id: number, tag_id: number) => void; allTags: Tag[] }) {
  return (
    <div className="task-item">
      <h1>{task.title}</h1>
      <h2>{task.priority}</h2>
      <h2>{String(task.completed)}</h2>
      {task.tags.map((tag) => (
        <h2 key={tag.id}>{tag.name} 
          <button onClick={() => onDetach(task.id, tag.id)}>Detach Tag</button>
        </h2>

      ))}
      <button onClick={() => onToggle(task.id)}>Change State</button>
      <button onClick={() => onDelete(task.id)}>Delete</button>
      
    </div>
  );
}