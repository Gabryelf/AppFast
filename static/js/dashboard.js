// dashboard.js
const API_BASE = window.location.origin;
let authToken = localStorage.getItem('token');

// Показать/скрыть сообщения
function showMessage(elementId, message, isError = false) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = isError ? 'error message' : 'success message';
    element.classList.remove('hidden');

    setTimeout(() => {
        element.classList.add('hidden');
    }, 5000);
}

// Предпросмотр изображений
function previewImages(event) {
    const previewContainer = document.getElementById('preview-container');
    previewContainer.innerHTML = '';

    const files = event.target.files;
    if (files.length === 0) return;

    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (!file.type.startsWith('image/')) continue;

        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.className = 'preview-image';
            img.title = file.name;
            previewContainer.appendChild(img);
        }
        reader.readAsDataURL(file);
    }
}

// Очистить форму
function clearForm() {
    document.getElementById('create-item-form').reset();
    document.getElementById('preview-container').innerHTML = '';
}

// Загрузить изображения на сервер
async function uploadImages(files) {
    if (files.length === 0) return [];

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('images', files[i]);
    }

    try {
        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to upload images');
        }

        const data = await response.json();
        return data.images || [];
    } catch (error) {
        console.error('Upload error:', error);
        return [];
    }
}

// Создать новый Item
async function createItem(event) {
    event.preventDefault();

    if (!authToken) {
        showMessage('error-message', 'Please login first', true);
        return;
    }

    // Получаем данные формы
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const files = document.getElementById('images').files;

    if (!title) {
        showMessage('error-message', 'Title is required', true);
        return;
    }

    try {
        // Шаг 1: Загружаем изображения
        const imagePaths = await uploadImages(files);

        // Шаг 2: Создаем Item
        const itemData = {
            title: title,
            description: description,
            cover_image: imagePaths.length > 0 ? imagePaths[0] : null,
            images: imagePaths
        };

        const response = await fetch(`${API_BASE}/items`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(itemData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create item');
        }

        const item = await response.json();

        // Очищаем форму и показываем успешное сообщение
        clearForm();
        showMessage('success-message', `Item "${item.title}" created successfully!`);

        // Обновляем список items
        loadMyItems();

    } catch (error) {
        console.error('Create item error:', error);
        showMessage('error-message', error.message, true);
    }
}

// Загрузить мои Items
async function loadMyItems() {
    if (!authToken) return;

    try {
        const response = await fetch(`${API_BASE}/items/my`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to load items');
        }

        const data = await response.json();
        displayItems(data.items);
    } catch (error) {
        console.error('Load items error:', error);
        document.getElementById('items-error').textContent = error.message;
        document.getElementById('items-error').classList.remove('hidden');
    }
}

// Отобразить Items
function displayItems(items) {
    const itemsList = document.getElementById('items-list');

    if (!items || items.length === 0) {
        itemsList.innerHTML = '<p>No items yet. Create your first item!</p>';
        return;
    }

    itemsList.innerHTML = items.map(item => `
        <div class="item-card" id="item-${item.id}">
            ${item.cover_image ?
                `<img src="${API_BASE}${item.cover_image}" alt="${item.title}" class="item-image">` :
                '<div class="item-image" style="background: #eee; display: flex; align-items: center; justify-content: center; color: #999;">No Image</div>'
            }
            <div class="item-title">${item.title}</div>
            <div class="item-description">${item.description || 'No description'}</div>
            <div>Created: ${new Date(item.created_at).toLocaleDateString()}</div>
            <div class="item-actions">
                <button onclick="viewItem(${item.id})">View</button>
                <button onclick="editItem(${item.id})" class="secondary">Edit</button>
                <button onclick="deleteItem(${item.id})" class="danger">Delete</button>
            </div>
        </div>
    `).join('');
}

// Просмотр Item
async function viewItem(itemId) {
    try {
        const response = await fetch(`${API_BASE}/items/${itemId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to load item');
        }

        const item = await response.json();
        alert(`Item Details:\nTitle: ${item.title}\nDescription: ${item.description}\nImages: ${item.images.length}\nAuthor: ${item.author?.nick_name || 'Unknown'}`);
    } catch (error) {
        console.error('View item error:', error);
        showMessage('error-message', error.message, true);
    }
}

// Редактировать Item
async function editItem(itemId) {
    const newTitle = prompt('Enter new title:');
    if (!newTitle) return;

    try {
        const response = await fetch(`${API_BASE}/items/${itemId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ title: newTitle })
        });

        if (!response.ok) {
            throw new Error('Failed to update item');
        }

        const updatedItem = await response.json();
        showMessage('success-message', `Item "${updatedItem.title}" updated successfully!`);
        loadMyItems();
    } catch (error) {
        console.error('Edit item error:', error);
        showMessage('error-message', error.message, true);
    }
}

// Удалить Item
async function deleteItem(itemId) {
    if (!confirm('Are you sure you want to delete this item?')) return;

    try {
        const response = await fetch(`${API_BASE}/items/${itemId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to delete item');
        }

        showMessage('success-message', 'Item deleted successfully!');
        loadMyItems();
    } catch (error) {
        console.error('Delete item error:', error);
        showMessage('error-message', error.message, true);
    }
}

// Загрузить информацию пользователя
async function loadUserInfo() {
    if (!authToken) {
        window.location.href = '/login';
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/user`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (!response.ok) {
            if (response.status === 401) {
                localStorage.removeItem('token');
                window.location.href = '/login';
                return;
            }
            throw new Error('Failed to load user info');
        }

        const user = await response.json();
        document.getElementById('user-info').innerHTML = `
            <p><strong>Name:</strong> ${user.first_name || 'Not set'} ${user.last_name || ''}</p>
            <p><strong>Nickname:</strong> ${user.nick_name || 'Not set'}</p>
            <p><strong>Email:</strong> ${user.email}</p>
        `;

        // Загружаем items пользователя
        loadMyItems();

    } catch (error) {
        console.error('Load user error:', error);
        document.getElementById('error-message').textContent = error.message;
        document.getElementById('error-message').classList.remove('hidden');
    }
}

// Обновить информацию пользователя
function refreshUserInfo() {
    loadUserInfo();
    showMessage('success-message', 'Information refreshed!');
}

// Выйти из системы
async function logout() {
    try {
        await fetch(`${API_BASE}/logout`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        localStorage.removeItem('token');
        window.location.href = '/login';
    } catch (error) {
        console.error('Logout error:', error);
        localStorage.removeItem('token');
        window.location.href = '/login';
    }
}

// Проверяем токен при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    authToken = localStorage.getItem('token');
    if (!authToken) {
        window.location.href = '/login';
    } else {
        loadUserInfo();
    }
});