document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');
    const successMessage = document.getElementById('success-message');

    if (!loginForm) return;

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Получаем данные формы
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;

        // Валидация
        if (!email || !password) {
            showError('Пожалуйста, заполните все поля');
            return;
        }

        // Показываем загрузку
        const submitBtn = loginForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Вход...';
        submitBtn.disabled = true;

        try {
            // Отправляем запрос на API
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Успешный вход
                showSuccess('Вход выполнен успешно!');

                // Сохраняем токен
                localStorage.setItem('token', data.token);

                // Перенаправляем на дашборд через 1.5 секунды
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1500);
            } else {
                // Ошибка входа
                showError(data.detail || 'Ошибка входа. Проверьте email и пароль.');
            }
        } catch (error) {
            console.error('Login error:', error);
            showError('Ошибка сети. Проверьте подключение к интернету.');
        } finally {
            // Восстанавливаем кнопку
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });

    // Вспомогательные функции для отображения сообщений
    function showError(message) {
        if (errorMessage) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
            errorMessage.className = 'error-message';
        }

        if (successMessage) {
            successMessage.style.display = 'none';
        }
    }

    function showSuccess(message) {
        if (successMessage) {
            successMessage.textContent = message;
            successMessage.style.display = 'block';
            successMessage.className = 'success-message';
        }

        if (errorMessage) {
            errorMessage.style.display = 'none';
        }
    }

    // Очистка сообщений при фокусе на полях
    const inputs = loginForm.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            if (errorMessage) errorMessage.style.display = 'none';
            if (successMessage) successMessage.style.display = 'none';
        });
    });
});