document.addEventListener('DOMContentLoaded', function() {
    const cartLink = document.getElementById('cart-link');
    const cartPopup = document.getElementById('cart-popup');

    if (cartLink && cartPopup) {
        cartLink.addEventListener('mouseover', function() {
            cartPopup.style.display = 'block';
        });

        cartLink.addEventListener('mouseout', function() {
            cartPopup.style.display = 'none';
        });

        cartPopup.addEventListener('mouseover', function() {
            cartPopup.style.display = 'block';
        });

        cartPopup.addEventListener('mouseout', function() {
            cartPopup.style.display = 'none';
        });
    }
});