(function(){
  "use strict";

  var STORAGE_KEY = "selectedCity";
  var VISITED_KEY = "cityPopupSeen";
  var overlay = document.getElementById("city-popup-overlay");
  var closeBtn = document.getElementById("city-popup-close");
  var searchInput = document.getElementById("city-popup-search-input");
  var emptyState = document.getElementById("city-popup-empty");
  var cityButtons = Array.prototype.slice.call(document.querySelectorAll(".city-option"));
  var lastFocused = null;

  function renderSelection(){
    try {
      var saved = window.localStorage.getItem(STORAGE_KEY);
      cityButtons.forEach(function(btn){
        var isSelected = btn.getAttribute("data-city") === saved;
        btn.classList.toggle("is-selected", isSelected);
      });
    } catch (e) {}
  }

  function openPopup(){
    if (!overlay) return;
    lastFocused = document.activeElement;
    overlay.classList.add("is-open");
    overlay.setAttribute("aria-hidden", "false");
    document.body.classList.add("city-popup-open");
    setTimeout(function(){
      if (searchInput) searchInput.focus();
    }, 120);
  }

  function closePopup(){
    if (!overlay) return;
    overlay.classList.remove("is-open");
    overlay.setAttribute("aria-hidden", "true");
    document.body.classList.remove("city-popup-open");
    try { window.localStorage.setItem(VISITED_KEY, "1"); } catch (e) {}
    if (lastFocused && typeof lastFocused.focus === "function") {
      lastFocused.focus();
    }
  }

  function getCityUrl(city){
    var slug = city.toLowerCase().replace(/\s+/g, '-');
    return slug + '.html';
  }

  function selectCity(btn){
    var city = btn.getAttribute("data-city") || "";
    if (!city) return;
    try { window.localStorage.setItem(STORAGE_KEY, city); } catch (e) {}
    renderSelection();
    window.dispatchEvent(new Event("citySelected"));
    if (typeof window.refreshHeaderCity === "function") {
      window.refreshHeaderCity();
    }
    var url = getCityUrl(city);
    if (url) {
      window.location.href = url;
    } else {
      closePopup();
    }
  }

  if (overlay) {
    overlay.addEventListener("click", function(event){
      if (event.target === overlay) {
        closePopup();
      }
    });

    document.addEventListener("keydown", function(event){
      if (event.key === "Escape" && overlay.classList.contains("is-open")) {
        closePopup();
      }
    });
  }

  if (closeBtn) {
    closeBtn.addEventListener("click", closePopup);
  }

  cityButtons.forEach(function(btn){
    btn.addEventListener("click", function(){ selectCity(btn); });
    btn.addEventListener("keydown", function(event){
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        selectCity(btn);
      }
    });
  });

  if (searchInput) {
    searchInput.addEventListener("input", function(){
      var query = searchInput.value.trim().toLowerCase();
      var visibleCount = 0;
      cityButtons.forEach(function(btn){
        var match = (btn.getAttribute("data-city") || "").toLowerCase().indexOf(query) !== -1;
        btn.style.display = match ? "" : "none";
        if (match) visibleCount++;
      });
      if (emptyState) {
        emptyState.style.display = visibleCount === 0 ? "block" : "none";
      }
    });
  }

  renderSelection();
  window.openCityPopup = openPopup;

  try {
    var seen = window.localStorage.getItem(VISITED_KEY);
    if (!seen) {
      setTimeout(openPopup, 2000);
    }
  } catch (e) {}
})();