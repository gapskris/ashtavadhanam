/**
 * Ashtavadhanam Modern — Adaptive Viewport Engine
 * Autonomously inspects device viewport (dimensions, aspect ratio, safe insets, browser chrome)
 * and dynamically calculates mathematical layout variables, preventing any top/bottom clipping
 * on arbitrary mobile, tablet, foldable, desktop, and Smart TV viewports.
 *
 * Exposes window.ViewportEngine for runtime querying and programmatic updates.
 */
(function(global) {
  'use strict';

  function updateViewportMetrics() {
    const vv = typeof window !== 'undefined' ? window.visualViewport : null;
    const w = vv ? vv.width : window.innerWidth;
    const h = vv ? vv.height : window.innerHeight;
    const aspect = w / Math.max(1, h);
    const isLandscape = aspect > 1.05;

    // 1. Determine device form factor profile
    let profile = 'desktop';
    if (w <= 540 || (!isLandscape && w <= 640) || (isLandscape && h <= 500)) {
      profile = h < 660 ? 'phone-compact' : 'phone-tall';
    } else if (w <= 1024) {
      profile = isLandscape ? 'tablet-landscape' : 'tablet-portrait';
    } else if (w >= 2400 || h >= 1400) {
      profile = 'tv-ultrawide';
    }

    // 2. Derive dynamic UI scale and stage height budgets
    let uiScale = 1.0;
    let maxStageHeight = 360;

    if (isLandscape && h <= 500) {
      // Landscape mobile (e.g. 844x390, 667x375, 740x360)
      maxStageHeight = Math.round(Math.min(130, Math.max(90, h * 0.28)));
      uiScale = Math.min(0.75, Math.max(0.55, h / 540));
    } else if (profile.startsWith('phone')) {
      // Mobile Portrait:
      // Non-frame vertical budget: Emblem (~70px) + Mantra (~36px) + Caption (~50px) + Buttons (~80px) + Insets (~30px) = ~266px
      const nonFrameBudget = 265;
      const remainingHeight = Math.max(120, h - nonFrameBudget);

      // Frame height dynamically capped at remaining budget or 24% of viewport height (whichever is safer)
      maxStageHeight = Math.round(Math.min(210, Math.max(125, Math.min(remainingHeight, h * 0.24))));

      // UI scale for typography, margins, and icons
      uiScale = Math.min(1.05, Math.max(0.68, (h / 700) * 0.95));
    } else if (profile.startsWith('tablet')) {
      // Tablet viewports
      maxStageHeight = Math.round(Math.min(320, Math.max(200, h * 0.32)));
      uiScale = Math.min(1.15, Math.max(0.90, h / 800));
    } else {
      // Desktop / Smart TV
      maxStageHeight = Math.round(Math.min(480, Math.max(260, h * 0.36)));
      uiScale = Math.min(1.35, Math.max(1.00, h / 900));
    }

    // 3. Write directly to root CSS custom properties
    const root = document.documentElement;
    root.style.setProperty('--app-dvh', `${h}px`);
    root.style.setProperty('--app-dvw', `${w}px`);
    root.style.setProperty('--ui-scale', uiScale.toFixed(3));
    root.style.setProperty('--dynamic-stage-max-h', `${maxStageHeight}px`);
    root.setAttribute('data-device-profile', profile);
    root.setAttribute('data-orientation', isLandscape ? 'landscape' : 'portrait');

    return {
      width: w,
      height: h,
      aspectRatio: aspect,
      profile: profile,
      orientation: isLandscape ? 'landscape' : 'portrait',
      uiScale: parseFloat(uiScale.toFixed(3)),
      maxStageHeight: maxStageHeight
    };
  }

  // Execute synchronously before paint
  if (typeof document !== 'undefined') {
    updateViewportMetrics();
  }

  // Reactive listener with RAF debouncing
  if (typeof window !== 'undefined') {
    let ticking = false;
    const onResize = function() {
      if (!ticking) {
        window.requestAnimationFrame(function() {
          updateViewportMetrics();
          ticking = false;
        });
        ticking = true;
      }
    };

    window.addEventListener('resize', onResize, { passive: true });
    if (window.visualViewport) {
      window.visualViewport.addEventListener('resize', onResize, { passive: true });
      window.visualViewport.addEventListener('scroll', onResize, { passive: true });
    }
    window.addEventListener('orientationchange', function() {
      setTimeout(updateViewportMetrics, 100);
    });
  }

  // Public API
  global.ViewportEngine = {
    update: updateViewportMetrics,
    getMetrics: function() {
      const vv = typeof window !== 'undefined' ? window.visualViewport : null;
      const root = typeof document !== 'undefined' ? document.documentElement : null;
      return {
        width: vv ? vv.width : (typeof window !== 'undefined' ? window.innerWidth : 0),
        height: vv ? vv.height : (typeof window !== 'undefined' ? window.innerHeight : 0),
        profile: root ? root.getAttribute('data-device-profile') : 'desktop',
        orientation: root ? root.getAttribute('data-orientation') : 'portrait',
        uiScale: root ? parseFloat(root.style.getPropertyValue('--ui-scale') || '1') : 1,
        maxStageHeight: root ? parseInt(root.style.getPropertyValue('--dynamic-stage-max-h') || '360', 10) : 360
      };
    }
  };

})(typeof window !== 'undefined' ? window : this);
