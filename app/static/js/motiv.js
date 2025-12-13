function refreshToken() {
    return fetch('/auth/refresh', {
        method: 'POST',
    })
        .then((res) => {
            if (res.status === 200) {
                const tokenData = res.json();
                
                return Promise.resolve();
            }
            return Promise.reject();
        });
}
const hasToken = document.cookie.includes('my_access_token') ||
                    localStorage.getItem('my_access_token');
const hasRefreshToken = document.cookie.includes('my_refresh_token') ||
                    localStorage.getItem('my_refresh_token');

if (!hasToken){
    if (hasRefreshToken){
        refreshToken()
    }
}

let currentIndex = 0;
let answers = ""
const questionCard = document.querySelector(".question-card p");
const answersContainer = document.querySelector(".answers-container");
const submitBtn = document.getElementById("answerBtn");

function renderQuestion() {
    const q = test_data[currentIndex];

    questionCard.textContent = q.question_text;

    const oldOptions = answersContainer.querySelectorAll(".answer-option");
    oldOptions.forEach(opt => opt.remove());

    q.answers.forEach(a => {
        const div = document.createElement("div");
        div.classList.add("answer-option");

        div.innerHTML = `
            <input type="radio" id="answer_${a.id}" name="question_${q.question_id}" value="${a.id}">
            <label for="answer_${a.id}">${a.text}</label>
        `;

        answersContainer.insertBefore(div, submitBtn);
    });
}

submitBtn.addEventListener("click", () => {
    const selected = document.querySelector('input[type="radio"]:checked');
    if (!selected) {
        return;
    }

    const answerIndex = Array.from(
        document.querySelectorAll(".answer-option input")
    ).indexOf(selected) + 1;

    answers += answerIndex;
    currentIndex++;

    if (currentIndex >= test_data.length) {
        const token = document.cookie.includes('my_access_token') ||
                     localStorage.getItem('my_access_token');
        
        if (!token) {
            fetch('/auth/refresh', {
                    method: 'POST',
                });
        }
        
        
        fetch("/test/motivacionniy", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`  // Добавляем Bearer токен
            },
            body: JSON.stringify({
                answers: answers
            })
        })
        .then(response => {
            if (response.status === 401) {
                // Токен истек или невалиден
                alert("Сессия истекла. Пожалуйста, войдите снова.");
                window.location.href = "/auth/login";
                return;
            }
            return response.json();
        })
        .then(data => {
            window.location.href = "/test/result?test=motivacionniy"
        })
        .catch(error => {
            console.error("Ошибка:", error);
        });
        
    }

    renderQuestion();
});

renderQuestion();