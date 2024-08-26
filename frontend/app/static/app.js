document.addEventListener("DOMContentLoaded", function() {

    const backend = "http://localhost:8085";
    // Fetch and display the Top 10 list on page load
    fetchTop10();

    // Handle form submission for search
    document.getElementById('searchForm').addEventListener('submit', function(event) {
        event.preventDefault();
        fetchSearchResults();
    });

    // Autocomplete functionality
    addAutocomplete('stateInput');
    addAutocomplete('compInput1');
    addAutocomplete('compInput2');

    function addAutocomplete(inputId) {
        let inputElement = document.getElementById(inputId);

        inputElement.addEventListener('input', function() {
            let query = this.value.trim().toLowerCase();
            if (query.length > 0) {
                fetch(`${backend}/autocomplete?query=${query}`)
                    .then(response => response.json())
                    .then(suggestions => {
                        // Filter suggestions to only those that start with the query and limit to 5
                        let filteredSuggestions = suggestions.filter(s => s.toLowerCase().startsWith(query)).slice(0, 5);

                        // Clear existing datalist options
                        let dataList = document.getElementById(`${inputId}-datalist`);
                        if (!dataList) {
                            dataList = document.createElement('datalist');
                            dataList.id = `${inputId}-datalist`;
                            inputElement.setAttribute('list', dataList.id);
                            document.body.appendChild(dataList);
                        }
                        dataList.innerHTML = '';

                        // Add filtered suggestions to the datalist
                        filteredSuggestions.forEach(suggestion => {
                            let option = document.createElement('option');
                            option.value = suggestion;
                            dataList.appendChild(option);
                        });
                    })
                    .catch(error => {
                        console.error('Error fetching autocomplete suggestions:', error);
                    });
            }
        });
    }

    // Fetch top 10 from the backend
    function fetchTop10() {
        fetch(`${backend}/list/top10`)
            .then(response => response.json())
            .then(data => {
                let top10List = document.getElementById('top10List');
                top10List.innerHTML = '';  // Clear previous data

                if (Array.isArray(data)) {
                    data.forEach(item => {
                        let listItem = document.createElement('tr');
                        let countryCell = document.createElement('td');
                        countryCell.textContent = item['Country'];
                        listItem.appendChild(countryCell);

                        let indexCell = document.createElement('td');
                        indexCell.textContent = item['Cost of Living Plus Rent Index'];
                        listItem.appendChild(indexCell);

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
        fetch(`${backend}/query/${stateName}`)
            .then(response => response.json())
            .then(data => {
                let searchResults = document.getElementById('searchResults');
                searchResults.innerHTML = '';  // Clear previous data

                if (data.error) {
                    searchResults.textContent = data.error;
                } else {
                    let table = document.createElement('table');
                    table.className = 'table table-bordered';

                    for (const [key, value] of Object.entries(data[0])) {
                        let row = document.createElement('tr');
                        let keyCell = document.createElement('td');
                        keyCell.textContent = key;
                        row.appendChild(keyCell);

                        let valueCell = document.createElement('td');
                        valueCell.textContent = value;
                        row.appendChild(valueCell);

                        table.appendChild(row);
                    }

                    searchResults.appendChild(table);
                }
            })
            .catch(error => {
                console.error('Error fetching search results:', error);
                document.getElementById('searchResults').textContent = 'Error loading search results';
            });
    }

    // Handle comparison button click
    document.getElementById('vsButton').addEventListener('click', function() {
        let state1 = document.getElementById('compInput1').value;
        let state2 = document.getElementById('compInput2').value;

        if (state1 && state2) {
            Promise.all([
                fetch(`${backend}/query/${state1}`),
                fetch(`${backend}/query/${state2}`)
            ])
            .then(responses => Promise.all(responses.map(response => response.json())))
            .then(([data1, data2]) => {
                let stateData1 = document.getElementById('stateData1');
                let stateData2 = document.getElementById('stateData2');
                stateData1.innerHTML = '';  // Clear previous data
                stateData2.innerHTML = '';  // Clear previous data

                if (data1.error) {
                    stateData1.textContent = data1.error;
                } else {
                    let table = document.createElement('table');
                    table.className = 'table table-bordered';

                    for (const [key, value] of Object.entries(data1[0])) {
                        let row = document.createElement('tr');
                        let keyCell = document.createElement('td');
                        keyCell.textContent = key;
                        row.appendChild(keyCell);

                        let valueCell = document.createElement('td');
                        valueCell.textContent = value;
                        row.appendChild(valueCell);

                        table.appendChild(row);
                    }

                    stateData1.appendChild(table);
                }

                if (data2.error) {
                    stateData2.textContent = data2.error;
                } else {
                    let table = document.createElement('table');
                    table.className = 'table table-bordered';

                    for (const [key, value] of Object.entries(data2[0])) {
                        let row = document.createElement('tr');
                        let keyCell = document.createElement('td');
                        keyCell.textContent = key;
                        row.appendChild(keyCell);

                        let valueCell = document.createElement('td');
                        valueCell.textContent = value;
                        row.appendChild(valueCell);

                        table.appendChild(row);
                    }

                    stateData2.appendChild(table);
                }
            })
            .catch(error => {
                console.error('Error fetching comparison results:', error);
                document.getElementById('stateData1').textContent = 'Error loading comparison results';
                document.getElementById('stateData2').textContent = 'Error loading comparison results';
            });
        } else {
            alert('Please select both states to compare.');
        }
    });

});
