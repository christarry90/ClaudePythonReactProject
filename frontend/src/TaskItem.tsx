export default function TaskItem({ task }: { task: Task }) {
  return (
    <div>
      <h1>{task.title}</h1>
      <h2>{String(task.completed)}</h2>
    </div>
  );
}