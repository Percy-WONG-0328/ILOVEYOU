// 等待页面DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 初始化所有交互功能
    setupEventListeners();
    setupTaskCompletion();
    setupTaskForm();
    setupDragAndDrop();
});

// 统一管理所有事件监听器
function setupEventListeners() {
    // 可以在这里添加其他全局事件监听
}

// 显示消息提示
function showMessage(text, isSuccess = true) {
    const messageElement = document.getElementById('message');
    if (!messageElement) return;
    
    messageElement.textContent = text;
    messageElement.className = 'message ' + (isSuccess ? 'success' : 'error');
    messageElement.style.display = 'block';
    
    // 3秒后自动隐藏
    setTimeout(() => {
        messageElement.style.opacity = '0';
        setTimeout(() => {
            messageElement.style.display = 'none';
            messageElement.style.opacity = '1';
        }, 300);
    }, 3000);
}

// 任务完成状态切换功能
function setupTaskCompletion() {
    const tasksContainer = document.querySelector('.tasks');
    if (!tasksContainer) return;
    
    // 使用事件委托，处理动态添加的任务
    tasksContainer.addEventListener('click', function(e) {
        const taskElement = e.target.closest('.task');
        if (!taskElement) return;
        
        // 避免点击链接时触发（如果将来添加链接）
        if (e.target.tagName === 'A') return;
        
        const taskId = taskElement.dataset.taskId;
        const isCompleted = taskElement.classList.contains('completed');
        
        // 显示加载状态
        taskElement.style.opacity = '0.7';
        taskElement.style.cursor = 'wait';
        
        // 更新任务状态
        updateTaskStatus(taskId, !isCompleted)
            .then(success => {
                // 恢复样式
                taskElement.style.opacity = '1';
                taskElement.style.cursor = 'pointer';
                
                if (success) {
                    // 更新UI
                    if (!isCompleted) {
                        taskElement.classList.add('completed');
                        // 添加完成动画
                        taskElement.style.transform = 'scale(1.02)';
                        setTimeout(() => {
                            taskElement.style.transform = 'scale(1)';
                        }, 300);
                        showMessage('任务已标记为完成');
                    } else {
                        taskElement.classList.remove('completed');
                        showMessage('任务已标记为未完成');
                    }
                }
            });
    });
}

// 发送请求更新任务状态到服务器
function updateTaskStatus(taskId, completed) {
    return fetch(`/tasks/${taskId}/toggle/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ completed: completed })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('服务器响应错误');
        }
        return response.json();
    })
    .then(data => {
        if (!data.success) {
            throw new Error(data.error || '更新任务失败');
        }
        return true;
    })
    .catch(error => {
        console.error('更新任务状态失败:', error);
        showMessage('操作失败: ' + error.message, false);
        return false;
    });
}

// 处理添加任务表单
function setupTaskForm() {
    const form = document.getElementById('taskForm');
    if (!form) return;
    
    const submitBtn = document.getElementById('submitBtn');
    const loadingIndicator = submitBtn?.querySelector('.loading');
    const titleInput = document.getElementById('id_title');
    const descriptionInput = document.getElementById('id_description');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // 简单验证
        if (!titleInput.value.trim()) {
            showMessage('请输入任务标题', false);
            titleInput.focus();
            return;
        }
        
        // 显示加载状态
        if (submitBtn) submitBtn.disabled = true;
        if (loadingIndicator) loadingIndicator.style.display = 'inline-block';
        
        const newTask = {
            title: titleInput.value.trim(),
            description: descriptionInput.value.trim()
        };
        
        // 发送添加任务请求
        fetch('/tasks/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(newTask)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error || `HTTP错误: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.success && data.task) {
                // 添加新任务到页面
                addTaskToDOM(data.task);
                
                // 重置表单
                form.reset();
                titleInput.focus();
                showMessage('任务添加成功！');
            } else {
                throw new Error(data.error || '添加任务失败');
            }
        })
        .catch(error => {
            console.error('添加任务失败:', error);
            showMessage('添加失败: ' + error.message, false);
        })
        .finally(() => {
            // 恢复按钮状态
            if (submitBtn) submitBtn.disabled = false;
            if (loadingIndicator) loadingIndicator.style.display = 'none';
        });
    });
}

// 将新任务添加到页面DOM
function addTaskToDOM(task) {
    const tasksContainer = document.querySelector('.tasks');
    if (!tasksContainer) return;
    
    // 检查并移除"暂无任务"提示
    const emptyMessage = tasksContainer.querySelector('p');
    if (emptyMessage) {
        emptyMessage.remove();
    }
    
    // 创建任务元素
    const taskElement = createTaskElement(task);
    
    // 添加进入动画
    taskElement.style.opacity = '0';
    taskElement.style.transform = 'translateY(20px)';
    taskElement.style.transition = 'all 0.3s ease';
    
    // 添加到页面最前面
    tasksContainer.prepend(taskElement);
    
    // 触发动画
    setTimeout(() => {
        taskElement.style.opacity = '1';
        taskElement.style.transform = 'translateY(0)';
    }, 10);
}

// 创建单个任务的DOM元素
function createTaskElement(task) {
    const div = document.createElement('div');
    div.className = `task ${task.completed ? 'completed' : ''}`;
    div.dataset.taskId = task.id;
    div.draggable = true; // 允许拖拽
    
    // 构建任务HTML内容
    div.innerHTML = `
        <h3 class="title">${escapeHtml(task.title)}</h3>
        ${task.description ? `<p>${escapeHtml(task.description)}</p>` : ''}
        <small>创建于: ${task.created_at}</small>
        ${task.completed && task.completed_at ? 
            `<small>已完成于: ${task.completed_at}</small>` : ''}
    `;
    
    // 添加拖拽事件
    div.addEventListener('dragstart', function() {
        this.classList.add('dragging');
        this.style.opacity = '0.5';
    });
    
    div.addEventListener('dragend', function() {
        this.classList.remove('dragging');
        this.style.opacity = '1';
        saveTaskOrder(); // 保存排序
    });
    
    return div;
}

// 任务拖拽排序功能
function setupDragAndDrop() {
    const tasksContainer = document.querySelector('.tasks');
    if (!tasksContainer) return;
    
    // 拖拽经过事件
    tasksContainer.addEventListener('dragover', function(e) {
        e.preventDefault();
        const afterElement = getDragAfterElement(tasksContainer, e.clientY);
        const draggingElement = document.querySelector('.task.dragging');
        
        if (draggingElement && afterElement) {
            tasksContainer.insertBefore(draggingElement, afterElement);
        } else if (draggingElement) {
            tasksContainer.appendChild(draggingElement);
        }
    });
}

// 确定拖拽元素的插入位置
function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.task:not(.dragging)')];
    
    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}

// 保存任务排序（可以扩展为保存到服务器）
function saveTaskOrder() {
    const taskIds = [];
    document.querySelectorAll('.task').forEach(task => {
        taskIds.push(task.dataset.taskId);
    });
    
    console.log('当前任务顺序:', taskIds);
    // 如需保存到服务器，可以取消下面的注释
    
    fetch('/tasks/reorder/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ order: taskIds })
    })
    .then(response => {
        if (!response.ok) throw new Error('保存排序失败');
        return response.json();
    })
    .then(data => {
        if (data.success) {
            console.log('排序已保存');
        }
    })
    .catch(error => {
        console.error('保存排序失败:', error);
    });
    
}

// django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//xss invation?
function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
