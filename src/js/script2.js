console.log("JS файл подключен!");
document.addEventListener('DOMContentLoaded', function() {
    const leftBtn = document.querySelector('.left-btn');
    const rightBtn = document.querySelector('.right-btn');

    leftBtn.addEventListener('click', scrollLeft);
    rightBtn.addEventListener('click', scrollRight);
});
const leftBtn = document.querySelector('.left-btn');
const rightBtn = document.querySelector('.right-btn');

if (leftBtn && rightBtn) {
    leftBtn.addEventListener('click', scrollLeft);
    rightBtn.addEventListener('click', scrollRight);
} else {
    console.error('Кнопки не найдены!');
}
