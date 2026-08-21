import TaskList from './TaskList';
import type { Task } from './types';
import {useState} from 'react';
import AddTaskForm from './AddTaskForm';
import { useEffect } from 'react';
import Rosetta from './Rosetta';
import './App.css'
import type { Tag } from './types';

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [showRosetta, setShowRosetta] = useState(false);
  const [tags, setTags] = useState<Tag[]>([]);

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

  useEffect(() => {
    async function fetchTags() {
      try {
        const response = await fetch('/proxy/8000/tags');

        if (!response.ok) {
          throw new Error('Failed to fetch tags');
        }

        const data: Tag[] = await response.json();
        setTags(data);
      } catch (error) {
        console.error(error);
      }
    }

    fetchTags();
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

async function handleAddTask(title: string, priority: 'low' | 'medium' | 'high'){
  const response = await fetch('/proxy/8000/tasks', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json'},
          body: JSON.stringify({ title, priority }),
        })

      
  const data: Task = await response.json();

  setTasks((prev) => [...prev, data]);
}

async function handleAttachTag(task_id: number, tag_id: number) {
    const response = await fetch(`/proxy/8000/tasks/${task_id}/tags/${tag_id}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json'}, 
        })

    const data: Task = await response.json();
    setTasks((prev) => 
      prev.map((t) =>
        t.id === data.id ? data : t
      )
    );
}

async function handleDetachTag(task_id: number, tag_id: number) {
    const response = await fetch(`/proxy/8000/tasks/${task_id}/tags/${tag_id}`, {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json'},
        })

    const data: Task = await response.json();
    setTasks((prev) => 
      prev.map((t) =>
        t.id === data.id ? data : t
      )
    );
}

const availableTags = tags.filter((tag) => !tasks.tags.some((t) => t.tag_id === tag.id)

  return (
    <>
    <div className="app">
      <button className="toggle-btn" onClick={() => setShowRosetta(!showRosetta)}>
        {showRosetta ? 'View Tasks' : 'View Rosetta'}
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
            onAttach={handleAttachTag}
            onDetach={handleDetachTag}
            allTags={tags}
          />
        </>
      )}
    </div>
      
    </>
    
  );
}



export default App;