document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const navCollapse = document.querySelector('.nav-collapse');
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    
    if (hamburgerMenu && navCollapse) {
        document.addEventListener('click', function(event) {
            if (!hamburgerMenu.contains(event.target) && !navCollapse.contains(event.target)) {
                menuToggle.checked = false;
            }
        });
        
        const navLinks = document.querySelectorAll('.nav-collapse a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 992) {
                    menuToggle.checked = false;
                }
            });
        });
    }
});
