/* ============================================================
   CITY SELECTION POPUP — standalone script
   - Opens only on first visit (localStorage flag)
   - Stores chosen city in localStorage key: selectedCity
   - ESC closes, outside click closes, search filters cities
   - Fully self-contained: does not touch any other script/element
============================================================ */
(function(){
  "use strict";

  var STORAGE_KEY = "selectedCity";
  var VISITED_KEY = "cpHasVisited";

  var overlay = document.getElementById("cp-overlay");
  if(!overlay) return;

  var modal = document.getElementById("cp-modal");
  var closeBtn = document.getElementById("cp-close");
  var searchInput = document.getElementById("cp-search");
  var cityButtons = Array.prototype.slice.call(document.querySelectorAll(".cp-city"));
  var emptyState = document.getElementById("cp-empty");
  var lastFocused = null;

  function openPopup(){
    lastFocused = document.activeElement;
    overlay.classList.add("cp-open");
    overlay.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    setTimeout(function(){
      if(searchInput){ searchInput.focus(); }
    }, 200);
  }

  function closePopup(){
    overlay.classList.remove("cp-open");
    overlay.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    try{ localStorage.setItem(VISITED_KEY, "1"); }catch(e){}
    if(lastFocused && typeof lastFocused.focus === "function"){
      lastFocused.focus();
    }
  }

  function selectCity(btn){
    if(btn.classList.contains("cp-disabled")) return;
    var city = btn.getAttribute("data-city");
    try{ localStorage.setItem(STORAGE_KEY, city); }catch(e){}
    cityButtons.forEach(function(b){ b.classList.remove("cp-selected"); });
    btn.classList.add("cp-selected");
    setTimeout(closePopup, 220);
  }

  cityButtons.forEach(function(btn){
    btn.addEventListener("click", function(){ selectCity(btn); });
    btn.addEventListener("keydown", function(e){
      if(e.key === "Enter" || e.key === " "){
        e.preventDefault();
        selectCity(btn);
      }
    });
  });

  if(closeBtn){
    closeBtn.addEventListener("click", closePopup);
  }

  overlay.addEventListener("click", function(e){
    if(e.target === overlay){
      closePopup();
    }
  });

  document.addEventListener("keydown", function(e){
    if(e.key === "Escape" && overlay.classList.contains("cp-open")){
      closePopup();
    }
  });

  if(searchInput){
    searchInput.addEventListener("input", function(){
      var q = searchInput.value.trim().toLowerCase();
      var visibleCount = 0;
      cityButtons.forEach(function(btn){
        var name = (btn.getAttribute("data-city") || "").toLowerCase();
        var match = name.indexOf(q) !== -1;
        btn.style.display = match ? "" : "none";
        if(match) visibleCount++;
      });
      if(emptyState){
        emptyState.style.display = visibleCount === 0 ? "block" : "none";
      }
    });
  }

  // Mark previously selected city as highlighted, if any
  try{
    var saved = localStorage.getItem(STORAGE_KEY);
    if(saved){
      cityButtons.forEach(function(btn){
        if(btn.getAttribute("data-city") === saved){
          btn.classList.add("cp-selected");
        }
      });
    }
  }catch(e){}

  // Open only on first visit
  try{
    var visited = localStorage.getItem(VISITED_KEY);
    if(!visited){
      // slight delay so it doesn't fight with page paint/other scripts
      setTimeout(openPopup, 400);
    }
  }catch(e){
    // if localStorage unavailable, do not force-open
  }
})();