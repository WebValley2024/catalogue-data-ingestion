/*!
 * Theme Toggler
 * Toggles between light and dark theme
 * Based on Bootstrap 5.3 color mode toggler (https://getbootstrap.com/docs/5.3/customize/color-modes/#javascript)
 */

function updateThemeSelection(theme) {
    // Remove 'active' class from all dropdown items
    document.querySelectorAll('.dropdown-item').forEach(item => {
        item.classList.remove('active');
    });

    // Add 'active' class to the selected theme
    let selectedTheme = document.getElementById(`${theme}_theme`);
    if (selectedTheme) {
        selectedTheme.classList.add('active');

        // Update the icon in the dropdown button
        let currentThemeIcon = document.getElementById('currentThemeIcon');
        currentThemeIcon.className = selectedTheme.querySelector('i').className;
    }
}

const getStoredTheme = () => localStorage.getItem('theme')
const setStoredTheme = theme => localStorage.setItem('theme', theme)

const getPreferredTheme = () => {
    const storedTheme = getStoredTheme()
    if (storedTheme) {
        return storedTheme
    }

    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

const getPreferredThemeNotAuto = () => {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

const setTheme = theme => {
    if (theme === 'auto') {
        document.documentElement.setAttribute('data-bs-theme', (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'))
        setStoredTheme('auto')
    } else {
        document.documentElement.setAttribute('data-bs-theme', theme)
        setStoredTheme(theme)
    }
}

const getCurrentTheme = () => document.documentElement.getAttribute('data-bs-theme')

setTheme(getPreferredTheme())

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    const storedTheme = getStoredTheme()
    if (storedTheme !== 'light' && storedTheme !== 'dark') {
        setTheme(getPreferredTheme())
        updateThemeSelection(getPreferredTheme())
    }
    document.dispatchEvent(new Event('themeChange'))
})

document.addEventListener('DOMContentLoaded', () => {
    try {
        document.getElementById('auto_theme').addEventListener('click', () => {
            setTheme('auto');
            updateThemeSelection('auto');
            document.dispatchEvent(new Event('themeChange'));
        });
        document.getElementById('light_theme').addEventListener('click', () => {
            setTheme('light');
            updateThemeSelection('light');
            document.dispatchEvent(new Event('themeChange'));
        });
        document.getElementById('dark_theme').addEventListener('click', () => {
            setTheme('dark');
            updateThemeSelection('dark');
            document.dispatchEvent(new Event('themeChange'));
        });
    } catch (e) {
        console.error('Error adding event listeners to theme toggler buttons:', e);
    }
});

// create an event sender so that the main page can listen to the event
const event = new Event('themeChange');
document.addEventListener('DOMContentLoaded', () => {
    document.dispatchEvent(event);
});
document.addEventListener('themeChange', () => {
    window.parent.postMessage({ theme: getCurrentTheme() }, '*');
});