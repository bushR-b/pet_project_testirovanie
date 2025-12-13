const loginModal = document.getElementById("login-modal");
const registerModal = document.getElementById("register-modal");

// Получаем кнопки, которые открывают modal
const loginButton = document.getElementById("login-button");
const registerButton = document.getElementById("register-button");

// Получаем элементы <span>, которые закрывают modal
const loginCloseButton = document.getElementById("login-close");
const registerCloseButton = document.getElementById("register-close");

// Когда пользователь кликает на кнопку, открываем modal
if (loginButton) {
    loginButton.onclick = function() {
        if (loginModal) loginModal.style.display = "block";
    }
}

if (registerButton) {
    registerButton.onclick = function() {
        if (registerModal) registerModal.style.display = "block";
    }
}

// Когда пользователь кликает на <span> (x), закрываем modal
if (loginCloseButton) {
    loginCloseButton.onclick = function() {
        if (loginModal) loginModal.style.display = "none";
    }
}

if (registerCloseButton) {
    registerCloseButton.onclick = function() {
        if (registerModal) registerModal.style.display = "none";
    }
}

// Когда пользователь кликает вне modal, закрываем его
window.onclick = function(event) {
    if (loginModal && event.target == loginModal) {
        loginModal.style.display = "none";
    }
    if (registerModal && event.target == registerModal) {
        registerModal.style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('RegisterForm');
    
    if (registerForm) {
        registerForm.addEventListener('submit', async function(event) {
            event.preventDefault(); 
            const data = {
                "name": document.getElementById('Registername').value,
                "surname": document.getElementById('Registerlastname').value,
                "last_name": document.getElementById('Registermiddlename').value,
                "username": document.getElementById('Registerusername').value,
                "password": document.getElementById('Registerpassword').value,
                "confirm_password": document.getElementById('Registerconfirmpassword').value
            };
            
            // Проверка совпадения паролей
            if (data.password !== data.confirm_password) {
                alert('Пароли не совпадают!');
                return;
            }
            
            try {
                const response = await fetch('/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    const result = await response.json();
                    registerForm.reset();
                    
                    // Закрываем модальное окно
                    const modal = document.getElementById('register-modal');
                    if (modal) modal.style.display = 'none';
                    
                    // Показываем сообщение об успехе
                    alert('Регистрация успешна!');
                    
                } else {
                    const error = await response.json();
                    console.error('Ошибка регистрации:', error);
                    alert('Ошибка регистрации: ' + (error.message || 'Неизвестная ошибка'));
                }
                
            } catch (error) {
                console.error('Ошибка сети:', error);
                alert('Ошибка соединения с сервером');
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('LoginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const data = {
                "username": document.getElementById('LoginUsername').value,
                "password": document.getElementById('LoginPassword').value
            };

            try {
                const response = await fetch('/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    const result = await response.json();
                    
                    // Закрываем модальное окно
                    const modal = document.getElementById('login-modal');
                    if (modal) modal.style.display = 'none';
                    
                    // Обновляем интерфейс
                    updateUIAfterLogin();
                    
                } else {
                    const error = await response.json();
                    console.error('Ошибка входа:', error);
                    alert('Ошибка входа: ' + (error.message || 'Неизвестная ошибка'));
                }
                
            } catch (error) {
                console.error('Ошибка сети:', error);
                alert('Ошибка соединения с сервером');
            }
        });
    }
});

// Функция для обновления UI после входа
function updateUIAfterLogin() {
    const authLinks = document.getElementById('auth-links');
    if (authLinks) {
        authLinks.innerHTML = '<a href="/user/me" id="user-button">Мой профиль</a> | <a href="/user/logout">Выйти</a>';
    }
}

function showAuthChoice() {
    const loginModal = document.getElementById("login-modal");
    if (loginModal) {
        loginModal.style.display = "block";
    }
}

function checkAuth() {
    // Проверяем наличие токена разными способами
    if (!document.cookie.includes('access_token=') && 
        !document.cookie.includes('my_access_token=') &&
        !localStorage.getItem('access_token')) {
        showAuthChoice();
        return false;
    }
    return true;
}

// Проверяем авторизацию при клике на тесты
document.addEventListener('DOMContentLoaded', function() {
    const keyrsiBtn = document.getElementById('start-keyrsi');
    const tomasBtn = document.getElementById('start-tomas');
    const motivBtn = document.getElementById('start-motivacionniy');
    
    if (keyrsiBtn) {
        keyrsiBtn.addEventListener('click', function(e) {
            if (!checkAuth()) {
                e.preventDefault();
            }
        });
    }
    
    if (tomasBtn) {
        tomasBtn.addEventListener('click', function(e) {
            if (!checkAuth()) {
                e.preventDefault();
            }
        });
    }
    
    if (motivBtn) {
        motivBtn.addEventListener('click', function(e) {
            if (!checkAuth()) {
                e.preventDefault();
            }
        });
    }
    
    // Проверяем авторизацию при загрузке страницы
    checkInitialAuth();
});

function checkInitialAuth() {
    // Проверяем наличие токена
    const hasToken = document.cookie.includes('my_access_token') ||
                     localStorage.getItem('my_access_token');
    
    const authLinks = document.getElementById('auth-links');
    if (!hasToken){
        fetch("/auth/refresh", {method: 'POST'})
    }
    if (hasToken && authLinks) {
        authLinks.innerHTML = '<a href="/user/me" id="user-button">Мой профиль</a> | <a href="/user/logout">Выйти</a>';
    } else if (authLinks) {
        authLinks.innerHTML = '<a href="#" id="login-button">Войти</a> | <a href="#" id="register-button">Регистрация</a>';
        
        // Перепривязываем обработчики для новых кнопок
        const loginBtn = document.getElementById('login-button');
        const registerBtn = document.getElementById('register-button');
        
        if (loginBtn) {
            loginBtn.onclick = function() {
                const modal = document.getElementById('login-modal');
                if (modal) modal.style.display = 'block';
            };
        }
        
        if (registerBtn) {
            registerBtn.onclick = function() {
                const modal = document.getElementById('register-modal');
                if (modal) modal.style.display = 'block';
            };
        }
    }
}
