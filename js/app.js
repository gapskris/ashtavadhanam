/**
 * Ashtavadhanam Modern — Application Controller & Router
 * 100% 1-to-1 Content Mapped Architecture
 */

class AshtavadhanamApp {
  constructor() {
    this.data = window.ASHTAVADHANAM_DATA;
    this.currentPageIndex = 0;
    this.currentSection = 'performance';
    this.displayView = 'devanagari';
    
    // Treatise reader indices
    this.currentAvadhanaIndex = 0;
    this.currentConcentrationIndex = 0;
    
    // UI Elements
    this.splashGateway = document.getElementById('splash-gateway');
    this.openingTitleStage = document.getElementById('opening-title-stage');
    this.openingVideoStage = document.getElementById('opening-video-stage');
    this.openingFadeImg = document.getElementById('opening-title-img') || document.getElementById('opening-fade-img');
    this.openingProgressFill = document.getElementById('opening-progress-fill');
    this.openingFrameCaption = document.getElementById('opening-frame-caption');
    this.btnSkipOpening = document.getElementById('btn-enter') || document.getElementById('btn-skip-opening');
    this.btnWatchOpeningVideo = document.getElementById('btn-start-montage') || document.getElementById('btn-watch-opening-video');
    this.btnSkipVideoStage = document.getElementById('btn-skip-montage') || document.getElementById('btn-skip-video-stage');
    this.btnOpenVideoInModal = document.getElementById('btn-open-video-in-modal');
    this.openingMontageVideo = document.getElementById('opening-montage-video');
    this.btnReplayOpening = document.getElementById('btn-replay-opening');

    this.appShell = document.getElementById('app-shell');
    this.roundPillsContainer = document.getElementById('round-pills');
    this.dialoguesWrapper = document.getElementById('dialogues-wrapper');
    this.currentRoundTitle = document.getElementById('current-round-title');
    this.currentRoundMeta = document.getElementById('current-round-meta');
    this.btnPlayAllRound = document.getElementById('btn-play-all-round');
    this.btnWatchVideo = document.getElementById('btn-watch-video');
    this.navDrawer = document.getElementById('nav-drawer');
    this.btnToggleMenu = document.getElementById('btn-toggle-menu');
    this.btnCloseNav = document.getElementById('btn-close-nav');
    
    this.openingTimer = null;
    this.init();
  }

  init() {
    // Opening Sequence
    this.initOpeningSequence();

    // Option 1: Responsive Docked Sidebar on Desktop (>= 1280px)
    const backdropEl = document.getElementById('nav-drawer-backdrop');
    const btnCollapseSidebar = document.getElementById('btn-collapse-sidebar');

    const initSidebarState = () => {
      if (window.innerWidth >= 1280) {
        document.body.classList.add('sidebar-docked');
        document.body.classList.remove('sidebar-collapsed');
      } else {
        document.body.classList.remove('sidebar-docked', 'sidebar-collapsed');
      }
    };
    initSidebarState();

    window.addEventListener('resize', () => {
      if (window.innerWidth < 1280 && document.body.classList.contains('sidebar-docked')) {
        document.body.classList.remove('sidebar-docked', 'sidebar-collapsed');
      } else if (window.innerWidth >= 1280 && !document.body.classList.contains('sidebar-collapsed')) {
        document.body.classList.add('sidebar-docked');
      }
    });

    const closeDrawerMobile = () => {
      this.navDrawer.classList.remove('open');
      if (backdropEl) backdropEl.classList.remove('active');
    };

    const toggleDrawer = () => {
      if (window.innerWidth >= 1280) {
        const isCollapsed = document.body.classList.toggle('sidebar-collapsed');
        document.body.classList.toggle('sidebar-docked', !isCollapsed);
      } else {
        const isOpen = this.navDrawer.classList.toggle('open');
        if (backdropEl) backdropEl.classList.toggle('active', isOpen);
      }
    };

    this.btnToggleMenu.addEventListener('click', toggleDrawer);
    this.btnCloseNav.addEventListener('click', closeDrawerMobile);
    if (backdropEl) backdropEl.addEventListener('click', closeDrawerMobile);

    // Right Tools & Settings Drawer (Symmetrical to Left Nav Drawer)
    const toolsDrawer = document.getElementById('tools-drawer');
    const toolsBackdrop = document.getElementById('tools-drawer-backdrop');
    const btnToggleTools = document.getElementById('btn-toggle-tools');
    const btnCloseTools = document.getElementById('btn-close-tools');

    const openToolsDrawer = () => {
      if (toolsDrawer) toolsDrawer.classList.add('open');
      if (toolsBackdrop) {
        toolsBackdrop.classList.remove('hidden');
        toolsBackdrop.classList.add('active');
      }
    };

    const closeToolsDrawer = () => {
      if (toolsDrawer) toolsDrawer.classList.remove('open');
      if (toolsBackdrop) {
        toolsBackdrop.classList.remove('active');
        toolsBackdrop.classList.add('hidden');
      }
    };

    if (btnToggleTools) btnToggleTools.addEventListener('click', openToolsDrawer);
    if (btnCloseTools) btnCloseTools.addEventListener('click', closeToolsDrawer);
    if (toolsBackdrop) toolsBackdrop.addEventListener('click', closeToolsDrawer);

    // Wire individual tool items
    const toolSearch = document.getElementById('tool-search');
    if (toolSearch) {
      toolSearch.addEventListener('click', () => {
        closeToolsDrawer();
        if (this.search) this.search.open();
      });
    }

    const toolInstall = document.getElementById('tool-install');
    if (toolInstall) {
      toolInstall.addEventListener('click', () => {
        closeToolsDrawer();
        if (this.deferredInstallPrompt) {
          this.deferredInstallPrompt.prompt();
          this.deferredInstallPrompt.userChoice.then(() => {
            this.deferredInstallPrompt = null;
          });
        } else {
          alert('Ashtavadhanam App is ready for offline install.\n• On Chrome/Android: Tap 3-dots ⋮ > Add to Home screen\n• On iOS Safari: Tap Share ⎙ > Add to Home Screen');
        }
      });
    }

    const toolTv = document.getElementById('tool-tv-mode');
    if (toolTv) {
      toolTv.addEventListener('click', () => {
        closeToolsDrawer();
        if (window.toggleTvMode) window.toggleTvMode();
      });
    }

    const toolFullscreen = document.getElementById('tool-fullscreen');
    if (toolFullscreen) {
      toolFullscreen.addEventListener('click', () => {
        closeToolsDrawer();
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen().catch(e => console.log(e));
        } else {
          document.exitFullscreen().catch(e => console.log(e));
        }
      });
    }

    const toolHelp = document.getElementById('tool-help');
    if (toolHelp) {
      toolHelp.addEventListener('click', () => {
        closeToolsDrawer();
        this.navigateToSection('help');
      });
    }

    const toolChimes = document.getElementById('tool-chimes');
    const toolChimesStatus = document.getElementById('tool-chimes-status');
    const updateChimesDisplay = () => {
      const enabled = localStorage.getItem('ashtavadhanam_chimes_enabled') !== 'false';
      if (toolChimesStatus) {
        toolChimesStatus.textContent = enabled ? 'ON' : 'OFF';
        toolChimesStatus.classList.toggle('active', enabled);
      }
    };
    updateChimesDisplay();

    if (toolChimes) {
      toolChimes.addEventListener('click', () => {
        const btnToggleChimes = document.getElementById('btn-toggle-chimes');
        if (btnToggleChimes) {
          btnToggleChimes.click();
        } else {
          const current = localStorage.getItem('ashtavadhanam_chimes_enabled') !== 'false';
          localStorage.setItem('ashtavadhanam_chimes_enabled', !current ? 'true' : 'false');
        }
        updateChimesDisplay();
      });
    }

    if (btnCollapseSidebar) {
      btnCollapseSidebar.addEventListener('click', () => {
        document.body.classList.add('sidebar-collapsed');
        document.body.classList.remove('sidebar-docked');
      });
    }

    // Home Button & Brand Click -> Return directly to Main Landing Page
    const handleHomeClick = () => {
      this.returnToLandingPage();
    };
    const btnHome = document.getElementById('btn-home');
    if (btnHome) btnHome.addEventListener('click', handleHomeClick);
    const brandHome = document.getElementById('brand-home');
    if (brandHome) brandHome.addEventListener('click', handleHomeClick);

    // Nav Links
    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', (e) => {
        const sec = e.currentTarget.dataset.section;
        if (sec) {
          this.navigateToSection(sec);
          closeDrawerMobile();
        }
      });
    });

    // 3-Way Display Switcher
    document.querySelectorAll('.view-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const view = e.currentTarget.dataset.view;
        this.setDisplayView(view);
      });
    });

    // Page arrows for Rounds
    document.getElementById('btn-round-prev').addEventListener('click', () => {
      if (this.currentPageIndex > 0) this.navigateToPage(this.currentPageIndex);
    });
    document.getElementById('btn-round-next').addEventListener('click', () => {
      if (this.currentPageIndex < 24) this.navigateToPage(this.currentPageIndex + 2);
    });

    // Play All Round
    this.btnPlayAllRound.addEventListener('click', () => {
      if (window.Player) window.Player.playClip(0);
    });

    // TV Mode Button
    const btnTv = document.getElementById('btn-tv-mode');
    if (btnTv) btnTv.addEventListener('click', () => window.toggleTvMode && window.toggleTvMode());

    // Fullscreen Button
    const btnFs = document.getElementById('btn-fullscreen');
    if (btnFs) {
      btnFs.addEventListener('click', () => {
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen().catch(e => console.log(e));
        } else {
          document.exitFullscreen().catch(e => console.log(e));
        }
      });
    }

    // Help Button
    const btnHelp = document.getElementById('btn-help');
    if (btnHelp) {
      btnHelp.addEventListener('click', () => {
        this.navigateToSection('help');
        this.navDrawer.classList.remove('open');
      });
    }

    // Search Drawer Button
    const btnNavSearch = document.getElementById('btn-nav-search');
    if (btnNavSearch) {
      btnNavSearch.addEventListener('click', () => {
        this.navDrawer.classList.remove('open');
        if (this.search) this.search.open();
      });
    }

    // Initialize modules
    this.renderRoundPills();
    this.initAvadhanaReader();
    this.initConcentrationReader();
    this.renderTreatises();
    this.renderAcknowledgments();
    this.renderHelp();
    this.renderGlimpses();
    this.renderHistoricalGallery();
    this.initTouchGestures();
    this.initExitModal();

    // Initialize Search Engine (Phase 10)
    if (window.AshtavadhanamSearch) {
      this.search = new window.AshtavadhanamSearch(this);
      this.search.initUI();
      window.Search = this.search;
    }

    this.registerServiceWorker();
    this.initPWAInstallPrompt();
    this.initTempleChimes();
  }

  /* ================= AUTHENTIC OPENING SEQUENCE CONTROLLER ================= */
  initOpeningSequence() {
    this.splashGateway = document.getElementById('splash-gateway');
    this.openingTitleStage = document.getElementById('opening-title-stage');
    this.openingVideoStage = document.getElementById('opening-video-stage');
    this.btnStartFullExperience = document.getElementById('btn-start-full-experience');
    this.btnEnterDirect = document.getElementById('btn-enter');
    this.btnSkipMontage = document.getElementById('btn-skip-montage');
    this.btnSkipToMontage = document.getElementById('btn-skip-to-montage');
    
    // Stacked Title Frames (S01 to S06)
    this.titleContainer = document.getElementById('opening-title-container');
    this.titleFrames = [
      document.getElementById('opening-title-img'),
      document.getElementById('title-frame-2'),
      document.getElementById('title-frame-3'),
      document.getElementById('title-frame-4'),
      document.getElementById('title-frame-5'),
      document.getElementById('title-frame-6')
    ];
    this.btnThemeSoundToggle = document.getElementById('btn-theme-sound-toggle');
    this.openingThemeAudio = document.getElementById('opening-theme-audio');

    // Stacked Mosaic Frames (01, 02, 03) & Montage Video
    this.mosaicContainer = document.getElementById('opening-mosaic-container');
    this.mosaicFrame01 = document.getElementById('mosaic-frame-01');
    this.mosaicFrame02 = document.getElementById('mosaic-frame-02');
    this.mosaicFrame03 = document.getElementById('mosaic-frame-03');
    this.mosaicVideoWindow = document.getElementById('mosaic-video-window');
    this.openingMontageVideo = document.getElementById('opening-montage-video');
    this.btnMontageSoundToggle = document.getElementById('btn-montage-sound-toggle');
    this.btnToggleTheaterMode = document.getElementById('btn-toggle-theater-mode');

    this.statusTitle = document.getElementById('opening-sequence-status-title');
    this.statusDesc = document.getElementById('opening-sequence-status-desc');
    this.progressFill = document.getElementById('opening-sequence-progress');
    this.btnReplayOpening = document.getElementById('btn-replay-opening');

    this.openingSequenceTimers = [];

    // 1. PRELOAD ALL OPENING IMAGES IN MEMORY FOR ZERO DISK LATENCY
    const preloadList = [
      'assets/images/opening/S01.jpg',
      'assets/images/opening/S02.jpg',
      'assets/images/opening/S03.jpg',
      'assets/images/opening/S04.jpg',
      'assets/images/opening/S05.jpg',
      'assets/images/opening/S06.jpg',
      'assets/images/opening/01.jpg',
      'assets/images/opening/02.jpg',
      'assets/images/opening/03.jpg'
    ];
    this.preloadedOpeningImages = preloadList.map(src => {
      const img = new Image();
      img.src = src;
      return img;
    });

    // Start autonomous landing page calligraphic dissolve (S01 to S06)
    this.startLandingAnimation();

    const clearAllTimers = () => {
      this.stopLandingAnimation();
      this.openingSequenceTimers.forEach(t => clearTimeout(t));
      this.openingSequenceTimers = [];
    };

    const enterApp = () => {
      clearAllTimers();
      if (this.openingMontageVideo) {
        this.openingMontageVideo.pause();
      }
      if (this.openingThemeAudio) {
        this.openingThemeAudio.pause();
      }
      if (this.splashGateway) this.splashGateway.classList.add('hidden');
      if (this.appShell) this.appShell.classList.remove('hidden');
      this.navigateToPage(1, false);
    };

    if (this.btnEnterDirect) {
      this.btnEnterDirect.addEventListener('click', enterApp);
    }
    if (this.btnSkipMontage) {
      this.btnSkipMontage.addEventListener('click', enterApp);
    }

    // Toggle Sound for Montage Video
    if (this.btnMontageSoundToggle && this.openingMontageVideo) {
      this.btnMontageSoundToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        this.openingMontageVideo.muted = !this.openingMontageVideo.muted;
        this.btnMontageSoundToggle.textContent = this.openingMontageVideo.muted ? '🔇 Sound: OFF' : '🔊 Sound: ON';
      });
    }

    // Toggle Music for Title Theme
    if (this.btnThemeSoundToggle && this.openingThemeAudio) {
      this.btnThemeSoundToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        this.openingThemeAudio.muted = !this.openingThemeAudio.muted;
        this.btnThemeSoundToggle.textContent = this.openingThemeAudio.muted ? '🔇 Music: OFF' : '🎵 Music: ON';
      });
    }

    // Toggle Expanded Theater / 1997 Mosaic Mode
    if (this.btnToggleTheaterMode && this.mosaicContainer) {
      this.btnToggleTheaterMode.addEventListener('click', (e) => {
        e.stopPropagation();
        const isTheater = this.mosaicContainer.classList.toggle('theater-mode');
        this.btnToggleTheaterMode.textContent = isTheater ? '🖼️ 1997 Mosaic Frame' : '🔲 Expand Theater';
      });
    }

    // PHASE 2: CULTURAL MOSAIC (03.bmp -> 02.bmp -> 01.bmp) & MONTAGE VIDEO
    const runMontagePhase = () => {
      clearAllTimers();
      if (this.openingTitleStage) this.openingTitleStage.classList.add('hidden');
      if (this.openingVideoStage) this.openingVideoStage.classList.remove('hidden');
      if (this.titleContainer) this.titleContainer.classList.add('hidden');
      if (this.mosaicContainer) this.mosaicContainer.classList.remove('hidden');

      if (this.btnSkipToMontage) {
        this.btnSkipToMontage.style.display = 'none';
      }

      // Prime video element inside synchronous click stack
      if (this.openingMontageVideo) {
        this.openingMontageVideo.muted = false;
        this.openingMontageVideo.load();
      }

      // Soft fade out of theme audio over 1.2s
      if (this.openingThemeAudio) {
        let vol = this.openingThemeAudio.volume;
        const fadeInterval = setInterval(() => {
          vol = Math.max(0, vol - 0.15);
          this.openingThemeAudio.volume = vol;
          if (vol <= 0) {
            clearInterval(fadeInterval);
            this.openingThemeAudio.pause();
          }
        }, 120);
      }

      // Step 2A: Display 03.bmp (Color Cultural Mosaic)
      if (this.mosaicFrame03) this.mosaicFrame03.classList.add('active');
      if (this.mosaicFrame02) this.mosaicFrame02.classList.remove('active');
      if (this.mosaicFrame01) this.mosaicFrame01.classList.remove('active');
      if (this.mosaicVideoWindow) this.mosaicVideoWindow.classList.remove('visible');

      if (this.statusTitle) this.statusTitle.textContent = "Authentic 1997 Cultural Mosaic";
      if (this.statusDesc) this.statusDesc.textContent = "Phase 2: Cultural Heritage Mosaic (03.bmp)";
      if (this.progressFill) this.progressFill.style.width = "35%";

      // Step 2B: Crossfade to 02.bmp (Sepia Transition Mosaic) at 1.2s
      const timer02 = setTimeout(() => {
        if (this.mosaicFrame02) this.mosaicFrame02.classList.add('active');
        if (this.mosaicFrame03) this.mosaicFrame03.classList.remove('active');
        if (this.mosaicFrame01) this.mosaicFrame01.classList.remove('active');
        if (this.statusDesc) this.statusDesc.textContent = "Phase 2: Transition Mosaic (02.bmp)";
        if (this.progressFill) this.progressFill.style.width = "40%";
      }, 1200);
      this.openingSequenceTimers.push(timer02);

      // Step 2C: Crossfade to 01.bmp (B&W Mosaic with Cutout) and Start Video at 2.4s
      const timer01 = setTimeout(() => {
        if (this.mosaicFrame01) this.mosaicFrame01.classList.add('active');
        if (this.mosaicFrame02) this.mosaicFrame02.classList.remove('active');
        if (this.mosaicFrame03) this.mosaicFrame03.classList.remove('active');
        if (this.mosaicVideoWindow) this.mosaicVideoWindow.classList.add('visible');

        if (this.statusTitle) this.statusTitle.textContent = "Authentic 1997 Archival Montage";
        if (this.statusDesc) this.statusDesc.textContent = "Phase 2: Archival Montage Video & Sanskrit Invocations (media/opening/montage.avi)";
        if (this.progressFill) this.progressFill.style.width = "45%";

        // Start video playback unmuted inside the 01.bmp cutout
        if (this.openingMontageVideo) {
          this.openingMontageVideo.currentTime = 0;
          this.openingMontageVideo.muted = false;
          this.openingMontageVideo.volume = 1.0;
          this.openingMontageVideo.play().catch(e => {
            console.log('Video play error:', e);
            if (this.openingMontageVideo.muted === false) {
              this.openingMontageVideo.muted = true;
              this.openingMontageVideo.play();
              if (this.btnMontageSoundToggle) {
                this.btnMontageSoundToggle.textContent = '🔇 Click to Unmute';
              }
            }
          });
        }
      }, 2400);
      this.openingSequenceTimers.push(timer01);

      // Video live progress bar & conclusion handlers
      if (this.openingMontageVideo) {
        this.openingMontageVideo.ontimeupdate = () => {
          if (this.openingMontageVideo.duration) {
            const vpct = this.openingMontageVideo.currentTime / this.openingMontageVideo.duration;
            const overallPct = Math.round(45 + vpct * 50);
            if (this.progressFill) this.progressFill.style.width = `${overallPct}%`;
          }
        };

        // Outro crossfade: 01.bmp -> 02.bmp -> 03.bmp -> enterApp()
        // Faithful to Director 6.0 ashmain1.dxr score timing (#myTimeOut: 2 Seconds at 12fps)
        this.openingMontageVideo.onended = () => {
          if (this.mosaicVideoWindow) this.mosaicVideoWindow.classList.remove('visible');
          if (this.statusTitle) this.statusTitle.textContent = "Authentic 1997 Archival Outro";
          if (this.statusDesc) this.statusDesc.textContent = "Phase 2 Outro: Concluding Archival Invocations (01.bmp)...";
          if (this.mosaicFrame01) this.mosaicFrame01.classList.add('active');
          if (this.mosaicFrame02) this.mosaicFrame02.classList.remove('active');
          if (this.mosaicFrame03) this.mosaicFrame03.classList.remove('active');

          const tOut1 = setTimeout(() => {
            if (this.statusDesc) this.statusDesc.textContent = "Phase 2 Outro: Transition Mosaic (02.bmp)...";
            if (this.mosaicFrame02) this.mosaicFrame02.classList.add('active');
            if (this.mosaicFrame01) this.mosaicFrame01.classList.remove('active');

            const tOut2 = setTimeout(() => {
              if (this.statusDesc) this.statusDesc.textContent = "Phase 2 Outro: Cultural Heritage Mosaic (03.bmp)...";
              if (this.mosaicFrame03) this.mosaicFrame03.classList.add('active');
              if (this.mosaicFrame02) this.mosaicFrame02.classList.remove('active');

              const tOut3 = setTimeout(() => {
                enterApp();
              }, 1800);
              this.openingSequenceTimers.push(tOut3);
            }, 1800);
            this.openingSequenceTimers.push(tOut2);
          }, 1800);
          this.openingSequenceTimers.push(tOut1);
        };
      }
    };

    if (this.btnSkipToMontage) {
      this.btnSkipToMontage.addEventListener('click', runMontagePhase);
    }

    // PHASE 1: ILLUMINATED TITLE CALLIGRAPHY (S01 to S06)
    const runAuthenticOpening = () => {
      clearAllTimers();
      if (this.openingTitleStage) this.openingTitleStage.classList.add('hidden');
      if (this.openingVideoStage) this.openingVideoStage.classList.remove('hidden');
      if (this.mosaicContainer) this.mosaicContainer.classList.add('hidden');
      if (this.titleContainer) this.titleContainer.classList.remove('hidden');

      if (this.btnSkipToMontage) {
        this.btnSkipToMontage.style.display = 'inline-flex';
      }

      if (this.statusTitle) this.statusTitle.textContent = "Ashtavadhanam — The Wonder that is Sanskrit";
      if (this.statusDesc) this.statusDesc.textContent = "Phase 1: Illuminated Title Calligraphy (S01 to S06)";
      if (this.progressFill) this.progressFill.style.width = "5%";

      // Play authentic Sanskrit title theme music (from ashmain.dxr)
      if (this.openingThemeAudio) {
        this.openingThemeAudio.currentTime = 0;
        this.openingThemeAudio.muted = false;
        this.openingThemeAudio.volume = 0.9;
        this.openingThemeAudio.play().catch(e => console.log('Theme audio play:', e));
      }

      // CRITICAL FOR BROWSER AUTOPLAY: Prime video element inside the synchronous user click event
      if (this.openingMontageVideo) {
        this.openingMontageVideo.muted = false;
        this.openingMontageVideo.load();
      }

      // Reset all title frames to inactive, frame 1 active
      this.titleFrames.forEach((frame, idx) => {
        if (!frame) return;
        if (idx === 0) {
          frame.classList.add('active');
        } else {
          frame.classList.remove('active');
        }
      });

      // Smooth progressive calligraphic dissolve sequence (every 750ms)
      const frameDelays = [0, 800, 1600, 2400, 3200, 4000];
      frameDelays.forEach((delay, idx) => {
        if (idx === 0) return; // already active
        const timer = setTimeout(() => {
          if (this.titleFrames[idx]) {
            this.titleFrames[idx].classList.add('active');
          }
          const pct = Math.round(5 + ((idx + 1) / 6) * 30);
          if (this.progressFill) this.progressFill.style.width = `${pct}%`;
          if (this.statusDesc) {
            this.statusDesc.textContent = `Illuminating Title Calligraphy — Stage ${idx + 1} of 6`;
          }

          // When S06 (final frame) is fully reached, hold for 2.2s then transition to Phase 2 (Montage Video)
          if (idx === 5) {
            const finishTimer = setTimeout(() => {
              runMontagePhase();
            }, 2200);
            this.openingSequenceTimers.push(finishTimer);
          }
        }, delay);
        this.openingSequenceTimers.push(timer);
      });
    };

    if (this.btnStartFullExperience) {
      this.btnStartFullExperience.addEventListener('click', runMontagePhase);
    }

    if (this.btnReplayOpening) {
      this.btnReplayOpening.addEventListener('click', () => {
        this.navDrawer.classList.remove('open');
        if (this.appShell) this.appShell.classList.add('hidden');
        if (this.splashGateway) this.splashGateway.classList.remove('hidden');
        if (this.openingVideoStage) this.openingVideoStage.classList.add('hidden');
        if (this.openingTitleStage) this.openingTitleStage.classList.remove('hidden');
        this.startLandingAnimation();
      });
    }

  }

  /* ================= AUTONOMOUS LANDING CALLIGRAPHIC ILLUMINATION ================= */
  startLandingAnimation() {
    this.stopLandingAnimation();
    this.landingFrames = [
      document.getElementById('landing-frame-1'),
      document.getElementById('landing-frame-2'),
      document.getElementById('landing-frame-3'),
      document.getElementById('landing-frame-4'),
      document.getElementById('landing-frame-5'),
      document.getElementById('landing-frame-6')
    ].filter(Boolean);

    if (this.landingFrames.length < 6) return;

    let step = 0;
    const playStep = () => {
      step = (step + 1) % 6;
      if (step === 0) {
        // Seamless crossfade reset: fade out layers 2-6 over 0.9s while frame 1 is already underneath
        this.landingFrames.forEach((f, i) => {
          if (i > 0) {
            f.classList.add('fade-reset');
            f.classList.remove('active');
          }
        });
        this.landingTimer = setTimeout(() => {
          this.landingFrames.forEach(f => f.classList.remove('fade-reset'));
          this.landingTimer = setTimeout(playStep, 500);
        }, 900);
        return;
      } else {
        this.landingFrames[step].classList.add('active');
      }

      // Fast fluid 260ms reveal per stage; 3200ms hold on complete illuminated S06
      const delay = (step === 5) ? 3200 : 260;
      this.landingTimer = setTimeout(playStep, delay);
    };

    // Begin fluid reveal after 600ms initial pause on frame 1
    this.landingTimer = setTimeout(playStep, 600);
  }

  stopLandingAnimation() {
    if (this.landingTimer) {
      clearTimeout(this.landingTimer);
      this.landingTimer = null;
    }
  }

  /* ================= RETURN TO MAIN LANDING PAGE ================= */
  returnToLandingPage() {
    try {
      if (window.Player && typeof window.Player.pause === 'function') {
        window.Player.pause();
      }
    } catch(err) {
      console.warn('Player pause on home return:', err);
    }
    if (document.fullscreenElement) {
      document.exitFullscreen().catch(() => {});
    }
    if (this.navDrawer) this.navDrawer.classList.remove('open');
    if (this.appShell) this.appShell.classList.add('hidden');
    if (this.splashGateway) this.splashGateway.classList.remove('hidden');
    if (this.openingVideoStage) this.openingVideoStage.classList.add('hidden');
    if (this.openingTitleStage) this.openingTitleStage.classList.remove('hidden');
    this.startLandingAnimation();
    window.scrollTo(0, 0);
  }

  /* ================= EXIT CONFIRMATION CONTROLLER (exit.dxr equivalent) ================= */
  initExitModal() {
    const exitModal = document.getElementById('exit-modal');
    const btnExit = document.getElementById('btn-exit');
    const btnCloseExit = document.getElementById('btn-close-exit');
    const btnCancelExit = document.getElementById('btn-cancel-exit');
    const btnConfirmExit = document.getElementById('btn-confirm-exit');
    const exitBackdrop = document.getElementById('exit-modal-backdrop');

    const showExitModal = (e) => {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      this.navDrawer.classList.remove('open');
      if (exitModal) exitModal.classList.remove('hidden');
    };

    const hideExitModal = (e) => {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      if (exitModal) exitModal.classList.add('hidden');
    };

    if (btnExit) btnExit.addEventListener('click', showExitModal);
    if (btnCloseExit) btnCloseExit.addEventListener('click', hideExitModal);
    if (btnCancelExit) btnCancelExit.addEventListener('click', hideExitModal);
    if (exitBackdrop) exitBackdrop.addEventListener('click', hideExitModal);

    // Escape key listener to close exit modal
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && exitModal && !exitModal.classList.contains('hidden')) {
        hideExitModal(e);
      }
    });

    if (btnConfirmExit) {
      btnConfirmExit.addEventListener('click', (e) => {
        if (e) {
          e.preventDefault();
          e.stopPropagation();
        }
        hideExitModal();
        try {
          if (window.Player) {
            if (typeof window.Player.pause === 'function') {
              window.Player.pause();
            } else if (window.Player.audio) {
              window.Player.audio.pause();
            }
          }
        } catch(err) {
          console.warn('Player pause on exit:', err);
        }
        if (document.fullscreenElement) {
          document.exitFullscreen().catch(() => {});
        }
        if (this.navDrawer) this.navDrawer.classList.remove('open');
        if (this.appShell) this.appShell.classList.add('hidden');
        if (this.splashGateway) this.splashGateway.classList.remove('hidden');
        if (this.openingVideoStage) this.openingVideoStage.classList.add('hidden');
        if (this.openingTitleStage) this.openingTitleStage.classList.remove('hidden');
        window.scrollTo(0, 0);
        try { window.close(); } catch(err) {}
      });
    }
  }

  /* ================= TREATISE CHAPTER READERS ================= */
  initAvadhanaReader() {
    const avadhana = this.data.treatises && this.data.treatises.avadhanaKala;
    const chapters = (avadhana && avadhana.chapters) || [];
    const pillsContainer = document.getElementById('avadhana-pills');
    if (!pillsContainer || chapters.length === 0) return;

    pillsContainer.innerHTML = '';
    chapters.forEach((ch, idx) => {
      const btn = document.createElement('button');
      btn.className = `chapter-pill ${idx === 0 ? 'active' : ''}`;
      btn.textContent = `Ch ${ch.chapter}`;
      btn.title = ch.title;
      btn.addEventListener('click', () => this.showAvadhanaChapter(idx));
      pillsContainer.appendChild(btn);
    });

    const btnPrev = document.getElementById('btn-avadhana-prev');
    const btnNext = document.getElementById('btn-avadhana-next');
    if (btnPrev) {
      btnPrev.addEventListener('click', () => {
        if (this.currentAvadhanaIndex > 0) this.showAvadhanaChapter(this.currentAvadhanaIndex - 1);
      });
    }
    if (btnNext) {
      btnNext.addEventListener('click', () => {
        if (this.currentAvadhanaIndex < chapters.length - 1) this.showAvadhanaChapter(this.currentAvadhanaIndex + 1);
      });
    }

    this.showAvadhanaChapter(0);
  }

  showAvadhanaChapter(index) {
    const chapters = this.data.treatises && this.data.treatises.avadhanaKala && this.data.treatises.avadhanaKala.chapters;
    if (!chapters || !chapters[index]) return;

    this.currentAvadhanaIndex = index;
    const ch = chapters[index];

    // Update pills
    document.querySelectorAll('#avadhana-pills .chapter-pill').forEach((p, idx) => {
      p.classList.toggle('active', idx === index);
    });

    // Update canvas & text
    const imgEl = document.getElementById('avadhana-canvas-img');
    const capEl = document.getElementById('avadhana-canvas-caption');
    const titleEl = document.getElementById('avadhana-chapter-title');
    const contentEl = document.getElementById('content-avadhanaKala');
    const indEl = document.getElementById('avadhana-page-indicator');

    const avadhanaTitlesSa = [
      'प्रथमः परिच्छेदः • अवधानस्वरूपम्',
      'द्वितीयः परिच्छेदः • अवधानस्येतिहासः',
      'तृतीयः परिच्छेदः • अष्टावधानाङ्गानि',
      'चतुर्थः परिच्छेदः • निषिद्धाक्षरी',
      'पञ्चमः परिच्छेदः • समस्यापूर्तिः',
      'षष्ठः परिच्छेदः • दत्तपदी',
      'सप्तमः परिच्छेदः • सङ्ख्यावलोकनानि'
    ];
    const titleSaEl = document.getElementById('avadhana-chapter-title-sa');
    if (titleSaEl) titleSaEl.textContent = avadhanaTitlesSa[index] || '';

    if (imgEl) imgEl.src = ch.canvas;
    if (capEl) capEl.textContent = `Original Director Canvas: ${ch.canvas.split('/').pop()} • Chapter ${ch.chapter} of 7`;
    if (titleEl) titleEl.textContent = ch.title;
    if (contentEl) contentEl.innerHTML = ch.content.map(p => `<p>${this.formatText(p)}</p>`).join('');
    if (indEl) indEl.textContent = `Chapter ${ch.chapter} of ${chapters.length}`;
  }

  initConcentrationReader() {
    const conc = this.data.treatises && this.data.treatises.concentration;
    const pages = (conc && conc.pages) || [];
    const pillsContainer = document.getElementById('concentration-pills');
    if (!pillsContainer || pages.length === 0) return;

    pillsContainer.innerHTML = '';
    pages.forEach((pg, idx) => {
      const btn = document.createElement('button');
      btn.className = `chapter-pill ${idx === 0 ? 'active' : ''}`;
      btn.textContent = `Page ${pg.page}`;
      btn.title = pg.title;
      btn.addEventListener('click', () => this.showConcentrationPage(idx));
      pillsContainer.appendChild(btn);
    });

    const btnPrev = document.getElementById('btn-concentration-prev');
    const btnNext = document.getElementById('btn-concentration-next');
    if (btnPrev) {
      btnPrev.addEventListener('click', () => {
        if (this.currentConcentrationIndex > 0) this.showConcentrationPage(this.currentConcentrationIndex - 1);
      });
    }
    if (btnNext) {
      btnNext.addEventListener('click', () => {
        if (this.currentConcentrationIndex < pages.length - 1) this.showConcentrationPage(this.currentConcentrationIndex + 1);
      });
    }

    this.showConcentrationPage(0);
  }

  showConcentrationPage(index) {
    const pages = this.data.treatises && this.data.treatises.concentration && this.data.treatises.concentration.pages;
    if (!pages || !pages[index]) return;

    this.currentConcentrationIndex = index;
    const pg = pages[index];

    // Update pills
    document.querySelectorAll('#concentration-pills .chapter-pill').forEach((p, idx) => {
      p.classList.toggle('active', idx === index);
    });

    // Update canvas & text
    const imgEl = document.getElementById('concentration-canvas-img');
    const capEl = document.getElementById('concentration-canvas-caption');
    const titleEl = document.getElementById('concentration-chapter-title');
    const titleSaEl = document.getElementById('concentration-chapter-title-sa');
    const contentEl = document.getElementById('content-concentration');
    const indEl = document.getElementById('concentration-page-indicator');

    const concentrationTitlesSa = [
      'प्रथमः पृष्ठः • धारणास्वरूपम्',
      'द्वितीयः पृष्ठः • एकाग्रता',
      'तृतीयः पृष्ठः • अभ्यासयोगः',
      'चतुर्थः पृष्ठः • मनःसंयमः',
      'पञ्चमः पृष्ठः • स्मरणशक्तिः',
      'षष्ठः पृष्ठः • फलश्रुतिः'
    ];
    if (titleSaEl) titleSaEl.textContent = concentrationTitlesSa[index] || '';

    if (imgEl) imgEl.src = pg.canvas;
    if (capEl) capEl.textContent = `Original Director Canvas: ${pg.canvas.split('/').pop()} • Page ${pg.page} of 6`;
    if (titleEl) titleEl.textContent = pg.title;
    if (contentEl) contentEl.innerHTML = pg.content.map(p => `<p>${this.formatText(p)}</p>`).join('');
    if (indEl) indEl.textContent = `Page ${pg.page} of ${pages.length}`;
  }

  /* ================= HISTORICAL ARTWORK GALLERY ================= */
  renderHistoricalGallery() {
    const grid = document.getElementById('historical-gallery-grid');
    if (!grid) return;

    const galleryItems = [
      { title: 'Opening Frame 1 (S01)', category: 'Title Animation', src: 'assets/images/opening/S01.jpg' },
      { title: 'Opening Frame 2 (S02)', category: 'Title Animation', src: 'assets/images/opening/S02.jpg' },
      { title: 'Opening Frame 3 (S03)', category: 'Title Animation', src: 'assets/images/opening/S03.jpg' },
      { title: 'Opening Frame 4 (S04)', category: 'Title Animation', src: 'assets/images/opening/S04.jpg' },
      { title: 'Opening Frame 5 (S05)', category: 'Title Animation', src: 'assets/images/opening/S05.jpg' },
      { title: 'Opening Frame 6 (S06)', category: 'Title Animation', src: 'assets/images/opening/S06.jpg' },
      { title: 'Cultural Heritage Mosaic (01)', category: 'Opening Video Frame', src: 'assets/images/opening/01.jpg' },
      { title: 'Supplementary Mosaic (02)', category: 'Opening Visuals', src: 'assets/images/opening/02.jpg' },
      { title: 'Supplementary Mosaic (03)', category: 'Opening Visuals', src: 'assets/images/opening/03.jpg' },
      { title: 'Scholars Assembly 1997', category: 'Historic Photography', src: 'assets/images/performance.jpg' },
      { title: 'Participating Institutions', category: 'Indology Registry', src: 'assets/images/institution/institution .jpg' },
      { title: 'Sri Aurobindo Society Office', category: 'Historic Archives', src: 'assets/images/sas/sas.jpg' },
      { title: 'Acknowledgments Illumination', category: 'Master Credits Backdrop', src: 'assets/images/acknowledge/back.jpg' },
      { title: 'Avadhana Kala Canvas 1', category: 'Treatise Master', src: 'assets/images/avdhankala01.jpg' },
      { title: 'Avadhana Kala Canvas 2', category: 'Treatise Master', src: 'assets/images/avdhankala02.jpg' },
      { title: 'Avadhana Kala Canvas 3', category: 'Treatise Master', src: 'assets/images/avdhankala03.jpg' },
      { title: 'Avadhana Kala Canvas 4', category: 'Treatise Master', src: 'assets/images/avdhankala04.jpg' },
      { title: 'Avadhana Kala Canvas 5', category: 'Treatise Master', src: 'assets/images/avdhankala05.jpg' },
      { title: 'Avadhana Kala Canvas 6', category: 'Treatise Master', src: 'assets/images/avdhankala06.jpg' },
      { title: 'Avadhana Kala Canvas 7', category: 'Treatise Master', src: 'assets/images/avdhankala07.jpg' },
      { title: 'Concentration Canvas 1', category: 'Philosophy Master', src: 'assets/images/ashtava01.jpg' },
      { title: 'Concentration Canvas 2', category: 'Philosophy Master', src: 'assets/images/ashtava02.jpg' },
      { title: 'Concentration Canvas 3', category: 'Philosophy Master', src: 'assets/images/ashtava03.jpg' },
      { title: 'Concentration Canvas 4', category: 'Philosophy Master', src: 'assets/images/ashtava04.jpg' },
      { title: 'Concentration Canvas 5', category: 'Philosophy Master', src: 'assets/images/ashtava05.jpg' },
      { title: 'Concentration Canvas 6', category: 'Philosophy Master', src: 'assets/images/ashtava06.jpg' }
    ];

    // Add all 25 Round Performance Stage Canvases (eightfold 01 to 25)
    for (let r = 1; r <= 25; r++) {
      const pad = r < 10 ? `0${r}` : `${r}`;
      galleryItems.push({
        title: `Round ${r} Performance Canvas`,
        category: 'Eightfold Performance Stage',
        src: `assets/images/eightfold ${pad}.jpg`
      });
    }

    grid.innerHTML = galleryItems.map(item => `
      <div class="gallery-item-card">
        <img class="gallery-img-thumb" src="${item.src}" alt="${item.title}" loading="lazy" onclick="window.open('${item.src}', '_blank')">
        <div class="gallery-item-info">
          <span class="gallery-item-title">${item.title}</span>
          <span class="gallery-item-meta">${item.category} • ${item.src.split('/').pop()}</span>
        </div>
      </div>
    `).join('');
  }

  /* ================= TOUCH & NAVIGATION ================= */
  initTouchGestures() {
    let touchStartX = 0;
    let touchStartY = 0;
    const stage = document.getElementById('stage-container');
    if (!stage) return;

    stage.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
      touchStartY = e.changedTouches[0].screenY;
    }, { passive: true });

    stage.addEventListener('touchend', (e) => {
      const touchEndX = e.changedTouches[0].screenX;
      const touchEndY = e.changedTouches[0].screenY;
      const diffX = touchEndX - touchStartX;
      const diffY = touchEndY - touchStartY;

      if (Math.abs(diffX) > 60 && Math.abs(diffX) > Math.abs(diffY) * 1.5) {
        if (diffX < 0 && this.currentPageIndex < 24) {
          this.navigateToPage(this.currentPageIndex + 2, false);
        } else if (diffX > 0 && this.currentPageIndex > 0) {
          this.navigateToPage(this.currentPageIndex, false);
        }
      }
    }, { passive: true });
  }

  setDisplayView(view) {
    document.body.classList.remove('mode-devanagari', 'mode-english', 'mode-bilingual');
    document.body.classList.add(`mode-${view}`);
    
    document.querySelectorAll('.view-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.view === view);
    });
  }

  navigateToSection(sectionId) {
    const previousSection = this.currentSection;
    this.currentSection = sectionId;
    document.querySelectorAll('.app-section').forEach(sec => {
      sec.classList.remove('active');
    });
    const target = document.getElementById(`section-${sectionId}`);
    if (target) target.classList.add('active');

    document.querySelectorAll('.nav-link').forEach(link => {
      link.classList.toggle('active', link.dataset.section === sectionId);
    });

    if (previousSection !== sectionId && (sectionId === 'avadhanaKala' || sectionId === 'concentration')) {
      this.playTempleChime();
    }
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  renderRoundPills() {
    this.roundPillsContainer.innerHTML = '';
    for (let i = 1; i <= 25; i++) {
      const pill = document.createElement('button');
      pill.className = `round-pill ${i === 1 ? 'active' : ''}`;
      pill.textContent = `Page ${i}`;
      pill.title = `Page ${i} of 25`;
      pill.setAttribute('role', 'tab');
      pill.setAttribute('aria-selected', i === 1 ? 'true' : 'false');
      pill.setAttribute('aria-label', `Page ${i} of 25`);
      pill.addEventListener('click', () => this.navigateToPage(i, false));
      this.roundPillsContainer.appendChild(pill);
    }
  }

  navigateToPage(pageNumber, autoPlayFirst = false) {
    this.currentPageIndex = pageNumber - 1;
    const pageData = this.data.pages[this.currentPageIndex];
    if (!pageData) return;

    // Update pills active
    document.querySelectorAll('.round-pill').forEach((pill, idx) => {
      const isCur = (idx === this.currentPageIndex);
      pill.classList.toggle('active', isCur);
      pill.setAttribute('aria-selected', isCur ? 'true' : 'false');
      if (isCur) {
        if (pageNumber === 1 && this.roundPillsContainer) {
          this.roundPillsContainer.scrollLeft = 0;
        } else {
          pill.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        }
      }
    });

    // Update Page Title & Meta
    this.currentRoundTitle.textContent = `Page ${pageNumber} of 25`;
    this.currentRoundMeta.textContent = `${pageData.audioCount} Audio Recitations ${pageData.video ? '• Video Demonstration Available' : ''}`;

    // Update prev/next navigation arrow states and tooltips
    const prevBtn = document.getElementById('btn-round-prev');
    const nextBtn = document.getElementById('btn-round-next');
    if (prevBtn) {
      prevBtn.title = pageNumber > 1 ? `Previous: Page ${pageNumber - 1}` : 'First Page';
      prevBtn.style.opacity = pageNumber > 1 ? '1' : '0.4';
      prevBtn.style.pointerEvents = pageNumber > 1 ? 'auto' : 'none';
      prevBtn.setAttribute('aria-disabled', pageNumber > 1 ? 'false' : 'true');
    }
    if (nextBtn) {
      nextBtn.title = pageNumber < 25 ? `Next: Page ${pageNumber + 1}` : 'Final Page';
      nextBtn.style.opacity = pageNumber < 25 ? '1' : '0.4';
      nextBtn.style.pointerEvents = pageNumber < 25 ? 'auto' : 'none';
      nextBtn.setAttribute('aria-disabled', pageNumber < 25 ? 'false' : 'true');
    }

    // Background Canvas Artwork & Safe Zone Layout
    const canvasImg = document.getElementById('stage-canvas-bg');
    if (canvasImg) {
      canvasImg.src = pageData.canvas;
      canvasImg.alt = `Page ${pageNumber} Stage Canvas (${pageData.canvas.split('/').pop()})`;
    }
    this.dialoguesWrapper.style.backgroundImage = 'none';

    // Apply artwork safe zone classification based on corner illustrations
    this.dialoguesWrapper.classList.remove('art-left', 'art-right', 'art-center');
    if ([1, 5, 11, 12, 15, 18, 19].includes(pageNumber)) {
      this.dialoguesWrapper.classList.add('art-left');
    } else if ([2, 9].includes(pageNumber)) {
      this.dialoguesWrapper.classList.add('art-right');
    } else {
      this.dialoguesWrapper.classList.add('art-center');
    }

    // Video button
    if (pageData.video) {
      this.btnWatchVideo.classList.remove('hidden');
      this.btnWatchVideo.onclick = () => {
        window.Player.openVideoModal(pageData.video, `Page ${pageNumber} Video Demonstration`);
      };
    } else {
      this.btnWatchVideo.classList.add('hidden');
    }

    // Parse dialogues and build cards
    this.renderDialogues(pageData);

    // Make sure we are on performance section
    if (this.currentSection !== 'performance') {
      this.navigateToSection('performance');
    }

    if (autoPlayFirst && window.Player) {
      window.Player.playClip(0);
    }
  }

  parseDialogueTurns(pageData) {
    const rawSan = (pageData.sanskritDevanagari || '').trim();
    const rawEng = (pageData.englishText || '').trim();

    const sanParas = rawSan.split(/\n\n+/).map(s => s.trim()).filter(Boolean);
    const engParas = rawEng.split(/\n\n+/).map(s => s.trim()).filter(Boolean);
    // Authentic speaker headers (excluding sound cues like The Bell / Ghaṇṭā so cues remain contextual with their turns)
    const speakerHeaderPat = /^(Avadhānī|Niṣiddhākṣarī|Aprastutaprasaṅga|Aprastutaprasanga|Samasyā|Dattapadī|Vyastākṣarī|President|Commentator):/i;

    const engTurns = [];
    let curEng = [];
    for (const p of engParas) {
      if (speakerHeaderPat.test(p)) {
        if (curEng.length > 0) {
          // If engTurns is still empty, and curEng doesn't start with a speaker header,
          // it is an intro stage direction for the first speaker, so keep it with curEng
          if (engTurns.length === 0 && !speakerHeaderPat.test(curEng[0])) {
            curEng.push(p);
          } else {
            engTurns.push(curEng.join('\n\n'));
            curEng = [p];
          }
        } else {
          curEng.push(p);
        }
      } else {
        curEng.push(p);
      }
    }
    if (curEng.length > 0) engTurns.push(curEng.join('\n\n'));

    return { sanTurns: sanParas, engTurns };
  }

  renderDialogues(pageData) {
    this.dialoguesWrapper.innerHTML = '';
    const audioFiles = pageData.audioFiles || [];

    const { sanTurns, engTurns } = this.parseDialogueTurns(pageData);
    const maxLines = Math.max(audioFiles.length, sanTurns.length, engTurns.length, 1);
    const playlist = [];

    for (let i = 0; i < maxLines; i++) {
      const audio = audioFiles[i];
      const san = sanTurns[i] || '';
      const eng = engTurns[i] || '';

      // SUPPRESS PHANTOM CARDS:
      // If there is no recitation (no Sanskrit and no audio file), do NOT create an empty dialogue card!
      if (!san.trim() && !audio) {
        // If there is English commentary/footnote text, attach it as an annotation to the preceding card
        if (eng && this.dialoguesWrapper.lastElementChild) {
          const prevBody = this.dialoguesWrapper.lastElementChild.querySelector('.dialogue-body');
          if (prevBody) {
            const cleanNote = eng.replace(/^(Commentator|President):\s*/i, '').trim();
            const noteEl = document.createElement('div');
            noteEl.className = 'text-english dialogue-footnote';
            noteEl.style.marginTop = '8px';
            noteEl.style.fontStyle = 'italic';
            noteEl.style.opacity = '0.85';
            noteEl.innerHTML = this.formatText(cleanNote);
            prevBody.appendChild(noteEl);
          }
        }
        continue; // Suppress empty card
      }

      const speakerInfo = this.detectSpeaker(san, eng);

      const card = document.createElement('div');
      card.className = 'dialogue-card';
      card.dataset.index = i;

      let audioButtonHtml = '';
      if (audio) {
        audioButtonHtml = `<button class="dialogue-audio-btn" data-clip="${i}" title="Play recitation">▶</button>`;
        playlist.push({
          id: audio.id,
          m4a: audio.m4a,
          mp3: audio.mp3,
          speaker: speakerInfo.name,
          title: `Page ${pageData.pageNumber} — Turn ${i + 1}`
        });
      }

      // Strip redundant leading speaker prefix since speaker badge is already rendered above
      const cleanSan = san.replace(/^(अवधानी|निषिद्धाक्षरी|नष्िाधाक्षरी|अप्रस्तुतप्रसङ्गः?|अप्रस्तुतप्रसङ्ग|समस्या|दत्तपदी|व्यस्ताक्षरी|व्याख्याकारः?|सभापतिः?|घण्टा):\s*/i, '').trim();
      const cleanEng = eng.replace(/^(Avadhānī|Niṣiddhākṣarī|Aprastutaprasaṅga|Aprastutaprasanga|Samasyā|Dattapadī|Vyastākṣarī|Commentator|President|The Bell|Ghaṇṭā):\s*/i, '').trim();

      // Single-syllable / brief banter responses (e.g. Card 3 'अ', 'र्त्य', 'लो')
      const isCompactTurn = cleanSan.length > 0 && cleanSan.length <= 4 && !cleanSan.includes('\n');
      if (isCompactTurn) {
        card.classList.add('compact-turn');
        card.innerHTML = `
          <div class="dialogue-header compact-header">
            <div class="speaker-seal-wrap">
              <span class="speaker-seal ${speakerInfo.cssClass}">〔 ${speakerInfo.name} 〕</span>
              <span class="compact-turn-subtitle">✦ प्रथमाक्षरम् • First Syllable Turn</span>
            </div>
            ${audioButtonHtml}
          </div>
          <div class="dialogue-body compact-body">
            <div class="text-sanskrit akshara-hero">${this.formatText(cleanSan)}</div>
            ${cleanEng ? `<div class="text-english">${this.formatText(cleanEng)}</div>` : ''}
          </div>
        `;
      } else {
        card.innerHTML = `
          <div class="dialogue-header">
            <span class="speaker-seal ${speakerInfo.cssClass}">〔 ${speakerInfo.name} 〕</span>
            ${audioButtonHtml}
          </div>
          <div class="dialogue-body">
            <div class="text-sanskrit">${this.formatSanskritVerse(cleanSan)}</div>
            ${cleanEng ? `<div class="text-english">${this.formatText(cleanEng)}</div>` : ''}
          </div>
        `;
      }

      const btn = card.querySelector('.dialogue-audio-btn');
      if (btn) {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          window.Player.playClip(i);
        });
      }
      card.addEventListener('click', () => {
        if (audio) window.Player.playClip(i);
      });

      this.dialoguesWrapper.appendChild(card);
    }

    if (window.Player) {
      window.Player.setPlaylist(playlist);
    }

    // Manage scroll hint pill visibility when content overflows
    const scrollHint = document.getElementById('scroll-hint-pill');
    if (scrollHint) {
      setTimeout(() => {
        if (this.dialoguesWrapper.scrollHeight > this.dialoguesWrapper.clientHeight + 25) {
          scrollHint.classList.remove('hidden');
          scrollHint.style.opacity = '1';
        } else {
          scrollHint.classList.add('hidden');
        }
      }, 120);

      this.dialoguesWrapper.onscroll = () => {
        if (this.dialoguesWrapper.scrollTop > 20) {
          scrollHint.style.opacity = '0';
          setTimeout(() => {
            if (this.dialoguesWrapper.scrollTop > 20) scrollHint.classList.add('hidden');
          }, 350);
        } else if (this.dialoguesWrapper.scrollHeight > this.dialoguesWrapper.clientHeight + 25) {
          scrollHint.classList.remove('hidden');
          scrollHint.style.opacity = '1';
        }
      };
    }
  }

  detectSpeaker(sanText, engText) {
    const combined = `${sanText || ''}\n${engText || ''}`.trim();
    const firstLines = combined.split('\n').slice(0, 3).join(' ').trim();

    if (/^(अवधानी|avadhānī|avadhani)/i.test(firstLines) || /^अवधानी:/i.test(sanText || '')) {
      return { name: 'अवधानी • Avadhānī', cssClass: 'speaker-avadhani' };
    }
    if (/^(निषिद्धाक्षरी|नष्िाधाक्षरी|niṣiddhākṣarī|nishiddha)/i.test(firstLines) || /^निषिद्धाक्षरी:/i.test(sanText || '')) {
      return { name: 'निषिद्धाक्षरी • Niṣiddhākṣarī', cssClass: 'speaker-nishidha' };
    }
    if (/^(अप्रस्तुतप्रसङ्ग|aprastuta)/i.test(firstLines) || /^अप्रस्तुत/i.test(sanText || '')) {
      return { name: 'अप्रस्तुतप्रसङ्ग • Aprastutaprasaṅga', cssClass: 'speaker-aprastuta' };
    }
    if (/^(समस्या|samasyā|samasya)/i.test(firstLines) || /^समस्या/i.test(sanText || '')) {
      return { name: 'समस्या • Samasyā', cssClass: 'speaker-samasya' };
    }
    if (/^(दत्तपदी|dattapadī|dattapadi)/i.test(firstLines) || /^दत्तपदी/i.test(sanText || '')) {
      return { name: 'दत्तपदी • Dattapadī', cssClass: 'speaker-dattapadi' };
    }
    if (/^(व्यस्ताक्षरी|vyastākṣarī|vyastakshari)/i.test(firstLines) || /^व्यस्ताक्षरी/i.test(sanText || '')) {
      return { name: 'व्यस्ताक्षरी • Vyastākṣarī', cssClass: 'speaker-vyastakshari' };
    }
    if (/^(घण्टा|the bell|ghaṇṭā|bell|🔔)/i.test(firstLines) || /^🔔/i.test(sanText || '')) {
      return { name: 'घण्टा • The Bell (Ghaṇṭā)', cssClass: 'speaker-bell' };
    }
    if (/^(सभापति|president|अध्यक्ष)/i.test(firstLines) || /^सभापति/i.test(sanText || '')) {
      return { name: 'सभापति • President', cssClass: 'speaker-president' };
    }
    if (/^(व्याख्याकार|commentator)/i.test(firstLines) || /^व्याख्याकार/i.test(sanText || '')) {
      return { name: 'व्याख्याकार • Commentator', cssClass: 'speaker-default' };
    }

    const pfx = firstLines.slice(0, 50).toLowerCase();
    if (pfx.includes('niṣiddhākṣarī') || pfx.includes('निषिद्धाक्षरी') || pfx.includes('nishiddha')) {
      return { name: 'निषिद्धाक्षरी • Niṣiddhākṣarī', cssClass: 'speaker-nishidha' };
    }
    if (pfx.includes('aprastuta') || pfx.includes('अप्रस्तुत')) {
      return { name: 'aprastutaprasaṅga • Aprastuta', cssClass: 'speaker-aprastuta' };
    }
    if (pfx.includes('samasyā') || pfx.includes('समस्या') || pfx.includes('samasya')) {
      return { name: 'समस्या • Samasyā', cssClass: 'speaker-samasya' };
    }
    if (pfx.includes('dattapadī') || pfx.includes('दत्तपदी') || pfx.includes('dattapadi')) {
      return { name: 'दत्तपदी • Dattapadī', cssClass: 'speaker-dattapadi' };
    }
    if (pfx.includes('vyastākṣarī') || pfx.includes('व्यस्ताक्षरी')) {
      return { name: 'व्यस्ताक्षरी • Vyastākṣarī', cssClass: 'speaker-vyastakshari' };
    }
    if (pfx.includes('bell') || pfx.includes('घण्टा') || pfx.includes('ghaṇṭā') || pfx.includes('🔔')) {
      return { name: 'घण्टा • The Bell (Ghaṇṭā)', cssClass: 'speaker-bell' };
    }
    if (pfx.includes('avadhānī') || pfx.includes('अवधानी') || pfx.includes('avadhani')) {
      return { name: 'अवधानी • Avadhānī', cssClass: 'speaker-avadhani' };
    }
    return { name: 'विद्वत्सभा • Assembly', cssClass: 'speaker-default' };
  }

  formatText(str) {
    return str.replace(/\n/g, '<br>');
  }

  cleanSanskritTypography(text) {
    if (!text) return '';
    // Normalize multiple spaces into single space while preserving intentional newlines
    let s = text.replace(/[ \t]+/g, ' ');
    // Prevent danda (। or ॥) from wrapping to start of a newline by using non-breaking space
    s = s.replace(/\s+([।॥])/g, '\u00A0$1');
    return s;
  }

  isMetricVerse(str) {
    if (!str) return false;
    // Conversational dialogue cues indicate prose (Gadya)
    if (/[?!—;:]|---|\(घण्टा|\(विहस्य|अहं मन्ये|श्रुतं वा/i.test(str)) {
      return false;
    }
    const lines = str.split('\n').map(l => l.trim()).filter(Boolean);
    if (lines.length < 2) return false;
    const hasDanda = lines.some(l => /[।॥]/.test(l)) || str.includes('॥') || str.includes('।।');
    return hasDanda && (lines.length === 2 || lines.length === 4 || lines.length >= 6);
  }

  formatSanskritVerse(str) {
    if (!str) return '';
    const cleaned = this.cleanSanskritTypography(str);
    if (this.isMetricVerse(cleaned)) {
      const rawLines = cleaned.split('\n').map(l => l.trim()).filter(Boolean);
      return rawLines.map((line, idx) => {
        const isEvenPada = (idx % 2 === 1);
        const padaClass = isEvenPada ? 'verse-line pada-even' : 'verse-line pada-odd';
        return `<span class="${padaClass}">${line}</span>`;
      }).join('');
    }
    // Clean prose dialogue (Gadya) with standard paragraph wrapping and left alignment
    return this.formatText(cleaned);
  }

  renderTreatises() {
    const t = this.data.treatises;
    if (!t) return;

    if (t.performanceDetails && document.getElementById('content-scholars')) {
      document.getElementById('content-scholars').innerHTML = t.performanceDetails.content.map(p => `<p>${this.formatText(p)}</p>`).join('');
    }
    if (t.institutions && document.getElementById('content-institutions')) {
      document.getElementById('content-institutions').innerHTML = t.institutions.content.map(p => `<p>${this.formatText(p)}</p>`).join('');
    }
    if (t.sriAurobindoSociety && document.getElementById('content-society')) {
      document.getElementById('content-society').innerHTML = t.sriAurobindoSociety.content.map(p => `<p>${this.formatText(p)}</p>`).join('');
    }
  }

  /* ================= ACKNOWLEDGMENTS (acknowledge.dxr / acknowledge.cxt) ================= */
  renderAcknowledgments() {
    const cred = this.data.credits;
    const container = document.getElementById('content-acknowledgments');
    if (!container || !cred) return;

    container.innerHTML = `
      <div class="ack-section">
        <h3 class="ack-heading">${cred.acknowledgments}</h3>
        <div class="ack-patrons-grid">
          ${cred.patrons.map(p => `<div class="ack-patron-badge">🏛️ ${p}</div>`).join('')}
        </div>
      </div>

      <div class="ack-section">
        <h3 class="ack-heading">Participants of the Ashtavadhanam at Pondicherry (अष्टावधानस्य विद्वांसः)</h3>
        <div class="ack-participants-table-wrapper">
          <table class="ack-table">
            <thead>
              <tr>
                <th>Role / भूमिका</th>
                <th>Scholar / नाम तथा परिचयः</th>
              </tr>
            </thead>
            <tbody>
              ${cred.participants.map(pt => `
                <tr>
                  <td class="ack-role-cell">${pt.role}</td>
                  <td class="ack-name-cell">${pt.name}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>

      <div class="ack-grid-2col">
        <div class="ack-section">
          <h3 class="ack-heading">The Creative Team (सृजनात्मक-दलम्)</h3>
          <ul class="ack-name-list">
            ${cred.creativeTeam.map(m => `<li>✦ ${m}</li>`).join('')}
          </ul>
        </div>

        <div class="ack-section">
          <h3 class="ack-heading">Music & Audio (संगीतम्)</h3>
          <ul class="ack-name-list">
            ${cred.music.map(m => `<li>🎵 ${m}</li>`).join('')}
          </ul>

          <h3 class="ack-heading" style="margin-top: 24px;">Technical Group (तान्त्रिक-दलम्)</h3>
          <ul class="ack-name-list">
            ${cred.technicalGroup.map(g => `<li>⚙️ ${g}</li>`).join('')}
          </ul>
        </div>
      </div>
    `;
  }

  /* ================= GUIDE & HELP (help.dxr / help.cxt / help.swf) ================= */
  renderHelp() {
    const h = this.data.help;
    const container = document.getElementById('content-help');
    if (!container || !h) return;

    container.innerHTML = `
      <div class="help-section modern-guide-section">
        <h3 class="help-heading">Modern Multimedia Experience Guide (उपयोग-मार्गदर्शिका)</h3>
        <div class="help-cards-grid">
          ${h.modernGuide.sections.map(s => `
            <div class="help-guide-card">
              <h4>${s.heading}</h4>
              <p>${s.content}</p>
            </div>
          `).join('')}
        </div>
      </div>

      <div class="help-section archival-guide-section">
        <h3 class="help-heading">${h.archivalManual.heading}</h3>
        <p class="help-note"><em>${h.archivalManual.historicalNote}</em></p>
        
        <div class="help-archival-grid">
          <div class="help-archival-box">
            <h4>Historic 1997 System Requirements</h4>
            <ul>
              ${h.archivalManual.specifications.map(spec => `<li>🖥️ ${spec}</li>`).join('')}
            </ul>
          </div>
          <div class="help-archival-box">
            <h4>Original CD-ROM Navigation Controls</h4>
            <ul>
              ${h.archivalManual.historicalNavigation.map(nav => `<li>🧭 ${nav}</li>`).join('')}
            </ul>
          </div>
        </div>
      </div>
    `;
  }

  renderGlimpses() {
    const grid = document.getElementById('glimpses-grid');
    if (!grid || !this.data.glimpses) return;

    grid.innerHTML = this.data.glimpses.map(g => `
      <div class="glimpse-card">
        <div class="glimpse-video-wrapper">
          <video src="${g.video}" controls playsinline preload="metadata"></video>
        </div>
        <div class="glimpse-body">
          <h3>${g.title}</h3>
          <p>${g.description}</p>
        </div>
      </div>
    `).join('');
  }

  initPWAInstallPrompt() {
    this.btnInstallHeader = document.getElementById('btn-install-pwa');
    this.btnInstallDrawer = document.getElementById('btn-install-pwa-drawer');

    // If app is already running in standalone PWA window, keep buttons hidden
    const isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone;
    if (isStandalone) {
      if (this.btnInstallHeader) this.btnInstallHeader.classList.add('hidden');
      if (this.btnInstallDrawer) this.btnInstallDrawer.classList.add('hidden');
      return;
    }

    // Check if prompt was captured early
    if (window.deferredPWAInstallPrompt) {
      this.showPWAInstallButtons();
    }

    const handleInstallClick = async () => {
      if (window.deferredPWAInstallPrompt) {
        window.deferredPWAInstallPrompt.prompt();
        const choice = await window.deferredPWAInstallPrompt.userChoice;
        if (choice && choice.outcome === 'accepted') {
          if (this.btnInstallHeader) this.btnInstallHeader.classList.add('hidden');
          if (this.btnInstallDrawer) this.btnInstallDrawer.classList.add('hidden');
        }
        window.deferredPWAInstallPrompt = null;
      } else {
        // Fallback guidance for PC / Safari / Firefox
        if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone) {
          alert('Ashtavadhanam is already installed and running as a standalone app! / अष्टवधानम् पूर्वमेव संस्थापितम्।');
        } else {
          alert('To install Ashtavadhanam App:\n\n• On Chrome/Edge PC: Look for the Install icon (🖥️ ⬇ or ⊞+) in the right side of the address bar, or click browser menu (⋮ / …) → "Install Ashtavadhanam".\n• On Safari iPhone/iPad: Tap Share (⎋) → "Add to Home Screen".\n• On Android Chrome: Tap menu (⋮) → "Install app" or "Add to Home screen".');
        }
      }
    };

    if (this.btnInstallHeader) {
      this.btnInstallHeader.addEventListener('click', handleInstallClick);
    }
    if (this.btnInstallDrawer) {
      this.btnInstallDrawer.addEventListener('click', handleInstallClick);
    }

    window.addEventListener('appinstalled', () => {
      console.log('[PWA] App installed successfully');
      if (this.btnInstallHeader) this.btnInstallHeader.classList.add('hidden');
      if (this.btnInstallDrawer) this.btnInstallDrawer.classList.add('hidden');
      window.deferredPWAInstallPrompt = null;
    });
  }

  showPWAInstallButtons() {
    const isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone;
    if (isStandalone) return;
    if (this.btnInstallHeader) this.btnInstallHeader.classList.remove('hidden');
    if (this.btnInstallDrawer) this.btnInstallDrawer.classList.remove('hidden');
  }

  /* ================= SACRED TEMPLE BELL CHIME SYNTHESIZER ================= */
  initTempleChimes() {
    this.chimesEnabled = localStorage.getItem('ashtavadhanam_chimes_enabled') === 'true';

    const btnDrawerChimes = document.getElementById('btn-toggle-chimes');
    const btnPlayerChimes = document.getElementById('btn-player-chimes');

    const handleToggle = (e) => {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      this.toggleTempleChimes();
    };

    if (btnDrawerChimes) btnDrawerChimes.addEventListener('click', handleToggle);
    if (btnPlayerChimes) btnPlayerChimes.addEventListener('click', handleToggle);

    this.updateChimesUI();
  }

  playTempleChime(preview = false) {
    if (!this.chimesEnabled && !preview) return;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      if (!this.bellAudioCtx || this.bellAudioCtx.state === 'closed') {
        this.bellAudioCtx = new AudioCtx();
      }
      if (this.bellAudioCtx.state === 'suspended') {
        this.bellAudioCtx.resume().catch(() => {});
      }
      const ctx = this.bellAudioCtx;
      const now = ctx.currentTime;
      const masterGain = ctx.createGain();
      masterGain.gain.setValueAtTime(0.22, now);
      masterGain.connect(ctx.destination);

      // Authentic Temple Bell partials (fundamental 528Hz Vedic scale + golden overtone series)
      const partials = [
        { mult: 0.50, gain: 0.12, decay: 1.8 }, // warm resonant undertone
        { mult: 1.00, gain: 0.40, decay: 2.2 }, // striking fundamental
        { mult: 2.76, gain: 0.22, decay: 1.3 }, // resonant bronze overtone
        { mult: 5.40, gain: 0.10, decay: 0.7 }, // shimmering upper harmonic
        { mult: 8.93, gain: 0.05, decay: 0.3 }  // crystal bell strike ping
      ];

      partials.forEach(p => {
        const osc = ctx.createOscillator();
        const g = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(528 * p.mult, now);

        g.gain.setValueAtTime(p.gain, now);
        g.gain.exponentialRampToValueAtTime(0.0001, now + p.decay);

        osc.connect(g);
        g.connect(masterGain);

        osc.start(now);
        osc.stop(now + p.decay + 0.1);
      });
    } catch(err) {
      console.warn('Temple chime play error:', err);
    }
  }

  toggleTempleChimes() {
    this.chimesEnabled = !this.chimesEnabled;
    localStorage.setItem('ashtavadhanam_chimes_enabled', this.chimesEnabled ? 'true' : 'false');
    this.updateChimesUI();
    if (this.chimesEnabled) {
      this.playTempleChime(true);
    }
  }

  updateChimesUI() {
    const icon = document.getElementById('chimes-icon');
    const label = document.getElementById('chimes-primary-label');
    const playerBtn = document.getElementById('btn-player-chimes');

    if (icon) icon.textContent = this.chimesEnabled ? '🔔' : '🔕';
    if (label) label.textContent = this.chimesEnabled ? 'Temple Bell Chimes: ON' : 'Temple Bell Chimes: OFF';
    if (playerBtn) {
      playerBtn.textContent = this.chimesEnabled ? '🔔' : '🔕';
      playerBtn.title = this.chimesEnabled ? 'Temple Bell Chimes: ON (Click to Mute)' : 'Temple Bell Chimes: OFF (Click to Enable)';
    }
  }

  registerServiceWorker() {
    if ('serviceWorker' in navigator && window.location.protocol.startsWith('http')) {
      navigator.serviceWorker.register('sw.js').then((registration) => {
        // Proactively check for new sw.js updates on every load
        registration.update().catch(() => {});

        // Automatically reload client when new service worker takes over
        let refreshing = false;
        navigator.serviceWorker.addEventListener('controllerchange', () => {
          if (!refreshing) {
            refreshing = true;
            window.location.reload();
          }
        });
      }).catch(e => {
        console.log('SW registration error:', e);
      });
    }
  }
}

// Global listener to capture beforeinstallprompt even if fired before DOMContentLoaded
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  window.deferredPWAInstallPrompt = e;
  if (window.App && typeof window.App.showPWAInstallButtons === 'function') {
    window.App.showPWAInstallButtons();
  }
});

window.addEventListener('DOMContentLoaded', () => {
  window.App = new AshtavadhanamApp();
});
