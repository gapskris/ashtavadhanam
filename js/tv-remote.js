/**
 * Ashtavadhanam Modern — Smart TV Remote Control & D-Pad Navigation Handler
 */

(function() {
  let isTvMode = false;
  let focusableElements = [];
  let currentFocusIndex = 0;

  // Auto-detect Smart TV User Agents (Samsung Tizen, LG webOS, Android TV, Apple TV, Sony Bravia, etc.)
  function autoDetectTv() {
    const ua = navigator.userAgent.toLowerCase();
    const isTV = /smart-tv|smarttv|googletv|appletv|hbbtv|pov_tv|netcast|tizen|webos|viera|bravia|hisense|aftb|aftt/.test(ua);
    if (isTV) {
      console.log("Smart TV browser detected. Activating 10-foot UI mode.");
      window.toggleTvMode(true);
    }
  }

  function updateFocusables() {
    focusableElements = Array.from(document.querySelectorAll(
      'button:not([disabled]):not(.hidden), .round-pill, .dialogue-card, input, [tabindex="0"]'
    )).filter(el => {
      return el.offsetParent !== null && !el.closest('.hidden');
    });
  }

  function setFocus(index) {
    if (focusableElements.length === 0) return;
    if (index < 0) index = 0;
    if (index >= focusableElements.length) index = focusableElements.length - 1;
    
    currentFocusIndex = index;
    const el = focusableElements[currentFocusIndex];
    if (el) {
      el.focus();
      el.classList.add('focused');
      // remove focused from others
      focusableElements.forEach(item => {
        if (item !== el) item.classList.remove('focused');
      });
      el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

  // Keyboard / Remote D-Pad Listener
  window.addEventListener('keydown', (e) => {
    const key = e.key;

    // Toggle TV mode with key 't' or 'T'
    if (key === 't' || key === 'T') {
      window.toggleTvMode();
      return;
    }

    // Spacebar toggles audio play/pause
    if (key === ' ' && e.target.tagName !== 'INPUT') {
      e.preventDefault();
      if (window.Player) window.Player.togglePlayPause();
      return;
    }

    // Escape closes modals or nav drawer
    if (key === 'Escape') {
      const exitModal = document.getElementById('exit-modal');
      if (exitModal && !exitModal.classList.contains('hidden')) {
        exitModal.classList.add('hidden');
        return;
      }
      const searchModal = document.getElementById('search-modal');
      if (searchModal && !searchModal.classList.contains('hidden')) {
        searchModal.classList.add('hidden');
        return;
      }
      if (window.Player && !document.getElementById('video-modal').classList.contains('hidden')) {
        window.Player.closeVideoModal();
      }
      const nav = document.getElementById('nav-drawer');
      if (nav && nav.classList.contains('open')) {
        nav.classList.remove('open');
      }
      return;
    }

    // Handle arrows for navigation
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(key)) {
      updateFocusables();
      if (focusableElements.length === 0) return;

      if (key === 'ArrowDown') {
        e.preventDefault();
        setFocus(currentFocusIndex + 1);
      } else if (key === 'ArrowUp') {
        e.preventDefault();
        setFocus(currentFocusIndex - 1);
      } else if (key === 'ArrowRight') {
        if (document.activeElement && document.activeElement.classList.contains('round-pill')) {
          e.preventDefault();
          const next = document.activeElement.nextElementSibling;
          if (next) next.focus();
        } else if (e.ctrlKey && window.Player) {
          window.Player.playNext();
        }
      } else if (key === 'ArrowLeft') {
        if (document.activeElement && document.activeElement.classList.contains('round-pill')) {
          e.preventDefault();
          const prev = document.activeElement.previousElementSibling;
          if (prev) prev.focus();
        } else if (e.ctrlKey && window.Player) {
          window.Player.playPrevious();
        }
      }
    }
  });

  // Export TV mode toggle
  window.toggleTvMode = function(forceState) {
    if (typeof forceState === 'boolean') {
      isTvMode = forceState;
    } else {
      isTvMode = !isTvMode;
    }
    document.body.classList.toggle('tv-mode', isTvMode);
    const btn = document.getElementById('btn-tv-mode');
    if (btn) btn.classList.toggle('active', isTvMode);
  };

  window.addEventListener('DOMContentLoaded', autoDetectTv);
})();
