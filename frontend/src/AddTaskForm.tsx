import { useState } from 'react';

function AddTaskForm({
  onAddTask,
}: {
  onAddTask: (title: string) => void;
}) {
  const [title, setTitle] = useState('');

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!title.trim()) return;

    onAddTask(title);
    setTitle('');
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={title}   
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter a task"
      />

      <button type="submit">
        Add Task
      </button>
    </form>
  );
}

export default AddTaskForm;