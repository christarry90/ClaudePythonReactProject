import TaskList from './TaskList';
import type { Task } from './types';
import {useState} from 'react';
import AddTaskForm from './AddTaskForm';
import { useEffect } from 'react';
import Rosetta from './Rosetta';

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [showRosetta, setShowRosetta] = useState(false);
  useEffect(() => {
    async function fetchTasks() {
      try {
        const response = await fetch('/proxy/8000/tasks');

        if (!response.ok) {
          throw new Error('Failed to fetch tasks');
        }

        const data: Task[] = await response.json();
        setTasks(data);
      } catch (error) {
        console.error(error);
      }
    }

    fetchTasks();
  }, []);


  async function handleToggle(id: number) {
    const task = tasks.find((t) => t.id === id)
    const response = await fetch(`/proxy/8000/tasks/${id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json'},
          body: JSON.stringify({completed: !task?.completed}),
        })

    const data: Task = await response.json();
    setTasks((prev) => 
      prev.map((t) =>
        t.id === data.id ? data : t
      )
    );
}

async function handleDelete(id: number){
  const response = await fetch(`/proxy/8000/tasks/${id}`, {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json'},
        })

  if (response.ok) {
    setTasks(
    tasks.filter((task) => task.id !== id)
    );
  }
  
}

async function handleAddTask(title: string){
  const response = await fetch('/proxy/8000/tasks', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json'},
          body: JSON.stringify({ title }),
        })

      
  const data: Task = await response.json();

  setTasks((prev) => [...prev, data]);
}

  return (
    <>
      <button onClick={() => setShowRosetta(!showRosetta)}>
      Toggle View
    </button>

    {showRosetta ? (
      <Rosetta />
    ) : (
      <>
        <AddTaskForm onAddTask={handleAddTask} />
        <TaskList
          tasks={tasks}
          onToggle={handleToggle}
          onDelete={handleDelete}
        />
      </>
    )}
    </>
    
  );
}



export default App;