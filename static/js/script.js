document.addEventListener('DOMContentLoaded', () => {
  // Checkout confirmation
  const checkoutBtn = document.getElementById('checkout');
  if (checkoutBtn) {
    checkoutBtn.onclick = () => {
      const confirmation = document.getElementById('confirmation-msg');
      if (confirmation) {
        confirmation.classList.remove('hidden');
      }
    };
  }

  // Add to cart buttons
  document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', () => {
      const productId = button.getAttribute('data-id');
      addToCart(productId);
    });
  });
});

function addToCart(asin) {
  const qty = document.getElementById("qty").value;
  fetch(`/add-to-cart/${asin}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ qty: qty })
  })
  .then(response => {
    if (response.ok) {
      document.getElementById("cart-message").textContent = "Added to cart!";
    } else {
      document.getElementById("cart-message").textContent = "Failed to add to cart.";
    }
  })
  .catch(error => {
    console.error("Error:", error);
    document.getElementById("cart-message").textContent = "Error adding to cart.";
  });
}


function loadProducts(category = '', search = '') {
  let url = '/api/products';
  const params = [];

  if (category) params.push(`category=${encodeURIComponent(category)}`);
  if (search) params.push(`search=${encodeURIComponent(search)}`);
  if (params.length) url += '?' + params.join('&');

  fetch(url)
    .then(res => res.json())
    .then(products => {
      const grid = document.querySelector('.product-grid');
      grid.innerHTML = '';

      products.forEach(item => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
          <img src="/static/images/${item.image_url}" alt="${item.name}">
          <h4>${item.name}</h4>
          <p>$${item.price}</p>
          <button class="add-to-cart" data-id="${item.id}">Add to Cart</button>
        `;
        grid.appendChild(card);
      });

      document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', () => {
          const productId = button.getAttribute('data-id');
          addToCart(productId);
        });
      });
    })
    .catch(err => console.error("Failed to load products:", err));
}
