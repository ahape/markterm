
document.addEventListener('DOMContentLoaded', () => {
    const listItems = document.querySelectorAll('li');
    let todoCount = 0;
    let completedCount = 0;

    // Create Progress UI
    const content = document.querySelector('.content');
    const progressContainer = document.createElement('div');
    progressContainer.className = 'todo-progress-container';
    progressContainer.innerHTML = `
        <div class="todo-stats">
            <span id="todo-count">0/0 Tasks Completed</span>
            <span id="todo-percent">0%</span>
        </div>
        <div class="todo-progress-bar">
            <div class="todo-progress-fill" id="todo-progress-fill"></div>
        </div>
    `;
    content.insertBefore(progressContainer, content.firstChild);

    const updateProgress = () => {
        const total = document.querySelectorAll('.todo-item').length;
        const completed = document.querySelectorAll('.todo-item.completed').length;
        const percent = total === 0 ? 0 : Math.round((completed / total) * 100);
        
        document.getElementById('todo-count').textContent = `${completed}/${total} Tasks Completed`;
        document.getElementById('todo-percent').textContent = `${percent}%`;
        document.getElementById('todo-progress-fill').style.width = `${percent}%`;
    };

    const clearButton = document.getElementById('clear-progress');
    clearButton.addEventListener('click', () => {
        if (confirm('Are you sure you want to clear all progress?')) {
            document.querySelectorAll('.todo-checkbox').forEach((cb, i) => {
                cb.checked = false;
                const li = cb.parentElement;
                li.classList.remove('completed');
                const storageKey = `todo-state-${window.location.pathname}-${i}`;
                localStorage.removeItem(storageKey);
            });
            updateProgress();
        }
    });

    listItems.forEach((li, index) => {
        const text = li.innerHTML.trim();
        const isUnchecked = text.startsWith('[ ]');
        const isChecked = text.startsWith('[x]') || text.startsWith('[X]');

        if (isUnchecked || isChecked) {
            li.classList.add('todo-item');
            const id = `todo-${index}`;
            
            // Remove the [ ] or [x] text
            const cleanHtml = text.replace(/^\[[ xX]\]/, '').trim();
            
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.className = 'todo-checkbox';
            checkbox.id = id;
            checkbox.checked = isChecked;

            // Use LocalStorage for persistence
            const storageKey = `todo-state-${window.location.pathname}-${index}`;
            const savedState = localStorage.getItem(storageKey);
            if (savedState !== null) {
                checkbox.checked = savedState === 'true';
            }

            if (checkbox.checked) {
                li.classList.add('completed');
            }

            li.innerHTML = '';
            li.appendChild(checkbox);
            
            const label = document.createElement('label');
            label.htmlFor = id;
            label.innerHTML = cleanHtml;
            label.style.cursor = 'pointer';
            label.style.flex = '1';
            li.appendChild(label);

            checkbox.addEventListener('change', () => {
                if (checkbox.checked) {
                    li.classList.add('completed');
                } else {
                    li.classList.remove('completed');
                }
                localStorage.setItem(storageKey, checkbox.checked);
                updateProgress();
            });
        }
    });

    updateProgress();
});
