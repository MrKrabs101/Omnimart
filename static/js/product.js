function changeQty(delta) {
  const qtyInput = document.getElementById("qty");
  let current = parseInt(qtyInput.value);
  if (!isNaN(current)) {
    qtyInput.value = Math.max(1, current + delta);
  }
}

function addToCart(asin) {
  const qty = document.getElementById("qty").value;

  fetch(`/add-to-cart/${asin}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ qty: qty })
  })
  .then(response => response.json())
  .then(data => {
    const messageEl = document.getElementById("cart-message");
    if (messageEl) {
      messageEl.textContent = data.message || "Added to cart!";
      messageEl.style.color = "green";
    }
  })
  .catch(error => {
    console.error("Error:", error);
    const messageEl = document.getElementById("cart-message");
    if (messageEl) {
      messageEl.textContent = "Error adding to cart.";
      messageEl.style.color = "red";
    }
  });
}
