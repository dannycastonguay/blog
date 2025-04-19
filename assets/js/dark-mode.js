// Dark mode toggle functionality
document.addEventListener('DOMContentLoaded', function() {
  // Check for saved theme preference
  const theme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', theme);

  // Create toggle switch container
  const toggleContainer = document.createElement('div');
  toggleContainer.className = 'theme-toggle-container';
  
  // Create the switch
  const toggleSwitch = document.createElement('div');
  toggleSwitch.className = 'theme-toggle-switch';
  toggleSwitch.setAttribute('aria-label', 'Toggle dark mode');
  toggleSwitch.setAttribute('role', 'button');
  toggleSwitch.setAttribute('tabindex', '0');
  
  // Add the minimal toggle
  toggleSwitch.innerHTML = `
    <svg class="moon-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
    </svg>
    <div class="theme-toggle-track">
      <div class="theme-toggle-knob ${theme === 'dark' ? '' : 'active'}"></div>
    </div>
    <svg class="sun-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <circle cx="12" cy="12" r="5"></circle>
      <line x1="12" y1="1" x2="12" y2="3"></line>
      <line x1="12" y1="21" x2="12" y2="23"></line>
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
      <line x1="1" y1="12" x2="3" y2="12"></line>
      <line x1="21" y1="12" x2="23" y2="12"></line>
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
    </svg>
  `;
  
  toggleContainer.appendChild(toggleSwitch);
  
  // Add click handler
  toggleSwitch.addEventListener('click', function() {
    toggleTheme();
  });
  
  // Add keyboard handler for accessibility
  toggleSwitch.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      toggleTheme();
    }
  });
  
  function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update toggle appearance
    const knob = toggleSwitch.querySelector('.theme-toggle-knob');
    if (newTheme === 'dark') {
      knob.classList.remove('active');
    } else {
      knob.classList.add('active');
    }
  }

  // Add to page
  const header = document.querySelector('.masthead');
  if (header) {
    header.appendChild(toggleContainer);
  } else {
    // Fallback - add to body if masthead not found
    console.log("Masthead not found, adding toggle to body");
    document.body.insertAdjacentHTML('afterbegin', 
      '<div class="theme-toggle-fixed">' + 
      toggleContainer.outerHTML + 
      '</div>'
    );
    
    // Re-add event listeners since outerHTML loses them
    document.querySelector('.theme-toggle-switch').addEventListener('click', toggleTheme);
    document.querySelector('.theme-toggle-switch').addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggleTheme();
      }
    });
  }
}); 