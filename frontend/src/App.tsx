import TaskList from './TaskList';
import type { Task } from './types';
import {useState} from 'react'

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

  return <TaskList tasks={tasks} onToggle={handleToggle}/>;
}



export default App;