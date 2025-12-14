function openGift(giftId) {
    const giftBox = document.querySelector(`.gift-box[data-id="${giftId}"]`);
    const requireAuth = giftBox.getAttribute('data-require-auth') === 'True' || 
                        giftBox.getAttribute('data-require-auth') === 'true' || 
                        giftBox.getAttribute('data-require-auth') === '1';
    
    if (giftBox.classList.contains('opened')) {
        showMessage('Этот подарок уже открыт!', 'warning');
        return;
    }
    
    if (giftBox.classList.contains('locked')) {
        showMessage('Стань нашим Эльфом, чтоб отккрыть все подарки!', 'warning');
        return;
    }
    
    fetch('/lab9/open_gift', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ gift_id: giftId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('opened-count').textContent = data.opened_count;
            document.getElementById('remaining-count').textContent = data.remaining;
            
            updateGiftBox(giftId, data.message, data.image);
            giftBox.classList.add('opened');
            
            showMessage(`🎉 Вы открыли подарок!`, 'success');
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Ошибка при открытии подарка', 'error');
    });
}

function updateGiftBox(giftId, message, image) {
    const giftBox = document.querySelector(`.gift-box[data-id="${giftId}"]`);
    
    const content = `
        <div class="opened-gift">
            <div class="congratulation">
                <p>${message}</p>
            </div>
            <img src="/static/lab9/${image}" alt="Подарок" class="gift-inside">
        </div>
    `;
    
    giftBox.innerHTML = content;
    giftBox.style.cursor = 'default';
}

function showMessage(text, type) {
    const messageArea = document.getElementById('message-area');
    messageArea.textContent = text;
    messageArea.style.display = 'block';
    
    switch(type) {
        case 'success':
            messageArea.style.borderColor = '#4caf50';
            messageArea.style.color = '#2e7d32';
            messageArea.style.backgroundColor = 'rgba(76, 175, 80, 0.1)';
            break;
        case 'error':
            messageArea.style.borderColor = '#f44336';
            messageArea.style.color = '#d32f2f';
            messageArea.style.backgroundColor = 'rgba(244, 67, 54, 0.1)';
            break;
        case 'warning':
            messageArea.style.borderColor = '#ff9800';
            messageArea.style.color = '#f57c00';
            messageArea.style.backgroundColor = 'rgba(255, 152, 0, 0.1)';
            break;
    }
    
    setTimeout(() => {
        messageArea.style.display = 'none';
    }, 5000);
}

function resetGifts() {
    if (confirm('Вы уверены, что хотите сбросить все подарки? Дедушка Мороз наполнит их снова!')) {
        console.log("Отправка запроса на сброс подарков...");
        
        fetch('/lab9/santa', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            console.log("Получен ответ:", response.status, response.statusText);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Данные ответа:", data);
            if (data.success) {
                showMessage(data.message, 'success');
                setTimeout(() => {
                    location.reload();
                }, 1500);
            } else {
                showMessage(data.message, 'error');
                console.error("Ошибка от сервера:", data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Ошибка при сбросе подарков: ' + error.message, 'error');
        });
    }
}