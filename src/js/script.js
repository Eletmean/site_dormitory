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
