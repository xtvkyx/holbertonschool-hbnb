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

async function submitReview(token, placeId, text, rating) {
  const url = `${API_BASE_URL}/reviews/`;
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ place_id: placeId, text, rating })
  });

  let data = {};
  try { data = await response.json(); } catch (e) {}

  if (!response.ok) {
    const msg = (data && (data.message || data.error)) || response.statusText || "Failed to submit review";
    throw new Error(msg);
  }

  return data;
}

async function fetchPlaceDetails(token, placeId) {
  const url = `${API_BASE_URL}/places/${encodeURIComponent(placeId)}`;
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(url, {
    method: "GET",
    headers
  });

  let data = {};
  try { data = await response.json(); } catch (e) {}

  if (!response.ok) {
    const msg = (data && (data.message || data.error)) || response.statusText || "Failed to fetch place";
    throw new Error(msg);
  }

  return data || {};
}

async function fetchReviewsByPlace(token, placeId) {
  const url = `${API_BASE_URL}/reviews/?place_id=${encodeURIComponent(placeId)}`;
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(url, {
    method: "GET",
    headers
  });

  let data = [];
  try { data = await response.json(); } catch (e) {}

  if (!response.ok) {
    const msg = (data && (data.message || data.error)) || response.statusText || "Failed to fetch reviews";
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

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id") || params.get("place_id");
}

function renderPlaceDetails(place) {
  const titleEl = document.getElementById("place-title");
  if (titleEl) titleEl.textContent = place.title || place.name || "Place";

  const detailsEl = document.getElementById("place-details");
  if (!detailsEl) return;
  detailsEl.innerHTML = "";

  const host = place.host || place.owner_name || place.owner || place.owner_id || "Unknown";
  const price = place.price ?? 0;
  const description = place.description || "";

  const amenities = Array.isArray(place.amenities) ? place.amenities : [];
  const amenityNames = amenities.map((a) => a.name).filter(Boolean);

  detailsEl.innerHTML = `
    <p><strong>Host:</strong> ${host}</p>
    <p><strong>Price per night:</strong> $${price}</p>
    <p><strong>Description:</strong> ${description}</p>
    <p><strong>Amenities:</strong> ${amenityNames.length ? amenityNames.join(", ") : "None"}</p>
  `;
}

function renderReviews(reviews) {
  const wrap = document.getElementById("reviews-wrap");
  if (!wrap) return;
  wrap.innerHTML = "";

  if (!reviews.length) {
    const empty = document.createElement("p");
    empty.textContent = "No reviews yet.";
    wrap.appendChild(empty);
    return;
  }

  for (const review of reviews) {
    const card = document.createElement("article");
    card.className = "review-card";

    const rating = review.rating;
    const ratingText = rating === null || rating === undefined ? "N/A" : String(rating);

    card.innerHTML = `
      <p><strong>User:</strong> ${review.user_id || "Unknown"}</p>
      <p>${review.text || ""}</p>
      <p>Rating: ${ratingText}</p>
    `;

    wrap.appendChild(card);
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

  const placeDetailsEl = document.getElementById("place-details");
  if (placeDetailsEl) {
    const placeId = getPlaceIdFromURL();
    const token = getCookie("token");

    const addReviewSection = document.getElementById("add-review");
    if (addReviewSection) addReviewSection.style.display = token ? "flex" : "none";

    const addReviewLink = document.getElementById("add-review-link");
    if (addReviewLink && placeId) {
      addReviewLink.href = `add_review.html?place_id=${encodeURIComponent(placeId)}`;
    }

    if (!placeId) {
      placeDetailsEl.textContent = "Missing place id in URL.";
      return;
    }

    fetchPlaceDetails(token, placeId)
      .then((place) => {
        renderPlaceDetails(place);
        if (Array.isArray(place.reviews)) {
          renderReviews(place.reviews);
        } else {
          return fetchReviewsByPlace(token, placeId).then(renderReviews);
        }
      })
      .catch((err) => {
        placeDetailsEl.textContent = err.message;
      });
  }

  const reviewForm = document.getElementById("review-form");
  if (reviewForm) {
    const token = getCookie("token");
    if (!token) {
      window.location.href = "index.html";
      return;
    }

    const placeId = getPlaceIdFromURL();
    if (!placeId) {
      window.location.href = "index.html";
      return;
    }

    const reviewMsgEl = document.getElementById("review-message");
    const reviewingTitleEl = document.getElementById("reviewing-title");

    if (reviewingTitleEl) {
      fetchPlaceDetails(token, placeId)
        .then((place) => {
          reviewingTitleEl.textContent = `Reviewing: ${place.title || place.name || ""}`;
        })
        .catch(() => {
          reviewingTitleEl.textContent = "Reviewing:";
        });
    }

    reviewForm.addEventListener("submit", async (event) => {
      event.preventDefault();

      if (reviewMsgEl) {
        reviewMsgEl.textContent = "";
        reviewMsgEl.style.color = "";
      }

      const text = (document.getElementById("review").value || "").trim();
      const ratingRaw = document.getElementById("rating").value;
      const rating = ratingRaw ? Number(ratingRaw) : null;

      try {
        await submitReview(token, placeId, text, rating);
        if (reviewMsgEl) {
          reviewMsgEl.textContent = "Review submitted successfully!";
          reviewMsgEl.style.color = "#2e7d32";
        } else {
          alert("Review submitted successfully!");
        }

        document.getElementById("review").value = "";
        document.getElementById("rating").value = "";
      } catch (err) {
        if (reviewMsgEl) {
          reviewMsgEl.textContent = err.message;
          reviewMsgEl.style.color = "#c62828";
        } else {
          alert(err.message);
        }
      }
    });
  }
});

