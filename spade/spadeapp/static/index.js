const tablesOptions = {
    "scrollX": true, // Enable horizontal scrolling
    "autoWidth": true, // Disable automatic column width calculation
    "retrieve": true,
    "pageLength": 50,
    "sorting": false,
    "lengthMenu": [10, 25, 50, 100, 250, 500, { label: 'All', value: -1 }],
    "initComplete": function () {
        // call the findFilters function to update the filters
        findFilters();

        // Apply the checkbox state to the columns
        const activeTab = document.querySelector('.nav-link.active');
        const tabName = activeTab.textContent.trim();
        const tableSelector = activeTab.getAttribute('data-bs-target') + ' div table';
        // check if the table has been initialized
        if (!$.fn.dataTable.isDataTable(tableSelector)) {
            return;
        }
        const table = $(tableSelector).DataTable({
            "retrieve": true,
            "responsive": true,
        });

        if (!tableColumnsState[tabName]) {
            return;
        }

        try {
            tableColumnsState[tabName].forEach(column => {
                table.column(column.index).visible(column.shown);
            });
        }
        catch (error) {
            console.error('Error applying the columns state:', error);
        }

        
    },
    "layout": {
        "topStart": {
            "paging": true,
            "pageLength": true,
            "info": true,
        },
        "topEnd": {
            "search": true,
            "buttons": [
                {
                    extend: 'excelHtml5',
                    text: '<i class="bi bi-file-earmark-bar-graph-fill"></i> XLSX',
                    filename: 'SpaDe_Data',
                },
                {
                    extend: 'csvHtml5',
                    text: '<i class="bi bi-file-earmark-spreadsheet-fill"></i> CSV',
                    filename: 'SpaDe_Data',
                },
                {
                    extend: 'print',
                    text: '<i class="bi bi-printer-fill"></i> Print',
                    filename: 'SpaDe_Data',
                },
            ],
        },
    },
};

function fixNav() {
    let navHeight = document.querySelector('#supBar').offsetHeight;
    let navbar = document.querySelector('.navbar').offsetHeight;

    if (document.getElementById('alert-container').childElementCount === 0) {
        document.getElementById('alert-container').style.marginTop = (navbar-15) + 'px';
    }

    document.getElementById('dateSelectorBox').style.marginTop = (navHeight+10) + 'px';
}

function autoDateSelector() {
    let startDate = new Date();
    let endDate = new Date();

    startDate.setMonth(startDate.getMonth() - 1);
    startDate.setHours(0, 0, 0, 0);
    endDate.setHours(23, 59, 59, 999);
    
    // set the date in the date selector
    document.getElementById('startDate').valueAsDate = startDate;
    document.getElementById('endDate').valueAsDate = endDate;
}

function updateTimePeriod(timePeriod) {
    let startDate = new Date();
    let endDate = new Date();

    switch (timePeriod) {
        case '7g':
            startDate.setDate(startDate.getDate() - 7);
            break;
        case '14g':
            startDate.setDate(startDate.getDate() - 14);
            break;
        case '1m':
            startDate.setMonth(startDate.getMonth() - 1);
            break;
        case '3m':
            startDate.setMonth(startDate.getMonth() - 3);
            break;
        case '6m':
            startDate.setMonth(startDate.getMonth() - 6);
            break;
        case '1y':
            startDate.setFullYear(startDate.getFullYear() - 1);
            break;
        case '2y':
            startDate.setFullYear(startDate.getFullYear() - 2);
            break;
        case '3y':
            startDate.setFullYear(startDate.getFullYear() - 3);
            break;
        case '4y':
            startDate.setFullYear(startDate.getFullYear() - 4);
            break;
        case '5y':
            startDate.setFullYear(startDate.getFullYear() - 5);
            break;
        case '10y':
            startDate.setFullYear(startDate.getFullYear() - 10);
            break;
    }

    document.getElementById('startDate').valueAsDate = startDate;
    document.getElementById('endDate').valueAsDate = endDate;

    document.getElementById('applyDateRange').click();
}

// Function to enable page elements and show a message
function enablePage(message, messageType, loadingModal, checkData) {
    document.getElementById('applyDateRange').disabled = false;
    document.getElementById('applyDateRange').textContent = 'Apply Date Range';
    document.getElementById('dateRangeDropdown').disabled = false;
    document.getElementById('startDate').disabled = false;
    document.getElementById('endDate').disabled = false;
    showAlert(message, messageType); // Show success or error message
    loadingModal.hide();
    clearInterval(checkData); // Clear the data checking interval
}

function loadData() {
    let startDate = document.getElementById('startDate').value;
    let endDate = document.getElementById('endDate').value;

    // List of conditions to check before applying the date range
    const conditions = [
        startDate === '',
        endDate === '',
        startDate === null,
        endDate === null,
        new Date(startDate) > new Date(endDate),
        new Date(startDate) < new Date(1900, 1, 1),
        new Date(endDate) < new Date(1900, 1, 1),
    ];

    if (conditions.some(Boolean)) {
        showAlert('Please select a valid date range', 'danger');
        return;
    }
    console.log('Start Date: ' + startDate);
    console.log('End Date: ' + endDate);

    // disable the button to prevent multiple clicks
    document.getElementById('applyDateRange').disabled = true;
    document.getElementById('applyDateRange').textContent = 'Loading...';
    document.getElementById('dateRangeDropdown').parentNode.querySelector('.dropdown-menu').classList.remove('show');
    document.getElementById('dateRangeDropdown').disabled = true;
    document.getElementById('startDate').disabled = true;
    document.getElementById('endDate').disabled = true;

    // clear the tables
    document.getElementById('earthquakeTable').querySelector('div table').innerHTML = '';
    document.getElementById('sweTable').querySelector('div table').innerHTML = '';
    document.getElementById('tgfTable').querySelector('div table').innerHTML = '';
    document.getElementById('grbTable').querySelector('div table').innerHTML = '';
    document.getElementById('dstTable').querySelector('div table').innerHTML = '';
    
    // initialize the tables with datatables
    $('#earthquakeTable div table').DataTable(tablesOptions);
    $('#sweTable div table').DataTable(tablesOptions);
    $('#tgfTable div table').DataTable(tablesOptions);
    $('#grbTable div table').DataTable(tablesOptions);
    $('#dstTable div table').DataTable(tablesOptions);

    // show the loading modal
    let loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    loadingModal.show();

    let isEverythingLoaded = [false, false, false, false, false];

    let myBeautifulURL = '/spadeapp/select_earthquake/?start=' + startDate + '&end=' + endDate;
    fetch(myBeautifulURL)
        .then(response => response.text())
        .then(data => {
            $('#earthquakeTable div table').DataTable().destroy();
            // EQ
            let EQ = document.getElementById('earthquakeTable').querySelector('div table');
            // Check if the data contains a debug message (generated by Django's debug mode)
            if (data.includes('DEBUG')) {
                showAlert(data, 'danger');
            }

            let rowCount = 0;

            // Check if the table has a lot of rows and show a warning before continuing
            // it's an HTML table, so we can count the number of rows
            try {
                rowCount = data.split('<tr').length - 1;
            } catch (error) {
                rowCount = 0;
            }

            if (rowCount > 2000) {
                let confirmResult = confirm('The earthquake table contains ' + rowCount + ' rows. Are you sure you want to continue?');
                if (confirmResult) {
                    EQ.innerHTML = data;
                } else {
                    showAlert('Not loading Earthquake data', 'warning');
                    EQ.innerHTML = '';
                }
            } else if (rowCount < 2) {
                EQ.innerHTML = '';
            } else {
                EQ.innerHTML = data;
            }
            // Initialize the DataTable
            $('#earthquakeTable div table').DataTable(tablesOptions);
            isEverythingLoaded[0] = true;
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error loading Earthquake data', 'danger');
            isEverythingLoaded[0] = true;
        });

    myBeautifulURL = '/spadeapp/select_swe/?start=' + startDate + '&end=' + endDate;
    fetch(myBeautifulURL)
        .then(response => response.text())
        .then(data => {
            $('#sweTable div table').DataTable().destroy();
            // SWE
            let SWE = document.getElementById('sweTable').querySelector('div table');
            // Check if the data contains a debug message (generated by Django's debug mode)
            if (data.includes('DEBUG')) {
                showAlert(data, 'danger');
            }
            // Check if the table has a lot of rows and show a warning before continuing
            // it's an HTML table, so we can count the number of rows
            try {
                rowCount = data.split('<tr').length - 1;
            } catch (error) {
                rowCount = 0;
            }

            if (rowCount > 2000) {
                let confirmResult = confirm('The Space Weather Events table contains ' + rowCount + ' rows. Are you sure you want to continue?');
                if (confirmResult) {
                    SWE.innerHTML = data;
                } else {
                    showAlert('Not loading SWE data', 'warning');
                    SWE.innerHTML = '';
                }
            } else if (rowCount < 2) {
                SWE.innerHTML = '';
            } else {
                SWE.innerHTML = data;
            }
            // Initialize the DataTable
            $('#sweTable div table').DataTable(tablesOptions);
            isEverythingLoaded[1] = true;
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error loading SWE data', 'danger');
            isEverythingLoaded[1] = true;
        });

    myBeautifulURL = '/spadeapp/select_tgf/?start=' + startDate + '&end=' + endDate;
    fetch(myBeautifulURL)
        .then(response => response.text())
        .then(data => {
            $('#tgfTable div table').DataTable().destroy();
            // TGF
            let TGF = document.getElementById('tgfTable').querySelector('div table');
            // Check if the data contains a debug message (generated by Django's debug mode)
            if (data.includes('DEBUG')) {
                showAlert(data, 'danger');
            }
            // Check if the table has a lot of rows and show a warning before continuing
            // it's an HTML table, so we can count the number of rows
            try {
                rowCount = data.split('<tr').length - 1;
            } catch (error) {
                rowCount = 0;
            }

            if (rowCount > 2000) {
                let confirmResult = confirm('The TGF table contains ' + rowCount + ' rows. Are you sure you want to continue?');
                if (confirmResult) {
                    TGF.innerHTML = data;
                } else {
                    showAlert('Not loading TGF data', 'warning');
                    TGF.innerHTML = '';
                }
            } else if (rowCount < 2) {
                TGF.innerHTML = '';
            } else {
                TGF.innerHTML = data;
            }
            // Initialize the DataTable
            $('#tgfTable div table').DataTable(tablesOptions);
            isEverythingLoaded[2] = true;
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error loading TGF data', 'danger');
            isEverythingLoaded[2] = true;
        });

    myBeautifulURL = '/spadeapp/select_grb/?start=' + startDate + '&end=' + endDate;
    fetch(myBeautifulURL)
        .then(response => response.text())
        .then(data => {
            $('#grbTable div table').DataTable().destroy();
            // GRB
            let GRB = document.getElementById('grbTable').querySelector('div table');
            // Check if the data contains a debug message (generated by Django's debug mode)
            if (data.includes('DEBUG')) {
                showAlert(data, 'danger');
            }
            // Check if the table has a lot of rows and show a warning before continuing
            // it's an HTML table, so we can count the number of rows
            try {
                rowCount = data.split('<tr').length - 1;
            } catch (error) {
                rowCount = 0;
            }

            if (rowCount > 2000) {
                let confirmResult = confirm('The GRB table contains ' + rowCount + ' rows. Are you sure you want to continue?');
                if (confirmResult) {
                    GRB.innerHTML = data;
                } else {
                    showAlert('Not loading GRB data', 'warning');
                    GRB.innerHTML = '';
                }
            } else if (rowCount < 2) {
                GRB.innerHTML = '';
            } else {
                GRB.innerHTML = data;
            }
            
            // Initialize the DataTable
            $('#grbTable div table').DataTable(tablesOptions);
            isEverythingLoaded[3] = true;
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error loading GRB data', 'danger');
            isEverythingLoaded[3] = true;
        });

    myBeautifulURL = '/spadeapp/select_gms/?start=' + startDate + '&end=' + endDate;
    fetch(myBeautifulURL)
        .then(response => response.text())
        .then(data => {
            $('#dstTable div table').DataTable().destroy();
            // Magnetic disturbances (Dst)
            let DST = document.getElementById('dstTable').querySelector('div table');
            // Check if the data contains a debug message (generated by Django's debug mode)
            if (data.includes('DEBUG')) {
                showAlert(data, 'danger');
            }
            // Check if the table has a lot of rows and show a warning before continuing
            // it's an HTML table, so we can count the number of rows
            try {
                rowCount = data.split('<tr').length - 1;
            } catch (error) {
                rowCount = 0;
            }

            if (rowCount > 10000) {
                let confirmResult = confirm('The Magnetic disturbances (Dst) table contains ' + rowCount + ' rows. Are you sure you want to continue?');
                if (confirmResult) {
                    DST.innerHTML = data;
                }
            } else if (rowCount < 2) {
                DST.innerHTML = '';
            } else {
                DST.innerHTML = data;
            }
            // Initialize the DataTable
            $('#dstTable div table').DataTable(tablesOptions);
            isEverythingLoaded[4] = true;
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error loading Magnetic disturbances (Dst) data', 'danger');
            isEverythingLoaded[4] = true;
        });

    // Interval to check if all data has been loaded
    let checkData = setInterval(function() {
        if (isEverythingLoaded.every(Boolean)) {
            enablePage('Data loaded successfully', 'success', loadingModal, checkData);
        }
    }, 1000);

    // Timeout to stop waiting and enable the page after a certain time
    let timeoutDuration = 120000; // 120 seconds
    setTimeout(function() {
        if (!isEverythingLoaded.every(Boolean)) {
            enablePage('Could not load all data, please try again later', 'danger', loadingModal, checkData);
        }
    }, timeoutDuration);
}

document.addEventListener('DOMContentLoaded', function () {
    window.alert = (function() {
        var nativeAlert = window.alert;
        return function(message) {
            window.alert = nativeAlert;
            message.indexOf("DataTables warning") === 0 ?
                console.warn(message) :
                nativeAlert(message);
            showAlert(message, 'danger');
        }
    })();

    updateThemeSelection(getStoredTheme());

    window.addEventListener('resize', fixNav);
    fixNav();

    const navbarNav = document.getElementById('navbarNav');
    if (navbarNav) {
        navbarNav.addEventListener('shown.bs.collapse', fixNav);
        navbarNav.addEventListener('hidden.bs.collapse', fixNav);
    }

    autoDateSelector();

    document.getElementById('quickRange7g').addEventListener('click', function() {
        updateTimePeriod('7g');
    });

    document.getElementById('quickRange14g').addEventListener('click', function() {
        updateTimePeriod('14g');
    });

    document.getElementById('quickRange1m').addEventListener('click', function() {
        updateTimePeriod('1m');
    });

    document.getElementById('quickRange3m').addEventListener('click', function() {
        updateTimePeriod('3m');
    });

    document.getElementById('quickRange6m').addEventListener('click', function() {
        updateTimePeriod('6m');
    });

    document.getElementById('quickRange1y').addEventListener('click', function() {
        updateTimePeriod('1y');
    });

    document.getElementById('quickRange2y').addEventListener('click', function() {
        updateTimePeriod('2y');
    });

    document.getElementById('quickRange3y').addEventListener('click', function() {
        updateTimePeriod('3y');
    });

    document.getElementById('quickRange4y').addEventListener('click', function() {
        updateTimePeriod('4y');
    });

    document.getElementById('quickRange5y').addEventListener('click', function() {
        updateTimePeriod('5y');
    });

    document.getElementById('quickRange10y').addEventListener('click', function() {
        updateTimePeriod('10y');
    });

    document.getElementById('applyDateRange').addEventListener('click', function() {
        loadData();
    });

    document.getElementById('openFilters').addEventListener('click', function(e) {
        findFilters();
    });

    document.getElementById('openContacts').addEventListener('click', function() {
        let contactsModal = new bootstrap.Modal(document.getElementById('contactsModal'));
        contactsModal.show();
    });
    
    document.getElementById('openCatalogue').addEventListener('click', function() {
        let catalogueModal = new bootstrap.Modal(document.getElementById('catalogueModal'));
        catalogueModal.show();
    });

    document.getElementById('downloadPDF').addEventListener('click', function() {
        // open the pdf in a new tab
        window.open(downloadPDFURL, '_blank');
    });

    // Add event listener to the tabs to update the filters
    const tabs = document.querySelectorAll('.nav-link');
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const filterOffcanvas = document.getElementById('filterOffcanvas').querySelector('.offcanvas-body');

            // Remove any existing filters
            while (filterOffcanvas.firstChild) {
                filterOffcanvas.removeChild(filterOffcanvas.firstChild);
            }

            findFilters();

            // update the columns width of the datatable
            $(tab.getAttribute('data-bs-target') + ' div table').DataTable().columns.adjust().draw();
        });
    });

    loadData();

    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"], [data-bs-toggle="offcanvas"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
});

// Global array to store the state of each table's columns
let tableColumnsState = {};

function findFilters() {
    const activeTab = document.querySelector('.nav-link.active');
    const tabName = activeTab.textContent.trim();
    const filterOffcanvas = document.getElementById('filterOffcanvas').querySelector('.offcanvas-body');
    // Assuming activeTab.getAttribute('data-bs-target') gives you the ID of the container holding the table
    const tableSelector = activeTab.getAttribute('data-bs-target') + ' div table';
    // Assuming tableSelector is defined and targets your table
    if (!$.fn.dataTable.isDataTable(tableSelector)) {
        return;
    }
    // Retrieve the DataTable instance
    const table = $(tableSelector).DataTable({
        "retrieve": true,
        "responsive": true,
    });

    if (table.columns().header().toArray().length === 0) {
        // find all the checkboxes and disable them
        const checkboxes = filterOffcanvas.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.disabled = true;
        });
        // disable the select all button
        const toggleAllButton = document.getElementById('toggleAllButton');
        if (toggleAllButton) {
            toggleAllButton.disabled = true;
        }
        return;
    } else {
        // find all the checkboxes and enable them
        const checkboxes = filterOffcanvas.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.disabled = false;
        });
        // enable the select all button
        const toggleAllButton = document.getElementById('toggleAllButton');
        if (toggleAllButton) {
            toggleAllButton.disabled = false;
        }
    }

    // Initialize or clear the state for this table
    if (!tableColumnsState[tabName]) {
        tableColumnsState[tabName] = table.columns().header().toArray().map((header, index) => ({
            index,
            name: header.textContent.trim(),
            shown: table.column(index).visible()
        }));
    } else if (tableColumnsState[tabName].length === 0) {
        console.log('No columns found in the table:', tabName);
        console.log('Reinitializing the state for the table:', tabName);

        // If the table has no columns, reinitialize the state
        tableColumnsState[tabName] = table.columns().header().toArray().map((header, index) => ({
            index,
            name: header.textContent.trim(),
            shown: table.column(index).visible()
        }));

        console.log(table);
        console.log('Table columns state:', tableColumnsState[tabName]);
    } else {
        // Clear existing filters from the offcanvas to prevent duplicates
        while (filterOffcanvas.firstChild) {
            filterOffcanvas.removeChild(filterOffcanvas.firstChild);
        }
    }

    const headers = table.columns().header().toArray();
    // Select the modal by its ID
    const catalogueModal = document.getElementById('catalogueModal');
    // Select all tables within the modal
    const tables = catalogueModal.querySelectorAll('table');

    headers.forEach(header => {
        header.setAttribute('data-bs-toggle', 'tooltip');
        header.setAttribute('data-bs-placement', 'top');
        // Initialize headerDescription as an empty string
        let headerDescription = '';
        // Iterate over each table
        tables.forEach(table => {
            const catalogueRows = table.querySelectorAll('tr');
            const headerText = header.textContent.trim();
            // Iterate over each row in the current table
            catalogueRows.forEach(row => {
                if (row.cells[0].textContent.trim() === headerText) {
                    headerDescription = row.cells[1].textContent.trim();
                    // Check if the description contains "10−7erg/cm2"
                    if (headerDescription.includes("10−7erg/cm2")) {
                        // Perform the desired operation here
                        headerDescription = headerDescription.replace("10−7erg/cm2", "10^{-7} erg/cm^2");
                    }
                }
            });
        });
        // Set the title to the corresponding description from the catalogue table
        header.setAttribute('data-bs-title', headerDescription);
    });

    try{
        $('[data-bs-toggle="tooltip"]').tooltip();
    } catch (error) {
        console.warn('Error initializing tooltips:', error);
    }

    let docFragment = document.createDocumentFragment();

    const toggleAllButton = document.createElement('button');
    toggleAllButton.className = 'btn btn-outline-primary mb-3';
    toggleAllButton.id = 'toggleAllButton';
    toggleAllButton.textContent = 'Select All';
    toggleAllButton.style.marginTop = '-10px';

    const checkedCount = tableColumnsState[tabName].filter(column => column.shown).length;
    const shouldSelectAll = checkedCount < tableColumnsState[tabName].length / 2;
    toggleAllButton.textContent = shouldSelectAll ? 'Select All' : 'Deselect All';

    // Append the button to the document fragment
    docFragment.appendChild(toggleAllButton);

    const tabNameElement = document.createElement('h5');
    tabNameElement.style.fontWeight = 'bold';
    tabNameElement.textContent = tabName;
    docFragment.appendChild(tabNameElement);

    tableColumnsState[tabName].forEach(column => {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = column.name;
        checkbox.checked = column.shown;
        checkbox.classList.add('form-check-input');

        const label = document.createElement('label');
        label.htmlFor = column.name;
        label.textContent = column.name;

        docFragment.appendChild(checkbox);
        docFragment.appendChild(document.createTextNode(' '));
        docFragment.appendChild(label);
        docFragment.appendChild(document.createElement('br'));

        checkbox.addEventListener('change', function() {
            // Toggle visibility using DataTables API
            const currentVisibility = table.column(column.index).visible();
            table.column(column.index).visible(!currentVisibility);
            column.shown = !currentVisibility;
            const toggleAllButton = document.getElementById('toggleAllButton');
            if (toggleAllButton) {
                const checkedCount = tableColumnsState[tabName].filter(column => column.shown).length;
                const shouldSelectAll = checkedCount < tableColumnsState[tabName].length / 2;
                toggleAllButton.textContent = shouldSelectAll ? 'Select All' : 'Deselect All';
            }
        });
    });

    toggleAllButton.addEventListener('click', function() {
        const newState = toggleAllButton.textContent === 'Select All';
        // check if the table has columns
        if (table.columns().header().toArray().length === 0) {
            return;
        }

        tableColumnsState[tabName].forEach(column => {
            const checkbox = document.getElementById(column.name);
            checkbox.checked = newState;
            table.column(column.index).visible(newState);
            column.shown = newState;
        });
        toggleAllButton.textContent = newState ? 'Deselect All' : 'Select All';
    });

    filterOffcanvas.appendChild(docFragment);
}

function showAlert(message, alertType) {
    const alertContainer = document.getElementById('alert-container');

    alertContainer.style.setProperty('padding-bottom', '15px', 'important');

    alertContainer.style.setProperty('display', 'block', 'important');

    // remove style attributes from message
    // Parse the message as HTML
    const parser = new DOMParser();
    const doc = parser.parseFromString(message, 'text/html');
    // Remove style attributes from all elements
    doc.querySelectorAll('[style]').forEach(el => el.removeAttribute('style'));
    // Serialize back to a string
    message = new XMLSerializer().serializeToString(doc.body).replace(/<\/?body>/g, '');    

    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${alertType} alert-dismissible fade show`;
    alertElement.role = 'alert';
    alertElement.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Chiudi"></button>
                `;
    alertContainer.appendChild(alertElement);

    const bsAlert = new bootstrap.Alert(alertElement);

    alertElement.addEventListener('closed.bs.alert', function () {
        if (alertContainer.childElementCount === 0) {
            alertContainer.style.setProperty('padding-bottom', '0', 'important');
            alertContainer.style.setProperty('display', 'none', 'important');
        }
    });

    setTimeout(function () {
        bsAlert.close();
    }, 7500);
}