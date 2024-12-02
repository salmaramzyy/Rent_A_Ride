'use strict';

/**
 * navbar toggle
 */

const overlay = document.querySelector("[data-overlay]");
const navbar = document.querySelector("[data-navbar]");
const navToggleBtn = document.querySelector("[data-nav-toggle-btn]");
const navbarLinks = document.querySelectorAll("[data-nav-link]");

const navToggleFunc = function () {
  navToggleBtn.classList.toggle("active");
  navbar.classList.toggle("active");
  overlay.classList.toggle("active");
}

navToggleBtn.addEventListener("click", navToggleFunc);
overlay.addEventListener("click", navToggleFunc);

for (let i = 0; i < navbarLinks.length; i++) {
  navbarLinks[i].addEventListener("click", navToggleFunc);
}



/**
 * header active on scroll
 */

const header = document.querySelector("[data-header]");

window.addEventListener("scroll", function () {
  window.scrollY >= 10 ? header.classList.add("active")
    : header.classList.remove("active");
});


// Function to handle login
function handleLogin() {
  const email = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value.trim();

  // Basic validation
  if (!email || !password) {
    alert("Please fill in all login fields.");
    return;
  }

  // Placeholder logic for authentication (replace with backend API integration)
  console.log("Logging in with:", { email, password });
  alert(`Logging in with email: ${email}`);
}

// Function to handle registration
function handleRegister() {
  const name = document.getElementById("register-name").value.trim();
  const email = document.getElementById("register-email").value.trim();
  const password = document.getElementById("register-password").value.trim();

  // Basic validation
  if (!name || !email || !password) {
    alert("Please fill in all registration fields.");
    return;
  }

  // Placeholder logic for user registration (replace with backend API integration)
  console.log("Registering user:", { name, email, password });
  alert(`Registering user: ${name}`);
}

// Optional: Toggle between login and register forms
function toggleForms(showLogin) {
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");

  if (showLogin) {
    loginForm.style.display = "block";
    registerForm.style.display = "none";
  } else {
    loginForm.style.display = "none";
    registerForm.style.display = "block";
  }
}

// Add event listeners to toggle buttons (if applicable)
document.addEventListener("DOMContentLoaded", () => {
  const toggleToLogin = document.getElementById("toggle-to-login");
  const toggleToRegister = document.getElementById("toggle-to-register");

  if (toggleToLogin) {
    toggleToLogin.addEventListener("click", () => toggleForms(true));
  }
  if (toggleToRegister) {
    toggleToRegister.addEventListener("click", () => toggleForms(false));
  }
});

