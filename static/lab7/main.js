function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function (data) {
            return data.json();
        })
        .then(function (films) {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';
            
            for(let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');
                
                let tdTitleRus = document.createElement('td');
                let tdTitle = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');
                
                tdTitleRus.innerText = films[i].title_ru;

                if (films[i].title && films[i].title !== films[i].title_ru) {
                    tdTitle.innerHTML = `<span class="original-title">${films[i].title}</span>`;
                } else {
                    tdTitle.innerHTML = '<span class="original-title">—</span>';
                }

                tdYear.innerText = films[i].year;
                
                let editButton = document.createElement('button');
                editButton.innerText = 'Редактировать';
                editButton.onclick = function() {
                    editFilm(i);
                };
                
                let delButton = document.createElement('button');
                delButton.innerText = 'Удалить';
                delButton.onclick = function() {
                    deleteFilm(i, films[i].title_ru);
                };
                
                tdActions.append(editButton);
                tdActions.append(delButton);
                
                tr.append(tdTitleRus);
                tr.append(tdTitle);
                tr.append(tdYear);
                tr.append(tdActions);
                
                tbody.append(tr);
            }
        });
}

function clearAllErrors() {
    const errorElements = document.querySelectorAll('.error-message');
    const inputElements = document.querySelectorAll('.error-border');
    
    errorElements.forEach(el => el.innerText = '');
    inputElements.forEach(el => el.classList.remove('error-border'));
}

function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }
    
    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
    .then(function () {
        fillFilmList();
    });
}


function showModal() {
    document.getElementById('film-modal').style.display = 'block';
    clearAllErrors();
}

function hideModal() {
    document.getElementById('film-modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function updateCharCount() {
    const description = document.getElementById('description');
    const charCount = document.getElementById('char-count');
    if (charCount) {
        const length = description.value.length;
        charCount.textContent = `${length}/2000`;
        if (length > 2000) {
            charCount.style.color = '#e74c3c';
        } else {
            charCount.style.color = '#666';
        }
    }
}

function addFilm() {
    document.getElementById('film-id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title_ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    updateCharCount();
    showModal();
}

function sendFilm() {
    const id = document.getElementById('film-id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title_ru').value,
        year: parseInt(document.getElementById('year').value),
        description: document.getElementById('description').value
    };

    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';
    
    clearAllErrors();

    fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        // Если есть ошибка валидации (400)
        if(resp.status === 400) {
            return resp.json();
        }
        // Для других ошибок
        return resp.text().then(text => {
            throw new Error(text || 'Unknown error');
        });
    })
    .then(function(errors) {
        if (errors && Object.keys(errors).length > 0) {
            for (const [field, message] of Object.entries(errors)) {
                const errorElement = document.getElementById(`${field}_error`);
                const inputElement = document.getElementById(field);
                
                if (errorElement) {
                    errorElement.innerText = message;
                }
                if (inputElement) {
                    inputElement.classList.add('error-border');
                }
            }
        }
    })
    .catch(function(error) {
        console.error('Ошибка при отправке данных:', error);
        alert('Произошла ошибка: ' + error.message);
    });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(function (data) {
            return data.json();
        })
        .then(function (film) {
            document.getElementById('film-id').value = id;  // Используем переданный id
            document.getElementById('title').value = film.title;
            document.getElementById('title_ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            updateCharCount();
            showModal();
        })
        .catch(function(error) {
            console.error('Ошибка при загрузке фильма:', error);
        });
}

function resetFilms() {
    if (!confirm('Восстановить оригинальный список фильмов? Все изменения будут потеряны.')) {
        return;
    }
    
    fetch('/lab7/rest-api/reset-films/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            alert('Список фильмов восстановлен!');
        }
    })
    .catch(function(error) {
        console.error('Ошибка при восстановлении:', error);
        alert('Ошибка при восстановлении списка фильмов');
    });
}