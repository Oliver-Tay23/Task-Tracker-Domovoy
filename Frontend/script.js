const taskForm = document.getElementById("taskForm");
const taskInput = document.getElementById("taskInput");
const taskList = document.getElementById("taskList");

async function fetchTasks() {
  const res = await fetch("/api/tasks");
  const tasks = await res.json();
  renderTasks(tasks);
}

function renderTasks(tasks) {
  taskList.innerHTML = "";

  if (tasks.length === 0) {
    const empty = document.createElement("li");
    empty.className = "task-list__empty";
    empty.textContent = "No tasks yet — add one above.";
    taskList.appendChild(empty);
    return;
  }

  tasks.forEach(function (task) {
    const li = document.createElement("li");
    li.className = "task-item" + (task.done ? " task-item--done" : "");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = task.done;
    checkbox.addEventListener("change", async function () {
      await fetch("/api/tasks/" + task.id, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ done: checkbox.checked })
      });
      fetchTasks();
    });

    const text = document.createElement("span");
    text.className = "task-item__text";
    text.textContent = task.text;

    const del = document.createElement("button");
    del.className = "task-item__delete";
    del.type = "button";
    del.textContent = "✕";
    del.addEventListener("click", async function () {
      await fetch("/api/tasks/" + task.id, { method: "DELETE" });
      fetchTasks();
    });

    li.appendChild(checkbox);
    li.appendChild(text);
    li.appendChild(del);
    taskList.appendChild(li);
  });
}

taskForm.addEventListener("submit", async function (e) {
  e.preventDefault();
  const value = taskInput.value.trim();
  if (!value) return;

  await fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: value })
  });

  taskInput.value = "";
  fetchTasks();
});

fetchTasks();