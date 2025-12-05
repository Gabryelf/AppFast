document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard page loaded');

    // Проверяем наличие токена
    const token = localStorage.getItem('auth_token');
    const tokenInfo = document.getElementById('token-info');

    if (token) {
        tokenInfo.textContent = token.substring(0, 30) + '...';
        // Загружаем информацию о пользователе
        loadUserInfo();
    } else {
        document.getElementById('error-message').style.display = 'block';
        document.getElementById('error-message').textContent = 'You are not logged in. Please login first.';
        document.getElementById('user-info').innerHTML = '<p><a href="/login">Go to Login</a></p>';
    }
});

async function loadUserInfo() {
    const token = localStorage.getItem('auth_token');
    const userInfoDiv = document.getElementById('user-info');
    const errorMessage = document.getElementById('error-message');

    if (!token) {
        errorMessage.style.display = 'block';
        errorMessage.textContent = 'No authentication token found';
        return;
    }

    try {
        const response = await fetch('/user', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const userData = await response.json();
            errorMessage.style.display = 'none';

            // Отображаем информацию о пользователе
            userInfoDiv.innerHTML = `
                <h3>User Information:</h3>
                <p><strong>ID:</strong> ${userData.id}</p>
                <p><strong>Email:</strong> ${userData.email}</p>
                <p><strong>Nickname:</strong> ${userData.nick_name || 'Not set'}</p>
                <p><strong>Full Name:</strong> ${userData.first_name || ''} ${userData.last_name || ''}</p>
            `;
        } else {
            const errorData = await response.json();
            errorMessage.style.display = 'block';
            errorMessage.textContent = `Error: ${errorData.detail || 'Failed to load user data'}`;
            userInfoDiv.innerHTML = '<p><a href="/login">Go to Login</a></p>';

            // Если ошибка аутентификации, очищаем токен
            if (response.status === 403 || response.status === 401) {
                localStorage.removeItem('auth_token');
            }
        }
    } catch (error) {
        console.error('Error loading user info:', error);
        errorMessage.style.display = 'block';
        errorMessage.textContent = 'Network error: ' + error.message;
    }
}

function logout() {
    // Можно добавить запрос на сервер для инвалидации токена
    // await fetch('/logout', { method: 'POST' });

    localStorage.removeItem('auth_token');
    window.location.href = '/login';
}

function refreshUserInfo() {
    loadUserInfo();
}

// Автоматическое обновление каждые 30 секунд (опционально)
setInterval(loadUserInfo, 30000);