import { useState } from 'react';

function LoginForm({
  onLogin,
}: {
  onLogin: (username: string, password: string) => void;
}) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    onLogin(username, password)
  }

  return (
    <form className="add-task-form" onSubmit={handleSubmit}>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Enter username"
      />

      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Enter password"
      />

      <button type="submit">
        Login
      </button>
    </form>
  );
}

export default LoginForm;