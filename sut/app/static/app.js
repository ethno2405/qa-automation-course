// Course Shop: cart functions of the web UI.
"use strict";

const slowUi = document.body.dataset.slowUi === "1";
const legacyCart = document.body.dataset.legacyCart === "1";

function randomDelay(maxMs) {
  return slowUi ? Math.random() * maxMs : 0;
}

function later(maxMs, action) {
  const delay = randomDelay(maxMs);
  if (delay === 0) {
    action();
  } else {
    setTimeout(action, delay);
  }
}

function setBadge(count) {
  const badge = document.getElementById("cart-count");
  if (badge) {
    badge.textContent = String(count);
  }
}

async function callApi(method, url, body) {
  const options = { method, headers: { "Accept": "application/json" }, credentials: "same-origin" };
  if (body !== undefined) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }
  let response;
  try {
    response = await fetch(url, options);
  } catch {
    return { ok: false, status: 0, data: { error: "The shop cannot be reached. Try again." } };
  }
  const data = await response.json().catch(() => ({}));
  return { ok: response.ok, status: response.status, data };
}

// Product page: add to cart
const addButton = document.getElementById("add-to-cart");
if (addButton) {
  const message = document.getElementById("add-message");
  if (slowUi) {
    addButton.disabled = true;
    later(2000, () => { addButton.disabled = false; });
  }
  addButton.addEventListener("click", async () => {
    const quantity = Number.parseInt(document.getElementById("quantity").value, 10);
    const productId = Number.parseInt(addButton.dataset.productId, 10);
    message.textContent = "";
    message.className = "";
    const result = await callApi("POST", "/api/cart/items", { product_id: productId, quantity });
    later(1500, () => {
      if (result.ok) {
        message.textContent = "The book is in the cart.";
        message.className = "ok";
        setBadge(result.data.count);
      } else {
        message.textContent = result.data.error || "The book could not be added.";
        message.className = "error";
      }
    });
  });
}

// Cart page: remove a book
function showTotals(cart) {
  document.getElementById("subtotal").textContent = `${cart.subtotal} EUR`;
  document.getElementById("discount").textContent = `${cart.discount === "0.00" ? "" : "-"}${cart.discount} EUR`;
  document.getElementById("discount-name").textContent = cart.discount_name || "";
  document.getElementById("shipping").textContent = `${cart.shipping} EUR`;
  document.getElementById("total").textContent = `${cart.total} EUR`;
}

function showCartError(text) {
  const message = document.getElementById("cart-message");
  message.textContent = text;
}

for (const button of document.querySelectorAll("button.remove")) {
  button.addEventListener("click", async () => {
    const productId = button.dataset.productId;
    showCartError("");
    const removed = await callApi("DELETE", `/api/cart/items/${productId}`);
    if (!removed.ok) {
      showCartError(removed.data.error || "The book could not be removed.");
      return;
    }
    const coupon = document.getElementById("coupon").value;
    const query = coupon ? `?coupon=${encodeURIComponent(coupon)}` : "";
    const cart = await callApi("GET", `/api/cart${query}`);
    if (!cart.ok) {
      showCartError("The cart could not be updated. Reload the page.");
      return;
    }
    later(1500, () => {
      button.closest("tr").remove();
      showTotals(cart.data);
      if (!legacyCart) {
        setBadge(cart.data.count);
      }
      if (cart.data.items.length === 0) {
        document.querySelector("[data-testid=cart-table]").remove();
        document.querySelector("[data-testid=checkout-button]").disabled = true;
      }
    });
  });
}
