const API = "/api/movies/";
const modal = document.getElementById("movieModal");

function loadMovies() {
    authFetch(API).then(data => {
        let html = "";
        data.forEach(m => {
            html += `
            <tr>
                <td>${m.title}</td>
                <td>${m.genre_name || m.genre}</td>
                <td>${m.release_year}</td>
                <td>
                    <button onclick="editMovie(${m.id}, '${m.title}', ${m.genre}, ${m.release_year})">✏️</button>
                    <button onclick="deleteMovie(${m.id})">🗑</button>
                </td>
            </tr>`;
        });
        document.getElementById("moviesTable").innerHTML = html;
    });
}

loadMovies();

function openModal() {
    modal.style.display = "block";
    document.getElementById("modalTitle").innerText = "Add Movie";
}

function closeModal() {
    modal.style.display = "none";
    document.getElementById("movieId").value = "";
    document.getElementById("title").value = "";
    document.getElementById("genre").value = "";
    document.getElementById("year").value = "";
}

function editMovie(id, title, genre, year) {
    openModal();
    document.getElementById("modalTitle").innerText = "Edit Movie";
    document.getElementById("movieId").value = id;
    document.getElementById("title").value = title;
    document.getElementById("genre").value = genre;
    document.getElementById("year").value = year;
}

function saveMovie() {
    const id = document.getElementById("movieId").value;
    const payload = {
        title: document.getElementById("title").value,
        genre: document.getElementById("genre").value,
        release_year: document.getElementById("year").value
    };

    const method = id ? "PUT" : "POST";
    const url = id ? API + id + "/" : API;

    authFetch(url, {
        method: method,
        body: JSON.stringify(payload)
    }).then(() => {
        closeModal();
        loadMovies();
    });
}

function deleteMovie(id) {
    if (!confirm("Delete this movie?")) return;

    authFetch(API + id + "/", {
        method: "DELETE"
    }).then(() => loadMovies());
}
