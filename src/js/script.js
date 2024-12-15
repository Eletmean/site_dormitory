// Находим бургер-меню и навигационное меню
const burger = document.querySelector('.burger');
const nav = document.querySelector('.nav');
const head = document.querySelector('.head');

// Добавляем обработчик событий для открытия и закрытия меню
burger.addEventListener('click', function() {
    nav.classList.toggle('active'); // Показываем или скрываем меню
    this.classList.toggle('active'); // Меняем вид бургера на крестик
    head.classList.toggle('no-rectangle'); // Скрываем прямоугольник слева при открытии меню
});

// Плавный скроллинг для всех ссылок в меню
document.querySelectorAll('.nav-item, .nav-items').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();  // Отменяем стандартное поведение ссылки
        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);

        // Проверяем, что элемент существует, и плавно скроллим к нему
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',  // Плавный скроллинг
                block: 'start'       // Начинаем скроллинг от начала элемента
            });
        }

        // Закрываем меню после выбора пункта
        nav.classList.remove('active');
        burger.classList.remove('active');
        head.classList.remove('no-rectangle'); // Возвращаем прямоугольник после закрытия меню
    });
});

let currentPosition = 0;
const imageWidth = 320; // Ширина изображения + отступ (300px + 20px)

function scrollLeft() {
    const gallery = document.querySelector('.gallery');
    currentPosition = Math.max(currentPosition - imageWidth * 3, 0); // Ограничение влево
    gallery.style.transform = `translateX(-${currentPosition}px)`;
}

function scrollRight() {
    const gallery = document.querySelector('.gallery');
    const maxScroll = imageWidth * (gallery.children.length - 3); // Ограничение вправо
    currentPosition = Math.min(currentPosition + imageWidth * 3, maxScroll);
    gallery.style.transform = `translateX(-${currentPosition}px)`;
}

const leftBtn = document.querySelector('.left-btn');
const rightBtn = document.querySelector('.right-btn');

leftBtn.addEventListener('click', scrollLeft);
rightBtn.addEventListener('click', scrollRight);