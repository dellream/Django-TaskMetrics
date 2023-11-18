// Получаем значение courseId из HTML-элемента с идентификатором 'course-id' 
// и преобразуем его из текста в формат JSON
const courseIdElement = document.getElementById('course-id');
const courseId = JSON.parse(courseIdElement.textContent);

// Формируем URL для WebSocket-соединения, используя текущий хост и courseId
const url = `ws://${window.location.host}/ws/chat/room/${courseId}/`;

// Создаем новый объект WebSocket для установки соединения с сервером
const chatSocket = new WebSocket(url);

// Обработчик события при получении сообщения от сервера
chatSocket.onmessage = function(event) {
    // Разбираем JSON-данные из события
    const data = JSON.parse(event.data);
    
    // Получаем элемент 'chat' из HTML и добавляем новое сообщение в виде div-элемента
    const chat = document.getElementById('chat');
    chat.innerHTML += `<div class="message">${data.message}</div>`;
    
    // Прокручиваем чат вниз, чтобы видеть последнее сообщение
    chat.scrollTop = chat.scrollHeight;
};

// Обработчик события при закрытии WebSocket-соединения
chatSocket.onclose = function(event) {
    console.error('Сокет чата неожиданно закрылся');
};

// Получаем ссылки на HTML-элементы ввода и кнопки отправки
const input = document.getElementById('chat-message-input');
const submitButton = document.getElementById('chat-message-submit');

// Добавляем обработчик события при нажатии на кнопку отправки
submitButton.addEventListener('click', function(event) {
    const message = input.value;
    if (message) {
        // Отправляем сообщение на сервер в формате JSON
        chatSocket.send(JSON.stringify({ 'message': message }));
        // Очищаем поле ввода
        input.value = '';
        // Переводим фокус на поле ввода
        input.focus();
    }
});

// Добавляем обработчик события при нажатии клавиши Enter в поле ввода
input.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        // Отменяем стандартное действие, если необходимо
        event.preventDefault();
        // Запускаем событие нажатия на кнопку отправки
        submitButton.click();
    }
});

// Устанавливаем фокус на поле ввода при загрузке страницы
input.focus();
