(() => {
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

  const activateOnly = (button, selector) => {
    $$(selector).forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
  };

  const toast = (message) => {
    let item = document.querySelector(".tl-toast");
    if (!item) {
      item = document.createElement("div");
      item.className = "tl-toast";
      document.body.appendChild(item);
    }

    item.textContent = message;
    item.classList.add("show");
    window.clearTimeout(toast.timer);
    toast.timer = window.setTimeout(() => item.classList.remove("show"), 2000);
  };

  const initButtonGroups = () => {
    [".type-btn", ".tab-btn", ".sort-btn", ".view-btn"].forEach((selector) => {
      $$(selector).forEach((button) => {
        button.addEventListener("click", () => activateOnly(button, selector));
      });
    });

    $$(".filter-btn").forEach((button) => {
      button.addEventListener("click", () => button.classList.toggle("active"));
    });
  };

  const initCards = () => {
    $$(".sug-card").forEach((card) => {
      card.addEventListener("click", () => card.classList.toggle("selected"));
    });

    $$(".action-btn.danger, .activity-del").forEach((button) => {
      button.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        const row = button.closest(".trip-card, .activity-row");
        if (row) row.remove();
      });
    });

    $$(".result-meta .btn").forEach((button) => {
      button.addEventListener("click", (event) => {
        event.stopPropagation();
        button.textContent = "Added";
        button.disabled = true;
        toast("Added to trip");
      });
    });
  };

  const initSearch = () => {
    $$(".search-box input").forEach((input) => {
      input.addEventListener("input", () => {
        const query = input.value.trim().toLowerCase();
        $$(".trip-card").forEach((card) => {
          card.style.display = card.textContent.toLowerCase().includes(query) ? "" : "none";
        });
      });
    });

    $$(".search-hero-input input").forEach((input) => {
      input.addEventListener("input", () => {
        const query = input.value.trim().toLowerCase();
        $$(".result-card").forEach((card) => {
          card.style.display = card.textContent.toLowerCase().includes(query) ? "" : "none";
        });
      });
    });
  };

  const initProfile = () => {
    $$(".toggle").forEach((toggle) => {
      toggle.addEventListener("click", () => toggle.classList.toggle("on"));
    });
  };

  document.addEventListener("DOMContentLoaded", () => {
    initButtonGroups();
    initCards();
    initSearch();
    initProfile();
  });
})();
