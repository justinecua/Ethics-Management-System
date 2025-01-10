

let toggleTheme = document.getElementById('Appearance-Btn');

toggleTheme.addEventListener('click', async () => {

  const body = document.documentElement;
  const currentTheme = localStorage.getItem('theme');
  if (currentTheme === 'dark') {
    body.setAttribute('data-theme', 'light');
    localStorage.setItem('theme', 'light');
  } else {
    body.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
  }

})



