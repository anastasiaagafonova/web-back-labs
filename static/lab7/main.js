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

function addFilm() {
    document.getElementById('film-id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title_ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

function sendFilm() {
    const id = document.getElementById('film-id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title_ru').value,
        year: document.getElementById('year').value,
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
        return resp.json();
    })
    .then(function(errors) {
        if (errors && Object.keys(errors).length > 0) {
            for (const [field, message] of Object.entries(errors)) {
                const errorElement = document.getElementById(`${field}_error`);
                const inputElement = document.getElementById(field);
                
                if (errorElement && inputElement) {
                    errorElement.innerText = message;
                    inputElement.classList.add('error-border');
                }
            }
        }
    })
    .catch(function(error) {
        console.error('Ошибка при отправке данных:', error);
    });
}


function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(function (data) {
            return data.json();
        })
        .then(function (film) {
            document.getElementById('film-id').value = film.id;
            document.getElementById('title').value = film.title;
            document.getElementById('title_ru').value = film.title_ru;  // Добавьте заполнение этого поля
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            showModal();
        })
        .catch(function(error) {
            console.error('Ошибка при загрузке фильма:', error);
        });
}