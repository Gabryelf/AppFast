document.addEventListener('DOMContentLoaded', function() {
    // Константы
    const API_BASE = window.location.origin;
    const authToken = localStorage.getItem('token');

    // Элементы DOM
    const createItemForm = document.getElementById('create-item-form');
    const itemsList = document.getElementById('items-list');
    const userInfo = document.getElementById('user-info');
    const logoutBtn = document.getElementById('logout-btn');
    const errorMessage = document.getElementById('error-message');
    const successMessage = document.getElementById('success-message');

    // Проверка авторизации
    if (!authToken) {
        redirectToLogin();
        return;
    }

    // Инициализация
    loadUserInfo();
    loadMyItems();
    setupEventListeners();

    // ===================== ОСНОВНЫЕ ФУНКЦИИ =====================

    function redirectToLogin() {
        alert('Пожалуйста, войдите в систему');
        window.location.href = '/login';
    }

    function showMessage(message, isError = false) {
        const element = isError ? errorMessage : successMessage;
        const otherElement = isError ? successMessage : errorMessage;

        if (element) {
            element.textContent = message;
            element.style.display = 'block';
            element.className = isError ? 'error-message' : 'success-message';
        }

        if (otherElement) {
            otherElement.style.display = 'none';
        }

        // Автоматическое скрытие через 5 секунд
        setTimeout(() => {
            if (element) element.style.display = 'none';
        }, 5000);
    }

    // ===================== РАБОТА С ПОЛЬЗОВАТЕЛЕМ =====================

    async function loadUserInfo() {
        try {
            const response = await fetch(`${API_BASE}/api/user`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${authToken}`
                }
            });

            if (response.status === 401) {
                // Неавторизован
                localStorage.removeItem('token');
                redirectToLogin();
                return;
            }

            if (!response.ok) {
                throw new Error('Ошибка загрузки информации о пользователе');
            }

            const user = await response.json();
            displayUserInfo(user);
        } catch (error) {
            console.error('Error loading user info:', error);
            showMessage('Ошибка загрузки профиля', true);
        }
    }

    function displayUserInfo(user) {
        if (!userInfo) return;

        userInfo.innerHTML = `
            <div class="user-profile">
                <h3>Профиль пользователя</h3>
                <p><strong>Имя:</strong> ${user.first_name || 'Не указано'}</p>
                <p><strong>Фамилия:</strong> ${user.last_name || 'Не указано'}</p>
                <p><strong>Никнейм:</strong> ${user.nick_name || 'Не указано'}</p>
                <p><strong>Email:</strong> ${user.email}</p>
                <p><strong>Дата регистрации:</strong> ${new Date(user.created_at).toLocaleDateString()}</p>
            </div>
        `;
    }

    async function logout() {
        try {
            await fetch(`${API_BASE}/api/logout`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${authToken}`
                }
            });
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
    }

    // ===================== РАБОТА С ITEMS =====================

    async function loadMyItems() {
        try {
            const response = await fetch(`${API_BASE}/api/items/my`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${authToken}`
                }
            });

            if (response.status === 401) {
                localStorage.removeItem('token');
                redirectToLogin();
                return;
            }

            if (!response.ok) {
                throw new Error('Ошибка загрузки предметов');
            }

            const data = await response.json();
            displayItems(data.items);
        } catch (error) {
            console.error('Error loading items:', error);
            if (itemsList) {
                itemsList.innerHTML = '<p class="error">Ошибка загрузки предметов</p>';
            }
        }
    }

    function displayItems(items) {
        if (!itemsList) return;

        if (!items || items.length === 0) {
            itemsList.innerHTML = '<p>У вас пока нет предметов. Создайте первый!</p>';
            return;
        }

        itemsList.innerHTML = items.map(item => `
            <div class="item-card" data-item-id="${item.id}">
                <div class="item-header">
                    <h4>${item.title}</h4>
                    <span class="item-date">${new Date(item.created_at).toLocaleDateString()}</span>
                </div>
                ${item.description ? `<p class="item-description">${item.description}</p>` : ''}
                ${item.cover_image ?
                    `<div class="item-image">
                        <img src="${item.cover_image}" alt="${item.title}" onerror="this.style.display='none'">
                    </div>` :
                    '<div class="no-image">Нет изображения</div>'
                }
                <div class="item-actions">
                    <button onclick="editItem(${item.id})" class="btn-edit">Редактировать</button>
                    <button onclick="deleteItem(${item.id})" class="btn-delete">Удалить</button>
                </div>
            </div>
        `).join('');
    }

    async function createItem(event) {
        event.preventDefault();

        if (!createItemForm) return;

        const formData = new FormData(createItemForm);
        const title = formData.get('title')?.trim();
        const description = formData.get('description')?.trim();
        const coverImage = formData.get('cover_image')?.trim();

        if (!title) {
            showMessage('Название обязательно для заполнения', true);
            return;
        }

        const itemData = {
            title: title,
            description: description || null,
            cover_image: coverImage || null,
            images: []  // Пока не реализована загрузка нескольких изображений
        };

        const submitBtn = createItemForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Создание...';
        submitBtn.disabled = true;

        try {
            const response = await fetch(`${API_BASE}/api/items`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authToken}`
                },
                body: JSON.stringify(itemData)
            });

            if (response.status === 401) {
                localStorage.removeItem('token');
                redirectToLogin();
                return;
            }

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Ошибка создания предмета');
            }

            const newItem = await response.json();
            showMessage(`Предмет "${newItem.title}" успешно создан!`);

            // Очищаем форму
            createItemForm.reset();

            // Обновляем список
            loadMyItems();
        } catch (error) {
            console.error('Error creating item:', error);
            showMessage(error.message, true);
        } finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    }

    async function editItem(itemId) {
        const newTitle = prompt('Введите новое название предмета:');
        if (!newTitle) return;

        try {
            const response = await fetch(`${API_BASE}/api/items/${itemId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authToken}`
                },
                body: JSON.stringify({ title: newTitle })
            });

            if (response.status === 401) {
                localStorage.removeItem('token');
                redirectToLogin();
                return;
            }

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Ошибка обновления предмета');
            }

            showMessage('Предмет успешно обновлён!');
            loadMyItems();
        } catch (error) {
            console.error('Error editing item:', error);
            showMessage(error.message, true);
        }
    }

    async function deleteItem(itemId) {
        if (!confirm('Вы уверены, что хотите удалить этот предмет?')) return;

        try {
            const response = await fetch(`${API_BASE}/api/items/${itemId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${authToken}`
                }
            });

            if (response.status === 401) {
                localStorage.removeItem('token');
                redirectToLogin();
                return;
            }

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Ошибка удаления предмета');
            }

            showMessage('Предмет успешно удалён!');
            loadMyItems();
        } catch (error) {
            console.error('Error deleting item:', error);
            showMessage(error.message, true);
        }
    }

    // ===================== НАСТРОЙКА ОБРАБОТЧИКОВ СОБЫТИЙ =====================

    function setupEventListeners() {
        // Форма создания предмета
        if (createItemForm) {
            createItemForm.addEventListener('submit', createItem);
        }

        // Кнопка выхода
        if (logoutBtn) {
            logoutBtn.addEventListener('click', logout);
        }

        // Кнопка обновления списка
        const refreshBtn = document.getElementById('refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', function() {
                loadMyItems();
                showMessage('Список обновлён');
            });
        }
    }

    // Делаем функции глобальными для вызова из HTML
    window.editItem = editItem;
    window.deleteItem = deleteItem;
});