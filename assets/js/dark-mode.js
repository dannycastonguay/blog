// Dark mode toggle functionality
(function() {
  // Check for saved theme preference
  const theme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', theme);

  // Create toggle button
  const toggle = document.createElement('button');
  toggle.className = 'theme-toggle';
  toggle.innerHTML = theme === 'dark' ? '☀️' : '🌙';
  toggle.setAttribute('aria-label', 'Toggle dark mode');
  
  // Add click handler
  toggle.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    toggle.innerHTML = newTheme === 'dark' ? '☀️' : '🌙';
  });

  // Add to page
  const header = document.querySelector('.masthead');
  if (header) {
    header.appendChild(toggle);
  }
})(); 