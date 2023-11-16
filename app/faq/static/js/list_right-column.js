// Обработчик события клика на ссылке
function handleLinkClick(event) {
  event.preventDefault();

  // Получаем ссылку, на которую кликнули
  const link = event.currentTarget;

  // Получаем URL страницы из атрибута href
  const url = link.getAttribute('href');

  // Создаем новый объект XMLHttpRequest
  const xhr = new XMLHttpRequest();

  // Устанавливаем обработчик события загрузки
  xhr.onload = function () {
    if (xhr.status === 200) {
      // Создаем временный контейнер для полученного контента
      const tempContainer = document.createElement('div');
      tempContainer.innerHTML = xhr.responseText;

      // Извлекаем только нужный элемент контента
      const detailElement = tempContainer.querySelector('.detail');

      // Обновляем контейнер для контента страницы с полученными данными
      pageContentContainer.innerHTML = '';
      pageContentContainer.appendChild(detailElement);

      // Убираем класс active у всех ссылок
      links.forEach((link) => link.classList.remove('active'));

      // Добавляем класс active к активной ссылке
      link.classList.add('active');

      // Повторно привязываем обработчики событий к элементам на странице, включая форму "collapsible"
      initializeCollapsible();
    } else {
      // Обработка ошибки, если запрос не удался
      console.error('Ошибка загрузки контента страницы:', xhr.status);
    }
  };

  // Устанавливаем метод запроса и URL
  xhr.open('GET', url);

  // Отправляем запрос на сервер
  xhr.send();
}

// Функция для инициализации форм "collapsible" ------------------------------------------------------------------------
function initializeCollapsible() {
  let coll = document.getElementsByClassName("collapsible");
  let i;

  for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
      this.classList.toggle("active");
      let content = this.nextElementSibling;
      if (content.style.display === "block") {
        content.style.display = "none";
      } else {
        content.style.display = "block";
      }
    });
  }
}

// Получаем ссылки и контейнер для контента страницы
const links = document.querySelectorAll('.content__left-col__list-single a');
const pageContentContainer = document.querySelector('.content__right-col__main');

// Назначаем обработчик события клика на каждую ссылку
links.forEach((link) => {
  link.addEventListener('click', handleLinkClick);
});

// Инициализируем формы "collapsible"
initializeCollapsible();

//------------------------------------------------------------------------------------------------

// // Создаем HTML-разметку для нового комментария
// function createCommentaryHTML(commentary) {
//   const commentElement = document.createElement('div');
//   commentElement.classList.add('detail__lowbody__commentary');

//   const authorElement = document.createElement('p');
//   authorElement.classList.add('detail__lowbody__commentary-author');
//   authorElement.textContent = `${commentary.name} / ${commentary.created}`;

//   const bodyElement = document.createElement('p');
//   bodyElement.classList.add('detail__lowbody__commentary-body');
//   bodyElement.textContent = commentary.body;

//   commentElement.appendChild(authorElement);
//   commentElement.appendChild(bodyElement);

//   return commentElement;
// }

// // Обработчик события клика на ссылке
// function handleLinkClick(event) {
//   event.preventDefault();

//   // Получаем ссылку, на которую кликнули
//   const link = event.currentTarget;

//   // Получаем URL страницы из атрибута href
//   const url = link.getAttribute('href');

//   // Создаем новый объект XMLHttpRequest
//   const xhr = new XMLHttpRequest();

//   // Устанавливаем обработчик события загрузки
//   xhr.onload = function () {
//     if (xhr.status === 200) {
//       const response = JSON.parse(xhr.responseText);
//       if (response.success) {
//         // Создаем HTML-разметку для нового комментария
//         const newCommentElement = createCommentaryHTML(response.commentary);

//         // Находим контейнер для комментариев
//         const commentsContainer = document.querySelector('.comments-container');

//         // Добавляем новый комментарий в контейнер
//         commentsContainer.appendChild(newCommentElement);
//       } else {
//         // Обработка ошибки, если сервер вернул неуспешный результат
//         console.error('Ошибка загрузки контента страницы:', response.error);
//       }
//     } else {
//       // Обработка ошибки, если запрос не удался
//       console.error('Ошибка загрузки контента страницы:', xhr.status);
//     }
//   };

//   // Устанавливаем метод запроса и URL
//   xhr.open('GET', url);

//   // Отправляем запрос на сервер
//   xhr.send();
// }


// // Функция для инициализации форм "collapsible"
// function initializeCollapsible() {
//   let coll = document.getElementsByClassName("collapsible");
//   let i;

//   for (i = 0; i < coll.length; i++) {
//     coll[i].addEventListener("click", function() {
//       this.classList.toggle("active");
//       let content = this.nextElementSibling;
//       if (content.style.display === "block") {
//         content.style.display = "none";
//       } else {
//         content.style.display = "block";
//       }
//     });
//   }
// }

// // Получаем ссылки и контейнер для контента страницы
// const links = document.querySelectorAll('.content__left-col__list-single a');
// const pageContentContainer = document.querySelector('.content__right-col__main');

// // Назначаем обработчик события клика на каждую ссылку
// links.forEach((link) => {
//   link.addEventListener('click', handleLinkClick);
// });

// // Инициализируем формы "collapsible"
// initializeCollapsible();
