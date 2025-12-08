document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('register-form');
    const errorMessage = document.getElementById('error-message');
    const successMessage = document.getElementById('success-message');

    if (!registerForm) return;

    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Получаем данные формы
        const formData = {
            email: document.getElementById('email').value.trim(),
            password: document.getElementById('password').value,
            first_name: document.getElementById('first_name')?.value.trim() || null,
            last_name: document.getElementById('last_name')?.value.trim() || null,
            nick_name: document.getElementById('nick_name')?.value.trim() || null
        };

        // Валидация
        if (!formData.email || !formData.password) {
            showError('Email и пароль обязательны для заполнения');
            return;
        }

        if (formData.password.length < 6) {
            showError('Пароль должен содержать минимум 6 символов');
            return;
        }

        // Показываем загрузку
        const submitBtn = registerForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Регистрация...';
        submitBtn.disabled = true;

        try {
            // Отправляем запрос на API
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                // Успешная регистрация
                showSuccess('Регистрация прошла успешно! Токен создан.');

                // Сохраняем токен (можно сразу войти)
                localStorage.setItem('token', data.token);

                // Перенаправляем на дашборд через 2 секунды
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 2000);
            } else {
                // Ошибка регистрации
                showError(data.detail || 'Ошибка регистрации. Попробуйте другой email.');
            }
        } catch (error) {
            console.error('Registration error:', error);
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
    const inputs = registerForm.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            if (errorMessage) errorMessage.style.display = 'none';
            if (successMessage) successMessage.style.display = 'none';
        });
    });

    // Проверка сложности пароля
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            const strengthIndicator = document.getElementById('password-strength');

            if (strengthIndicator) {
                let strength = 'слабый';
                let color = 'red';

                if (password.length >= 8 && /[A-Z]/.test(password) && /[0-9]/.test(password)) {
                    strength = 'сильный';
                    color = 'green';
                } else if (password.length >= 6) {
                    strength = 'средний';
                    color = 'orange';
                }

                strengthIndicator.textContent = `Надёжность пароля: ${strength}`;
                strengthIndicator.style.color = color;
            }
        });
    }
});