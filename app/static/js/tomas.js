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

document.addEventListener('DOMContentLoaded', function() {
    let currentIndex = 0;  // Индекс текущего вопроса (0, 1, 2, ...)
    let answers = "";  // Будет строка типа "1221..."
    const answersContainer = document.querySelector(".answers-container");
    const submitBtn = document.getElementById("answerBtn");
    
        function renderQuestion() {
            const q = test_data[currentIndex];
            
            // Обновляем вариант А (вопрос)
            const optionA = document.querySelector('label[for="answer_A"]');
            if (optionA) {
                optionA.textContent = q.question_text;
            }
            
            // Обновляем вариант Б (ответ)
            const optionB = document.querySelector('label[for="answer_B"]');
            if (optionB && q.answers && q.answers.length > 0) {
                optionB.textContent = q.answers[0].text;
            }
            
            // Сбрасываем выбор радиокнопок
            const radios = document.querySelectorAll('input[type="radio"]');
            radios.forEach(radio => radio.checked = false);
        }
            submitBtn.addEventListener("click", () => {
                const selected = document.querySelector('input[name="question_pair"]:checked');
        
        if (!selected) {
            alert("Пожалуйста, выберите вариант А или Б!");
            return;
        }

        // Сохраняем выбор (1 или 2)
        answers += selected.value;
        console.log("Текущие ответы:", answers);
        
        // Переходим к следующему вопросу
        currentIndex++;

        if (currentIndex >= test_data.length) {
            // Тест завершен, отправляем результаты
                const token = document.cookie.includes('my_access_token') ||
                localStorage.getItem('my_access_token');
                
                if (!token) {
                    fetch('/auth/refresh', {
                            method: 'POST',
                        });
                }
        
            fetch("/test/tomas", {
                method: "POST",
                headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`  // Добавляем Bearer токен
                },
                body: JSON.stringify({
                    answers: answers
                })
            })
            .then(data => {
                window.location.href = "/test/result?test=tomas"
            })
            .catch(error => {
                console.error("Ошибка:", error);
                alert("Произошла ошибка при отправке теста");
            });
            
            return;
        }

        renderQuestion();
    });

    // Инициализация
    renderQuestion();
});