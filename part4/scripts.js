/* scripts.js */

const API_BASE_URL = "http://127.0.0.1:5000/api/v1"; // <-- change if needed

function setCookie(name, value, days = 1) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  // SameSite=Lax works for normal local testing
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax`;
}

function getCookie(name) {
  const cookies = document.cookie ? document.cookie.split(";") : [];
  for (const cookie of cookies) {
    const [k, ...rest] = cookie.trim().split("=");
    if (k === name) return decodeURIComponent(rest.join("="));
  }
  return null;
}

async function loginUser(email, password) {
  const url = `${API_BASE_URL}/login`;

  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  // Try to parse json safely
  let data = {};
  try { data = await response.json(); } catch (e) {}

  if (!response.ok) {
    // Prefer API message if exists
    const msg = data.message || data.error || response.statusText || "Login failed";
    throw new Error(msg);
  }

  const token = data.access_token;
  if (!token) {
    throw new Error("Login succeeded but no access_token returned.");
  }

  return token;
}

async function fetchPlaces(token) {
  const url = `${API_BASE_URL}/places/`;
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(url, {
    method: "GET",
    headers
  });

  let data = [];
  try { data = await response.json(); } catch (e) {}

  if (!response.ok) {
    const msg = (data && (data.message || data.error)) || response.statusText || "Failed to fetch places";
    throw new Error(msg);
  }

  return Array.isArray(data) ? data : [];
}

function renderPlaces(places) {
  const listEl = document.getElementById("places-list");
  if (!listEl) return;
  listEl.innerHTML = "";

  for (const place of places) {
    const card = document.createElement("article");
    card.className = "place-card";
    card.dataset.price = String(place.price ?? "");

    const title = place.title || place.name || "Untitled";
    const price = place.price ?? 0;
    const id = place.id;

    card.innerHTML = `
      <h2>${title}</h2>
      <p class="price">Price per night: $${price}</p>
      <a href="place.html${id ? `?id=${encodeURIComponent(id)}` : ""}" class="details-button">View Details</a>
    `;

    listEl.appendChild(card);
  }
}

function applyPriceFilter(maxPrice) {
  const listEl = document.getElementById("places-list");
  if (!listEl) return;

  const cards = listEl.querySelectorAll(".place-card");
  for (const card of cards) {
    const priceRaw = card.dataset.price;
    const price = Number(priceRaw);
    const show = maxPrice === null || (Number.isFinite(price) && price <= maxPrice);
    card.style.display = show ? "" : "none";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    const errorEl = document.getElementById("error-message");

    loginForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (errorEl) errorEl.textContent = "";

      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value;

      try {
        const token = await loginUser(email, password);
        setCookie("token", token, 1);
        window.location.href = "index.html";
      } catch (err) {
        if (errorEl) errorEl.textContent = err.message;
        else alert(err.message);
      }
    });
  }

  const loginLink = document.getElementById("login-link");
  if (loginLink) {
    const token = getCookie("token");
    loginLink.style.display = token ? "none" : "inline-block";
  }

  const priceFilterEl = document.getElementById("price-filter");
  const placesListEl = document.getElementById("places-list");

  if (placesListEl) {
    const token = getCookie("token");
    fetchPlaces(token)
      .then((places) => {
        renderPlaces(places);
        if (priceFilterEl) {
          const val = priceFilterEl.value;
          applyPriceFilter(val === "all" ? null : Number(val));
        }
      })
      .catch((err) => {
        placesListEl.innerHTML = "";
        const msg = document.createElement("p");
        msg.textContent = err.message;
        placesListEl.appendChild(msg);
      });
  }

  if (priceFilterEl) {
    priceFilterEl.addEventListener("change", (event) => {
      const value = event.target.value;
      const maxPrice = value === "all" ? null : Number(value);
      applyPriceFilter(maxPrice);
    });
  }
});

