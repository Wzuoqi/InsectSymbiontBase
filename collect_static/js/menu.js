document.addEventListener('DOMContentLoaded', function () {
    const productBtn = document.getElementById('product-btn');
    const productMenu = document.getElementById('product-menu');

    productBtn.addEventListener('click', function () {
        productMenu.classList.toggle('hidden');
    });
});

// Show the modal
function showModal() {
    document.getElementById('modal').classList.remove('hidden');
}

// Hide the modal
function hideModal() {
    document.getElementById('modal').classList.add('hidden');
}
