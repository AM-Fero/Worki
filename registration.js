function openCity(evt, cityName, id) {
    // Объявляем все переменные
    var i, tabcontent, tablinks;
    document.getElementById("message").textContent = '';
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => input.value = '');
    // Получаем все элементы с class="tabcontent" и скрываем их
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Получаем все элементы с class="tablinks" и удаляем класс "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Показываем текущую вкладку и добавляем класс "active" к кнопке, которая открыла вкладку
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";

    if (id == 1) {
        document.getElementById(1).style.backgroundColor = 'rgba(57, 54, 73, 1)';
        document.getElementById(1).style.color = 'white'
        document.getElementById(2).style.backgroundColor = "white";
        document.getElementById(2).style.color = 'rgba(57, 54, 73, 1)';
    }
    else {
        document.getElementById(1).style.backgroundColor = 'white';
        document.getElementById(1).style.color = 'rgba(57, 54, 73, 1)';
        document.getElementById(2).style.backgroundColor = "rgba(57, 54, 73, 1)";
        document.getElementById(2).style.color = 'white';
    }
}
// Включаем JavaScript код отсюда выше
document.getElementById('registrationForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = {
        login: document.getElementById('login').value,
        password: document.getElementById('password').value,
        name: document.getElementById('name').value,
        fullName: document.getElementById('fullName').value
    };

    const submitButton = event.target.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    const messageDiv = document.getElementById('message');

    // Показываем состояние загрузки
    submitButton.textContent = 'Регистрация...';
    submitButton.disabled = true;
    messageDiv.textContent = '';
    messageDiv.className = '';

    try {
        const response = await fetch('http://localhost:5002/api/worki-auth/company-registration', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
            credentials: 'include'
        });

        const data = await response.json();

        if (response.ok) {
            messageDiv.textContent = 'Успешно!';
            messageDiv.className = 'success';
            event.target.reset();
            window.location.href = "success.html";
        } else {
            messageDiv.textContent = 'Error: ' + data.error;
            messageDiv.className = 'error';
        }

    } catch (error) {
        messageDiv.textContent = 'Network error: ' + error.message;
        messageDiv.className = 'error';
    } finally {
        submitButton.textContent = originalText;
        submitButton.disabled = false;
    }
});

document.getElementById('registrationForm2').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = {
        login: document.getElementById('uniemail').value,
        password: document.getElementById('unipassword').value,
        name: document.getElementById('uniname').value,
        fullName: document.getElementById('unifullName').value
    };

    const submitButton = event.target.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    const messageDiv = document.getElementById('message');

    // Показываем состояние загрузки
    submitButton.textContent = 'Регистрация...';
    submitButton.disabled = true;
    messageDiv.textContent = '';
    messageDiv.className = '';

    try {
        const response = await fetch('http://localhost:5002/api/worki-auth/uni-registration', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
            credentials: 'include'
        });

        const data = await response.json();

        if (response.ok) {
            messageDiv.textContent = 'Успешно!';
            messageDiv.className = 'success';
            event.target.reset();
            window.location.href = "success.html";
        } else {
            messageDiv.textContent = 'Error: ' + data.error;
            messageDiv.className = 'error';
        }
    } catch (error) {
        messageDiv.textContent = 'Network error: ' + error.message;
        messageDiv.className = 'error';
    } finally {
        submitButton.textContent = originalText;
        submitButton.disabled = false;
    }
});