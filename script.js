const API_URL = 'http://127.0.0.1:8000';

async function fetchTasks() {
    try {
        console.log('Fetching tasks...');
        const response = await fetch(`${API_URL}/tasks/`);
        const tasks = await response.json();
        displayTasks(tasks);
    } catch (error) {
        console.error('Error fetching tasks:', error);
    }
}

function displayTasks(tasks) {
    const taskList = document.getElementById('taskList');
    taskList.innerHTML = '';

    tasks.forEach(task => {
        const taskCard = document.createElement('div');
        taskCard.className = 'task-card';
        taskCard.innerHTML = `
            <div class="task-card-header">
            <h3>${task.task_name}</h3>
            <p> ${task.status}</p>
            </div>
            <p>${task.task_description || 'No description'}</p>
            <p>Due Date: ${task.due_date || 'No due date'}</p>
        `;
        
        taskCard.addEventListener('click', () => showEditModal(task));
        taskList.appendChild(taskCard);
    });
}

function showEditModal(task) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
        <div class="modal-content">
            <form class="edit-form">
                <h2>Edit Task</h2>
                <input type="text" name="task_name" value="${task.task_name}" placeholder="Task Name">
                <textarea name="task_description" placeholder="Description">${task.task_description || ''}</textarea>
                <input type="date" name="due_date" value="${task.due_date || ''}">
                <select name="status">
                    <option value="pending" ${task.status === 'pending' ? 'selected' : ''}>Pending</option>
                    <option value="in_progress" ${task.status === 'in_progress' ? 'selected' : ''}>In Progress</option>
                    <option value="completed" ${task.status === 'completed' ? 'selected' : ''}>Completed</option>
                </select>
                <div class="modal-actions">
                    <button type="submit" class="save-btn">Save</button>
                    <button type="button" class="cancel-btn">Cancel</button>
                </div>
            </form>
        </div>
    `;

    document.body.appendChild(modal);

    const form = modal.querySelector('form');
    const cancelBtn = modal.querySelector('.cancel-btn');

    cancelBtn.addEventListener('click', () => modal.remove());
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const updatedTask = {
            task_name: formData.get('task_name'),
            task_description: formData.get('task_description'),
            due_date: formData.get('due_date'),
            status: formData.get('status')
        };

        await fetch(`${API_URL}/update_task/${task.task_id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedTask)
        });
        modal.remove();
        fetchTasks();
    });
}

// Add this event listener to the main content area
document.querySelector('.main-content').addEventListener('dblclick', (e) => {
    if (e.target.className === 'main-content') {
        showCreateModal();
    }
});

function showCreateModal() {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
        <div class="modal-content">
            <form class="edit-form">
                <h2>Create New Task</h2>
                <input type="text" name="task_name" placeholder="Task Name" required>
                <textarea name="task_description" placeholder="Description"></textarea>
                <input type="date" name="due_date">
                <div class="modal-actions">
                    <button type="submit" class="save-btn">Create</button>
                    <button type="button" class="cancel-btn">Cancel</button>
                </div>
            </form>
        </div>
    `;

    document.body.appendChild(modal);

    const form = modal.querySelector('form');
    const cancelBtn = modal.querySelector('.cancel-btn');

    cancelBtn.addEventListener('click', () => modal.remove());
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const newTask = {
            task_name: formData.get('task_name'),
            task_description: formData.get('task_description'),
            due_date: formData.get('due_date'),
            status: 'pending'
        };

        await fetch(`${API_URL}/insert_task/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newTask)
        });
        modal.remove();
        fetchTasks();
    });
}



// Call fetchTasks when page loads
fetchTasks();
