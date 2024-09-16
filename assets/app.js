document.addEventListener('DOMContentLoaded', function() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function(event) {
            event.preventDefault();
            alert(`You clicked on ${item.textContent}`);
        });
    });
});