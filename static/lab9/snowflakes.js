// Добавьте этот скрипт в конец body
document.addEventListener('DOMContentLoaded', function() {
    // Создаем снежинки
    const snowflakesContainer = document.createElement('div');
    snowflakesContainer.className = 'snowflakes';
    document.body.prepend(snowflakesContainer);
    
    for (let i = 0; i < 50; i++) {
        const snowflake = document.createElement('div');
        snowflake.className = 'snowflake';
        
        // Случайный размер
        const size = Math.random() * 8 + 3;
        snowflake.style.width = `${size}px`;
        snowflake.style.height = `${size}px`;
        
        // Случайная позиция
        snowflake.style.left = `${Math.random() * 100}%`;
        snowflake.style.top = `${Math.random() * -100}px`;
        
        // Случайная прозрачность
        snowflake.style.opacity = Math.random() * 0.5 + 0.3;
        
        // Случайная скорость падения
        const duration = Math.random() * 4 + 2;
        snowflake.style.animationDuration = `${duration}s`;
        
        // Случайная задержка
        snowflake.style.animationDelay = `${Math.random() * 5}s`;
        
        snowflakesContainer.appendChild(snowflake);
    }
});