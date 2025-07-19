document.addEventListener('DOMContentLoaded', () => {
  const taskInput = document.getElementById('taskInput');
  const deadlineInput = document.getElementById('deadlineInput');
  const statusInput = document.getElementById('statusInput');
  const addTaskBtn = document.getElementById('addTaskBtn');
  const taskList = document.getElementById('taskList');

  addTaskBtn.addEventListener('click', () => {
    const task = taskInput.value.trim();
    const deadline = deadlineInput.value;
    const status = statusInput.value;

    if (!task || !deadline || !status) {
      alert('Please fill all fields!');
      return;
    }

    fetch('/add', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({task, deadline, status})
    })
    .then(res => res.json())
    .then(data => {
      location.reload(); 
    });
  });

  taskList.addEventListener('click', (e) => {
    const card = e.target.closest('.task-card');
    if (!card) return;

    const taskId = card.getAttribute('data-id');

    if (e.target.classList.contains('complete')) {
      fetch(`/complete/${taskId}`, { method: 'PATCH' })
        .then(res => res.json())
        .then(() => location.reload());
    }

    if (e.target.classList.contains('delete')) {
      fetch(`/delete/${taskId}`, { method: 'DELETE' })
        .then(res => res.json())
        .then(() => location.reload());
    }
  });
});
