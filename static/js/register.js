document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('register-form');
    const errorMessage = document.getElementById('error-message');
    const successMessage = document.getElementById('success-message');

    if (registerForm) {
        registerForm.onsubmit = async function(e) {
            e.preventDefault();

            const formData = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
                first_name: document.getElementById('first_name').value || null,
                last_name: document.getElementById('last_name').value || null,
                nick_name: document.getElementById('nick_name').value || null
            };

            try {
                const response = await fetch('/user', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(formData)
                });

                if (response.ok) {
                    const data = await response.json();
                    errorMessage.style.display = 'none';
                    successMessage.style.display = 'block';
                    successMessage.textContent = 'Registration successful! User ID: ' + data.user_id;
                    registerForm.reset();

                    setTimeout(() => {
                        window.location.href = '/login';
                    }, 2000);
                } else {
                    const errorData = await response.json();
                    successMessage.style.display = 'none';
                    errorMessage.style.display = 'block';
                    errorMessage.textContent = errorData.detail || 'Registration failed';
                }
            } catch (error) {
                errorMessage.style.display = 'block';
                errorMessage.textContent = 'Network error';
            }
        };
    }
});