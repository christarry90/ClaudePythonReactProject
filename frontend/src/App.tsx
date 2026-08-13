import TaskList from './TaskList';
import type { Task } from './types';
import {useState} from 'react';
import AddTaskForm from './AddTaskForm';

function App() {
  const [tasks, setTasks] = useState<Task[]>([
    {
      id: '1',
      title: 'Learn React',
      completed: true,
    },
    {
      id: '2',
      title: 'Learn TypeScript',
      completed: false,
    },
    {
      id: '3',
      title: 'Build a Todo App',
      completed: false,
    },
  ]);

  function handleToggle(id: string) {
  setTasks(
    tasks.map((task) =>
      task.id === id
        ? { ...task, completed: !task.completed }
        : task
    )
  );
}

function handleDelete(id: string){
  setTasks(
    tasks.filter((task) => task.id !== id)
  );
}

function handleAddTask(title: string){
  const newTask: Task = {
    id: crypto.randomUUID(),
    title,
    completed: false,
  };

  setTasks((prevTasks) => [...prevTasks, newTask]);
}

  return (
    <>
      <AddTaskForm onAddTask={handleAddTask} />
      <TaskList tasks={tasks} onToggle={handleToggle} onDelete={handleDelete} />
    </>
    
  );
}



export default App;