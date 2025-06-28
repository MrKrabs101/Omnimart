const cart = {
  "Product A": { price: 10.00, qty: 1, img: "" },
  "Product B": { price: 15.00, qty: 1, img: "" },
  "Product C": { price: 20.00, qty: 1, img: "" }
};

function updateCartUI() {
  const cartItems = document.getElementById('cart-items');
  const itemCount = document.getElementById('item-count');
  const cartTotal = document.getElementById('cart-total');
  const hstField = document.getElementById('hst');

  cartItems.innerHTML = '';
  let subtotal = 0;
  let count = 0;

  for (let item in cart) {
    const { price, qty, img } = cart[item];
    const itemTotal = price * qty;
    subtotal += itemTotal;
    count += qty;

    const itemDiv = document.createElement('div');
    itemDiv.className = 'cart-item';
    itemDiv.innerHTML = `
      <img src="${img}" alt="${item}">
      <div class="item-details">
        <h4>${item}</h4>
        <p>Price: $${price.toFixed(2)}</p>
        <div class="qty-controls">
          <button onclick="changeQty('${item}', -1)">-</button>
          <span>${qty}</span>
          <button onclick="changeQty('${item}', 1)">+</button>
          <button onclick="removeItem('${item}')">Delete</button>
        </div>
      </div>
    `;
    cartItems.appendChild(itemDiv);
  }

  const hst = subtotal * 0.13;
  const totalWithTax = subtotal + hst;

  itemCount.textContent = count;
  hstField.textContent = hst.toFixed(2);
  cartTotal.textContent = `Total: $${totalWithTax.toFixed(2)}`;
}

function changeQty(item, delta) {
  cart[item].qty += delta;
  if (cart[item].qty <= 0) delete cart[item];
  updateCartUI();
}

function removeItem(item) {
  delete cart[item];
  updateCartUI();
}

document.getElementById('checkout').onclick = () => {
  document.getElementById('confirmation-msg').classList.remove('hidden');
};

updateCartUI();
