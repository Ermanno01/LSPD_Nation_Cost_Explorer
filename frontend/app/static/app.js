document.addEventListener("DOMContentLoaded", function() {
    // Fetch and display the Top 10 list on page load
    fetchTop10();

    // Handle form submission for search
    document.getElementById('searchForm').addEventListener('submit', function(event) {
        event.preventDefault();
        fetchSearchResults();
    });

    // Fetch top 10 from the backend
    function fetchTop10() {
        fetch('http://localhost:8000/list/top10')
            .then(response => response.json())  // Parse the response as JSON
            .then(data => {
                console.log('Parsed Data:', data);  // Log the parsed data
                console.log('Type of data:', typeof data);
                console.log('Is data an array?', Array.isArray(data));

                let top10List = document.getElementById('top10List');
                top10List.innerHTML = '';  // Clear previous data

                // Check if data is an array before calling forEach
                if (Array.isArray(data)) {
                    data.forEach(item => {
                        let listItem = document.createElement('div');
                        listItem.textContent = `Country: ${item['Country']}, Cost of Living Plus Rent Index: ${item['Cost of Living Plus Rent Index']}`;
                        top10List.appendChild(listItem);
                    });
                } else {
                    top10List.textContent = 'Data is not an array';
                }
            })
            .catch(error => {
                console.error('Error fetching top 10:', error);
                document.getElementById('top10List').textContent = 'Error loading Top 10';
            });
    }

    // Fetch search results from the backend
    function fetchSearchResults() {
        let stateName = document.getElementById('stateInput').value;
        fetch(`http://0.0.0.0:8000/query/${stateName}`)
            .then(response => response.json())
            .then(data => {
                let searchResults = document.getElementById('searchResults');
                searchResults.innerHTML = '';  // Clear previous data
                if (data.error) {
                    searchResults.textContent = data.error;
                } else {
                    searchResults.textContent = JSON.stringify(data, null, 2);
                }
            })
            .catch(error => {
                console.error('Error fetching search results:', error);
                document.getElementById('searchResults').textContent = 'Error loading search results';
            });
    }
});
