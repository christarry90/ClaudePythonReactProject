import TaskList from './TaskList';
import type { Task } from './types';
import {useState} from 'react';
import AddTaskForm from './AddTaskForm';
import { useEffect } from 'react';
import Rosetta from './Rosetta';
import './App.css'
import type { Tag } from './types';
import LoginForm  from './Login';
import SignupForm from './Signup';

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [showRosetta, setShowRosetta] = useState(false);
  const [tags, setTags] = useState<Tag[]>([]);
  const [token, setToken] = useState(() => localStorage.getItem('token'))

  useEffect(() => {
    if(!token) return;
    async function fetchTasks() {
      try {
        const response = await fetch(`/proxy/8000/tasks`, {
          headers: { 
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${token}`,
          },  
        })

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
  }, [token]);

  useEffect(() => {
    if(!token) return;
    async function fetchTags() {
      try {
        const response = await fetch(`/proxy/8000/tags`, {
          headers: { 
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${token}`,
          },  
        })

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
  }, [token]);

  async function handleToggle(id: number) {
    const task = tasks.find((t) => t.id === id)
    const response = await fetch(`/proxy/8000/tasks/${id}`, {
          method: 'PUT',
          headers: { 
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${token}`,
          },  
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
          headers: { 
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${token}`,
          },  
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
          headers: { 
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${token}`,
          },
          body: JSON.stringify({ title, priority }),
        })

      
  const data: Task = await response.json();

  setTasks((prev) => [...prev, data]);
}

async function handleAttachTag(task_id: number, tag_id: number) {
    const response = await fetch(`/proxy/8000/tasks/${task_id}/tags/${tag_id}`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${token}`,
          },           
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
          headers: { 
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${token}`,
          },  
        })

    const data: Task = await response.json();
    setTasks((prev) => 
      prev.map((t) =>
        t.id === data.id ? data : t
      )
    );
}

async function handleLogin(username: string, password: string) {
    const response = await fetch(`/proxy/8000/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded'},
          body: new URLSearchParams({username, password}),
        })
        
        if (!response.ok) {
          throw new Error("Login failed");
        }

        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        setToken(data.access_token);
}

async function handleSignup(username: string, password: string) {
    const response = await fetch(`/proxy/8000/user`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json'},
          body: JSON.stringify({ username, password }),
        })
        
        if (!response.ok) {
          throw new Error("Signup failed");
        }

        handleLogin(username, password)
}

async function handleLogout() {
  localStorage.removeItem("token");
  setToken(null);
}

  return (
    <>
    {!token ? (
      <div className="app">
        <LoginForm onLogin={handleLogin} />
        <SignupForm onSignup={handleSignup} />
      </div>
    ) : ( 
      <div className="app">
      <button className="toggle-btn" onClick={() => setShowRosetta(!showRosetta)}>
        {showRosetta ? 'View Tasks' : 'View Rosetta'}
      </button>
      <button onClick={handleLogout}>
        Logout
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

    )}

    
      
    </>
    
  );
}



export default App;