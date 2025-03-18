let currentPage = 1;
let jsonData = []; // Store the loaded JSON data

// Fetch Data from minimal_urdu_texts.json
function fetchTexts() {
    const searchQuery = document.getElementById('searchBar').value.toLowerCase();
    const year = document.getElementById('filterYear').value;

    fetch('urdu_texts_with_authors.json')
        .then(response => response.json())
        .then(data => {
            jsonData = data;
            filterAndDisplayTexts(searchQuery, year);
        })
        .catch(error => {
            console.error('Error loading JSON:', error);
            document.getElementById('textsGrid').innerHTML = `<p>Error: ${error.message}</p>`;
        });
}

// Filter and Display Texts
function filterAndDisplayTexts(searchQuery, year) {
    const grid = document.getElementById('textsGrid');
    grid.innerHTML = ''; // Clear the grid

    // Apply filters
    let filteredData = jsonData.filter(book => {
        return (
            (!searchQuery || book.title.toLowerCase().includes(searchQuery)) &&
            (!year || book.year === year)
        );
    });

    // Implement Pagination
    const itemsPerPage = 9;
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedData = filteredData.slice(startIndex, endIndex);

    if (paginatedData.length === 0) {
        grid.innerHTML = '<p>No results found.</p>';
        return;
    }

    // Display books
    paginatedData.forEach(book => {
        grid.innerHTML += `
            <div class="col">
                <div class="card h-100">
                    <img src="${book.thumbnail_url}" class="card-img-top" alt="${book.title}">
                    <div class="card-body">
                        <h5 class="card-title">${book.title}</h5>
                        <p><strong>Year:</strong> ${book.year || 'Unknown'}</p>
                        <a href="${book.read_url}" class="btn btn-primary btn-sm" target="_blank">Read</a>
                        <a href="${book.download_url}" class="btn btn-secondary btn-sm" target="_blank">Download</a>
                    </div>
                </div>
            </div>
        `;
    });

    // Update Pagination Indicator
    document.getElementById('pageIndicator').innerText = `Page ${currentPage}`;
}

// Change Page
function changePage(delta) {
    currentPage += delta;
    if (currentPage < 1) currentPage = 1;
    fetchTexts();
}

// Initial Fetch
fetchTexts();
