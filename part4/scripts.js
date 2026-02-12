/* scripts.js */

const API_BASE_URL = "http://127.0.0.1:5000/api/v1"; // <-- change if needed

function setCookie(name, value, days = 1) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  // SameSite=Lax works for normal local testing
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax`;
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

document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  if (!loginForm) return; // only run on login page

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
});

