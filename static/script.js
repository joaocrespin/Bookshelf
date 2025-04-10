// Carries the preferred theme across pages

const html = document.documentElement;

// Retrieves the user's saved theme, if none retrieves dark
const savedTheme = localStorage.getItem('theme') || 'dark';
html.setAttribute('data-bs-theme', savedTheme);

const themeChanger = document.getElementById('theme-changer');
themeChanger.innerHTML = savedTheme === 'dark' ? 'Light' : 'Dark';

// Toggles between dark and light themes and saves the preference in the browser's local storage
function toggleTheme(){ 
    const currentTheme = html.getAttribute('data-bs-theme');
    if (currentTheme === 'dark'){ 
        html.setAttribute('data-bs-theme', 'light');
        localStorage.setItem('theme', 'light');
        themeChanger.innerHTML = 'Dark';
    } else { 
        html.setAttribute('data-bs-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        themeChanger.innerHTML ='Light';
    } 
 }
themeChanger.addEventListener('click', toggleTheme)