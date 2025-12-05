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