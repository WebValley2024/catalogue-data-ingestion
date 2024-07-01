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
}

document.addEventListener('DOMContentLoaded', function () {
    window.alert = (function() {
        var nativeAlert = window.alert;
        return function(message) {
            window.alert = nativeAlert;
            message.indexOf("DataTables warning") === 0 ?
                console.warn(message) :
                nativeAlert(message);
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
        let startDate = document.getElementById('startDate').value;
        let endDate = document.getElementById('endDate').value;

        if (startDate === '' || endDate === '') {
            showAlert('Please select a valid date range', 'danger');
            return;
        }

        console.log('Start Date: ' + startDate);
        console.log('End Date: ' + endDate);

        // fetch data from the server
        // TODO
        // simulate data fetch json very small or very big randomly
        let data = Math.random() > 0.5 ? 'small' : 'big';
        if (data === 'small') {
            data = JSON.stringify({'data': 'small data'});
        } else {
            data = JSON.stringify({'data': 'big data'.repeat(1000)});
        }

        // check if length of data is very big to avoid crashing the browser or the computer itself
        // if it is, show an alert to the user
        if (data.length > 1000) {
            if (!confirm('The data you are trying to fetch is very big and may crash your browser. Do you want to continue?')) {
                return;
            }
        }

        showAlert('Date range applied', 'success');
    });

    findFilters();

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
        });
    });

    fetch('/spadeapp/select_earthquake/')
        .then(response => response.text())
        .then(data => {
            // EQ
            let EQ = document.getElementById('earthquakeTable').querySelector('div table');
            EQ.innerHTML = data;
            $('#earthquakeTable div table').DataTable({
                "scrollX": true, // Enable horizontal scrolling
                "autoWidth": false // Disable automatic column width calculation
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });

    fetch('/spadeapp/select_swe/')
        .then(response => response.text())
        .then(data => {
            // SWE
            let SWE = document.getElementById('sweTable').querySelector('div table');
            SWE.innerHTML = data;
            $('#sweTable div table').DataTable({
                "scrollX": true, // Enable horizontal scrolling
                "autoWidth": false // Disable automatic column width calculation
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });

    fetch('/spadeapp/select_tgf/')
        .then(response => response.text())
        .then(data => {
            // TGF
            let TGF = document.getElementById('tgfTable').querySelector('div table');
            TGF.innerHTML = data;
            $('#tgfTable div table').DataTable({
                "scrollX": true, // Enable horizontal scrolling
                "autoWidth": false // Disable automatic column width calculation
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

// Global array to store the state of each table's columns
let tableColumnsState = {};

function findFilters() {
    const activeTab = document.querySelector('.nav-link.active');
    const tabName = activeTab.textContent.trim();
    const filterOffcanvas = document.getElementById('filterOffcanvas').querySelector('.offcanvas-body');
    const table = document.querySelector(activeTab.getAttribute('data-bs-target'));
    const tableHeaders = table.querySelectorAll('th');

    // Check if the table's state has already been stored
    if (!tableColumnsState[tabName]) {
        // Initialize the state for this table
        tableColumnsState[tabName] = Array.from(tableHeaders).map((header, index) => ({
            index,
            name: header.textContent.trim(),
            shown: !header.classList.contains('d-none')
        }));
    }

    // Clear existing filters from the offcanvas
    while (filterOffcanvas.firstChild) {
        filterOffcanvas.removeChild(filterOffcanvas.firstChild);
    }

    // Create a document fragment to temporarily hold the filters
    let docFragment = document.createDocumentFragment();

    // Add the tab name to the offcanvas
    const tabNameElement = document.createElement('h5');
    tabNameElement.style.fontWeight = 'bold';
    tabNameElement.textContent = tabName;
    docFragment.appendChild(tabNameElement);

    // Use the stored state to create checkboxes
    tableColumnsState[tabName].forEach(column => {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = column.name;
        checkbox.checked = column.shown;

        const label = document.createElement('label');
        label.htmlFor = column.name;
        label.textContent = column.name;

        docFragment.appendChild(checkbox);
        docFragment.appendChild(document.createTextNode(' '));
        docFragment.appendChild(label);
        docFragment.appendChild(document.createElement('br'));

        // Add event listener to show/hide columns
        checkbox.addEventListener('change', function() {
            // Update the visibility in the table and the stored state
            const header = tableHeaders[column.index];
            if (checkbox.checked) {
                header.classList.remove('d-none');
            } else {
                header.classList.add('d-none');
            }
            column.shown = checkbox.checked;
        });
    });

    // Append the filters to the offcanvas
    filterOffcanvas.appendChild(docFragment);
}

function showHideColumn(columnName, shown) {
    const table = document.querySelector('.tab-pane.active');
    const tableHeaders = table.querySelectorAll('th');
    const tableRows = table.querySelectorAll('tr');

    // use datatables plugin (the table already exists)
    let tableObj = $('#sweTable div table').DataTable();

    // Find the index of the column
    let columnIndex = -1;
    tableHeaders.forEach((header, index) => {
        if (header.textContent === columnName) {
            columnIndex = index;
        }
    });

    // Show/hide the column
    if (shown) {
        tableObj.column(columnIndex).visible(true);
    } else {
        tableObj.column(columnIndex).visible(false);
    }

    findFilters();
}

function showAlert(message, alertType) {
    const alertContainer = document.getElementById('alert-container');

    alertContainer.style.setProperty('padding-bottom', '15px', 'important');

    // Remove any existing alerts
    while (alertContainer.firstChild) {
        alertContainer.removeChild(alertContainer.firstChild);
    }

    alertContainer.style.setProperty('display', 'block', 'important');

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
    }, 2500);
}