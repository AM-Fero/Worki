function openCity(evt, cityName, id) {
    // Declare all variables
    var i, tabcontent, tablinks;
    document.getElementById("message").textContent = '';
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => input.value = '');
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
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

document.getElementById('registrationForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = {
        login: document.getElementById('login').value,
        password: document.getElementById('password').value,
    };

    const submitButton = event.target.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    const messageDiv = document.getElementById('message');

    // Show loading state
    submitButton.textContent = 'Вход...';
    submitButton.disabled = true;
    messageDiv.textContent = '';
    messageDiv.className = '';

    try {
        const response = await fetch('http://localhost:5002/api/worki-auth/company-worker-login', {
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
    };

    const submitButton = event.target.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    const messageDiv = document.getElementById('message');

    // Show loading state
    submitButton.textContent = 'Вход...';
    submitButton.disabled = true;
    messageDiv.textContent = '';
    messageDiv.className = '';

    try {
        const response = await fetch('http://localhost:5002/api/worki-auth/uni-login', {
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