
    function updateTotal() {
    let total = 0;
    document.querySelectorAll('.product-entry').forEach(entry => {
        let price = parseFloat(entry.querySelector('.product-select option:checked').dataset.price || 0);
        let qty = parseFloat(entry.querySelector('.quantity-input').value || 0);
        let totalPrice = price * qty;
        entry.querySelector('.price-display').value = totalPrice.toFixed(2);
        total += totalPrice;
    });

    const discountMessage = document.getElementById('discount-message');
    if (total >= 1000) {
        total = total * 0.9;
        discountMessage.textContent = 'A 10% discount has been applied.';
        discountMessage.style.color = 'green';
    } else {
        discountMessage.textContent = '';
    }

    document.getElementById('total-price').value = total.toFixed(2);
}

    document.getElementById('product-list').addEventListener('change', updateTotal);
    document.getElementById('product-list').addEventListener('input', updateTotal);

    document.getElementById('add-product').addEventListener('click', function () {
        let newEntry = document.querySelector('.product-entry').cloneNode(true);
        newEntry.querySelector('.quantity-input').value = '';
        newEntry.querySelector('.price-display').value = '';
        document.getElementById('product-list').appendChild(newEntry);
    });

    document.getElementById('product-list').addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-product')) {
            e.target.closest('.product-entry').remove();
            updateTotal();
        }
    });
