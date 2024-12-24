let currentPage = 1;
let jsonData = []; // Store the loaded JSON data

// Fetch Data from archive.json
function fetchTexts() {
    const searchQuery = document.getElementById('searchBar').value.toLowerCase();
    const author = document.getElementById('filterAuthor').value.toLowerCase();
    const year = document.getElementById('filterYear').value;
    const subject = document.getElementById('filterSubject').value.toLowerCase();

    fetch('textsdata/archive.json') // Adjusted path for nested structure
        .then(response => response.json())
        .then(data => {
            jsonData = data;
            filterAndDisplayTexts(searchQuery, author, year, subject);
        })
        .catch(error => {
            console.error('Error loading JSON:', error);
            document.getElementById('textsGrid').innerHTML = `<p>Error: ${error.message}</p>`;
        });
}

// Filter and Display Texts
function filterAndDisplayTexts(searchQuery, author, year, subject) {
    const grid = document.getElementById('textsGrid');
    grid.innerHTML = ''; // Clear the grid

    // Apply filters
    let filteredData = jsonData.filter(book => {
        return (
            (!searchQuery || book.title.toLowerCase().includes(searchQuery)) &&
            (!author || book.author.toLowerCase().includes(author)) &&
            (!year || String(book.year) === year) &&
            (!subject || book.subject.toLowerCase().includes(subject))
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
                    <img src="${book.thumbnail_url || 'https://via.placeholder.com/150'}" class="card-img-top" alt="${book.title}">
                    <div class="card-body">
                        <h5 class="card-title">${book.title}</h5>
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
}

// Change Page
function changePage(delta) {
    currentPage += delta;
    if (currentPage < 1) currentPage = 1;
    fetchTexts();
}

// Initial Fetch
fetchTexts();
