let currentPage = 1;

// Fetch Texts from the API
function fetchTexts() {
    const searchQuery = document.getElementById('searchBar').value;
    const author = document.getElementById('filterAuthor').value;
    const year = document.getElementById('filterYear').value;
    const subject = document.getElementById('filterSubject').value;

    const apiUrl = `http://127.0.0.1:5000/texts?page=${currentPage}&limit=9`
        + (searchQuery ? `&title=${encodeURIComponent(searchQuery)}` : '')
        + (author ? `&author=${encodeURIComponent(author)}` : '')
        + (year ? `&year=${encodeURIComponent(year)}` : '')
        + (subject ? `&subject=${encodeURIComponent(subject)}` : '');

    console.log("Fetching API URL:", apiUrl); // Log API URL for debugging

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("API Response:", data); // Log data for debugging
            const grid = document.getElementById('textsGrid');
            grid.innerHTML = ''; // Clear the grid

            if (!data.results || data.results.length === 0) {
                grid.innerHTML = '<p>No results found.</p>';
                return;
            }

            // Populate Grid
            data.results.forEach(book => {
                grid.innerHTML += `
                    <div class="col">
                        <div class="card h-100">
                            <img src="${book.thumbnail_url || 'https://via.placeholder.com/150'}" class="card-img-top" alt="${book.title || 'No Title'}">
                            <div class="card-body">
                                <h5 class="card-title">${book.title || 'Untitled'}</h5>
                                <p class="card-text"><strong>Author:</strong> ${book.author || 'Unknown'}</p>
                                <p class="card-text"><strong>Year:</strong> ${book.year || 'N/A'}</p>
                                <p class="card-text"><strong>Language:</strong> ${book.language || 'N/A'}</p>
                                <p class="card-text"><strong>Subject:</strong> ${book.subject || 'N/A'}</p>
                                <a href="${book.read_url}" class="btn btn-primary btn-sm" target="_blank">Read</a>
                                <a href="${book.download_url}" class="btn btn-secondary btn-sm" target="_blank">Download</a>
                            </div>
                        </div>
                    </div>
                `;
            });

            // Update Pagination Indicator
            document.getElementById('pageIndicator').innerText = `Page ${currentPage}`;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            document.getElementById('textsGrid').innerHTML = `<p>Error: ${error.message}</p>`;
        });
}

// Change Page
function changePage(delta) {
    currentPage += delta;
    if (currentPage < 1) currentPage = 1;
    fetchTexts();
}

// Initial Fetch
fetchTexts();
