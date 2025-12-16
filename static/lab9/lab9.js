document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('giftModal');
    const closeBtn = document.querySelector('.close-btn');
    const resetBtn = document.getElementById('resetBtn');
    
    // Создаем снежинки для новогодней атмосферы
    createSnowflakes();
    
    // Обработка клика по подарку
    document.querySelectorAll('.gift-box').forEach(box => {
        box.addEventListener('click', function() {
            const giftId = this.dataset.giftId;
            const isOpened = this.dataset.opened === 'true';
            const requiresAuth = this.dataset.requiresAuth === '1';
            
            if (isOpened) {
                showMessage('Этот подарок уже открыт!', 'info');
                return;
            }
            
            if (requiresAuth && !document.querySelector('.logout-btn')) {
                showMessage('Этот подарок доступен только авторизованным пользователям!', 'warning');
                return;
            }
            
            openGift(giftId);
        });
    });
    
    // Открытие подарка через AJAX
    function openGift(giftId) {
        fetch('/lab9/open_gift', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ gift_id: giftId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showMessage(data.error, 'error');
            } else {
                showGiftContent(data);
                updateStats(data.available_gifts);
                markGiftAsOpened(giftId);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Произошла ошибка при открытии подарка', 'error');
        });
    }
    
    // Показать содержимое подарка
    function showGiftContent(data) {
        const modalBody = document.getElementById('modalBody');
        modalBody.innerHTML = `
            <div class="gift-content">
                <h2>🎁 С Новым Годом! 🎁</h2>
                <div class="gift-message">
                    "${data.message}"
                </div>
                <img src="/static/lab9/images/${data.gift_image}" 
                     alt="Новогодний подарок" 
                     onerror="this.src='/static/lab9/images/gift_default.jpg'">
                <p style="margin-top: 20px; color: #ffd700; font-weight: bold;">
                    Вы получили новогодний подарок!
                </p>
            </div>
        `;
        modal.style.display = 'block';
        
        // Добавляем новогодний звук (опционально)
        playNewYearSound();
    }
    
    // Обновить статистику
    function updateStats(availableGifts) {
        const statElement = document.getElementById('availableGifts');
        if (statElement) {
            statElement.textContent = availableGifts;
            
            // Анимация обновления
            statElement.style.transform = 'scale(1.3)';
            setTimeout(() => {
                statElement.style.transform = 'scale(1)';
            }, 300);
        }
    }
    
    // Отметить подарок как открытый
    function markGiftAsOpened(giftId) {
        const giftBox = document.querySelector(`[data-gift-id="${giftId}"]`);
        if (giftBox) {
            giftBox.dataset.opened = 'true';
            giftBox.innerHTML = `
                <div class="gift-opened">
                    <img src="/static/lab9/images/box_opened.jpg" 
                         alt="Открытая коробка" 
                         class="gift-img">
                    <span class="gift-label">Открыто</span>
                </div>
            `;
            
            // Анимация открытия
            giftBox.style.animation = 'giftOpen 0.5s ease-out';
        }
    }
    
    // Кнопка "Дед Мороз"
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            if (confirm('🎅 Дед Мороз наполняет все коробки снова!\nХотите продолжить?')) {
                fetch('/lab9/reset_gifts', {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showMessage('Все коробки наполнены заново!', 'success');
                        setTimeout(() => {
                            location.reload();
                        }, 1500);
                    } else {
                        showMessage('Ошибка при сбросе подарков', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showMessage('Произошла ошибка', 'error');
                });
            }
        });
    }
    
    // Закрыть модальное окно
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Вспомогательные функции
    function showMessage(text, type = 'info') {
        const message = document.createElement('div');
        message.className = `message-${type}`;
        message.textContent = text;
        message.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 10px;
            color: white;
            font-weight: bold;
            z-index: 1001;
            animation: slideIn 0.3s ease-out;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        `;
        
        if (type === 'error') {
            message.style.background = 'linear-gradient(135deg, #c41e3a, #a81830)';
            message.style.border = '2px solid #ffd700';
        } else if (type === 'success') {
            message.style.background = 'linear-gradient(135deg, #1a472a, #0d2818)';
            message.style.border = '2px solid #ffd700';
        } else if (type === 'warning') {
            message.style.background = 'linear-gradient(135deg, #ff9800, #f57c00)';
            message.style.border = '2px solid #ffd700';
        } else {
            message.style.background = 'linear-gradient(135deg, #2196F3, #1976D2)';
            message.style.border = '2px solid #ffd700';
        }
        
        document.body.appendChild(message);
        
        setTimeout(() => {
            message.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => document.body.removeChild(message), 300);
        }, 3000);
    }
    
    function createSnowflakes() {
        const snowflakesCount = 50;
        
        for (let i = 0; i < snowflakesCount; i++) {
            const snowflake = document.createElement('div');
            snowflake.className = 'snowflake';
            
            const size = Math.random() * 5 + 2;
            const left = Math.random() * 100;
            const duration = Math.random() * 5 + 5;
            const delay = Math.random() * 5;
            
            snowflake.style.cssText = `
                width: ${size}px;
                height: ${size}px;
                left: ${left}vw;
                animation-duration: ${duration}s;
                animation-delay: ${delay}s;
                opacity: ${Math.random() * 0.5 + 0.3};
            `;
            
            document.body.appendChild(snowflake);
        }
    }
    
    function playNewYearSound() {
        // Опционально: можно добавить звук открытия подарка
        // Для этого нужен звуковой файл в static/lab9/sounds/
        try {
            const audio = new Audio('/static/lab9/sounds/gift_open.mp3');
            audio.volume = 0.3;
            audio.play().catch(e => console.log('Audio play failed:', e));
        } catch (e) {
            console.log('Sound not available');
        }
    }
    
    // Добавляем CSS анимации
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
        
        @keyframes giftOpen {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.2) rotate(10deg);
            }
            100% {
                transform: scale(1);
            }
        }
    `;
    document.head.appendChild(style);
});