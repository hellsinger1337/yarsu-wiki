// Регистрация
document.getElementById('register-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const formData = {
        username: username,
        email: email,
        password: password
    };

    const response = await fetch('http://127.0.0.1:8000/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData),
    });

    if (response.ok) {
        console.log('Registration successful');
    } else {
        console.error('Registration failed:', await response.json());
    }
});

// Авторизация
document.getElementById('login-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch('http://127.0.0.1:8000/auth/login', {
        method: 'POST',
        body: formData,
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        console.log('Login successful');
    } else {
        console.error('Login failed:', await response.json());
    }
});

// Оценка преподавателя
document.getElementById('rate-teacher-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const teacherId = document.getElementById('teacher-id').value;
    const knowledgeRating = document.getElementById('knowledge-rating').value;
    const teachingSkillRating = document.getElementById('teaching-skill-rating').value;
    const communicationRating = document.getElementById('communication-rating').value;
    const easinessRating = document.getElementById('easiness-rating').value;

    const token = localStorage.getItem('token');

    const formData = {
        teacher_id: parseInt(teacherId),
        knowledge_rating: parseFloat(knowledgeRating),
        teaching_skill_rating: parseFloat(teachingSkillRating),
        communication_rating: parseFloat(communicationRating),
        easiness_rating: parseFloat(easinessRating)
    };

    const response = await fetch('http://127.0.0.1:8000/api/teacher-ratings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData),
    });

    if (response.ok) {
        const result = await response.json();
        console.log(result);
    } else {
        console.error('Rating failed:', await response.json());
    }
});
