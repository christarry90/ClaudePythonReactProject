import TaskItem from './TaskItem';
import type { Task } from './types';
import type { Tag } from './types';

function TaskList({
  tasks,
  onToggle,
  onDelete,
  onAttach,
  onDetach,
  allTags,
}: {
  tasks: Task[];
  onToggle: (id: number) => void;
  onDelete: (id: number) => void;
  onAttach: (task_id: number, tag_id: number) => void;
  onDetach: (task_id: number, tag_id: number) => void;
  allTags: Tag[];
}) {
  return (
    <div>
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggle={onToggle}
          onDelete={onDelete}
          onAttach={onAttach}
          onDetach={onDetach}
          allTags = {allTags}
        />
      ))}
    </div>  
  );
}

export default TaskList;