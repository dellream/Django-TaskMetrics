const csrftoken = Cookies.get('csrftoken');

document.addEventListener('DOMContentLoaded', (event) => {
    // DOM загружена
    const likeButton = document.querySelector('a.like');
    const url = likeButton.getAttribute('data-url');
    let options = {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin'
    }
    
    likeButton.addEventListener('click', function(e){
        e.preventDefault();
    
        // добавим тело запроса
        let formData = new FormData();
        formData.append('id', likeButton.dataset.id);
        formData.append('action', likeButton.dataset.action);
        options['body'] = formData;
    
        // отправить HTTP запрос
        fetch(url, options)
        .then(response => response.json())
        .then(data => {
            if (data['status'] === 'ok')
            {
                let previousAction = likeButton.dataset.action;
    
                // Переключаем текст кнопки и атрибут data-action
                let action = previousAction === 'like' ? 'unlike' : 'like';
                likeButton.dataset.action = action;
                likeButton.innerHTML = action;
    
                // Обновляем количество лайков
                let likeCount = document.querySelector('span.count .total');
                let totalLikes = parseInt(likeCount.textContent);
                likeCount.textContent = previousAction === 'like' ? totalLikes + 1 : totalLikes - 1;
            }
        })
    });
});
