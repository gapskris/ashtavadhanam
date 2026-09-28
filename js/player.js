/**
 * Ashtavadhanam Modern — Audio & Video Player Engine
 * Driven by high-rate requestAnimationFrame timing loop
 */

class AshtavadhanamPlayer {
  constructor() {
    this.audio = document.getElementById('master-audio');
    this.modalVideo = document.getElementById('modal-video-player');
    
    // UI Elements
    this.btnPlayPause = document.getElementById('btn-play-pause');
    this.btnPrev = document.getElementById('btn-prev-clip');
    this.btnNext = document.getElementById('btn-next-clip');
    this.btnLoop = document.getElementById('btn-loop-mode');
    this.progressBar = document.getElementById('progress-bar-container');
    this.progressFill = document.getElementById('progress-fill');
    this.currentTimeEl = document.getElementById('current-time');
    this.totalTimeEl = document.getElementById('total-time');
    this.clipTitleEl = document.getElementById('player-clip-title');
    this.speakerEl = document.getElementById('player-speaker');
    this.badgeEl = document.getElementById('player-badge');
    this.codecEl = document.getElementById('codec-indicator');
    
    // Video Modal
    this.videoModal = document.getElementById('video-modal');
    this.videoModalTitle = document.getElementById('video-modal-title');
    this.btnVideoClose = document.getElementById('btn-modal-close-x');
    this.videoModalBackdrop = document.getElementById('video-modal-close');
    
    // State
    this.playlist = [];
    this.currentIndex = -1;
    this.autoAdvance = true;
    this.isPlaying = false;
    this.preferM4A = this.audio.canPlayType('audio/mp4; codecs="mp4a.40.2"') !== '';
    
    this.codecEl.textContent = this.preferM4A ? 'AAC 192k' : 'MP3 192k';
    
    this.initEvents();
    this.startClockLoop();
  }

  initEvents() {
    this.btnPlayPause.addEventListener('click', () => this.togglePlayPause());
    this.btnPrev.addEventListener('click', () => this.playPrevious());
    this.btnNext.addEventListener('click', () => this.playNext());
    
    this.btnLoop.addEventListener('click', () => {
      this.autoAdvance = !this.autoAdvance;
      this.btnLoop.classList.toggle('active', this.autoAdvance);
    });

    // Scrubber click
    this.progressBar.addEventListener('click', (e) => {
      if (!this.audio.duration) return;
      const rect = this.progressBar.getBoundingClientRect();
      const pos = (e.clientX - rect.left) / rect.width;
      this.audio.currentTime = pos * this.audio.duration;
    });

    // Audio status
    this.audio.addEventListener('play', () => {
      this.isPlaying = true;
      this.btnPlayPause.textContent = '⏸';
      this.updateActiveCard();
    });

    this.audio.addEventListener('pause', () => {
      this.isPlaying = false;
      this.btnPlayPause.textContent = '▶';
      this.updateActiveCard();
    });

    this.audio.addEventListener('ended', () => {
      if (this.autoAdvance) {
        this.playNext();
      } else {
        this.isPlaying = false;
        this.btnPlayPause.textContent = '▶';
        this.updateActiveCard();
      }
    });

    // Video modal close
    if (this.btnVideoClose) {
      this.btnVideoClose.addEventListener('click', () => this.closeVideoModal());
    }
    if (this.videoModalBackdrop) {
      this.videoModalBackdrop.addEventListener('click', () => this.closeVideoModal());
    }

    // Player Minimize & Restore
    this.playerBar = document.getElementById('player-bar');
    this.btnMinimize = document.getElementById('btn-minimize-player');
    this.btnRestore = document.getElementById('btn-restore-player');

    if (this.btnMinimize && this.playerBar) {
      this.btnMinimize.addEventListener('click', () => {
        this.playerBar.classList.remove('active-expanded');
        this.playerBar.classList.add('idle-collapsed');
        if (this.btnRestore) this.btnRestore.classList.remove('hidden');
        const appShell = typeof document.querySelector === 'function' ? document.querySelector('.app-shell') : null;
        if (appShell) appShell.classList.remove('has-active-player');
      });
    }

    if (this.btnRestore && this.playerBar) {
      this.btnRestore.addEventListener('click', () => {
        this.playerBar.classList.remove('idle-collapsed');
        this.playerBar.classList.add('active-expanded');
        this.btnRestore.classList.add('hidden');
        const appShell = typeof document.querySelector === 'function' ? document.querySelector('.app-shell') : null;
        if (appShell) appShell.classList.add('has-active-player');
      });
    }
  }

  /**
   * High-Rate Animation Clock & Timeline Synchronization
   * As specified in Master Plan Phase 5: Query media.currentTime inside requestAnimationFrame
   */
  startClockLoop() {
    const loop = () => {
      if (this.audio && !this.audio.paused && this.audio.duration) {
        const cur = this.audio.currentTime;
        const dur = this.audio.duration;
        const pct = (cur / dur) * 100;
        
        this.progressFill.style.width = `${pct}%`;
        this.currentTimeEl.textContent = this.formatTime(cur);
        this.totalTimeEl.textContent = this.formatTime(dur);
      }
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  formatTime(sec) {
    if (isNaN(sec)) return '0:00';
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  }

  setPlaylist(items, startIndex = 0) {
    this.playlist = items;
    this.currentIndex = startIndex;
  }

  playClip(index, forceRestart = false) {
    if (index < 0 || index >= this.playlist.length) return;
    const clip = this.playlist[index];
    if (!clip) return;

    // Choose M4A or MP3
    const targetSrc = (this.preferM4A && clip.m4a) ? clip.m4a : (clip.mp3 || clip.m4a);
    let curSrc = '';
    try {
      curSrc = decodeURIComponent(this.audio.currentSrc || this.audio.src || '');
    } catch (e) {
      curSrc = this.audio.currentSrc || this.audio.src || '';
    }

    // Check if player is currently loaded with THIS exact clip on this page
    const isSameTrack = curSrc && (curSrc.endsWith(targetSrc) || targetSrc.endsWith(curSrc)) && (index === this.currentIndex);

    if (isSameTrack && !forceRestart) {
      if (this.audio.ended) {
        this.audio.currentTime = 0;
        this.audio.play().catch(e => console.warn("Playback resume error:", e));
      } else if (!this.audio.paused) {
        this.audio.pause();
      } else {
        this.audio.play().catch(e => console.warn("Playback resume error:", e));
      }
      this.updateActiveCard();
      return;
    }

    this.currentIndex = index;
    this.audio.src = targetSrc;
    
    // Auto-expand player bar when track is played
    if (this.playerBar) {
      this.playerBar.classList.remove('idle-collapsed');
      this.playerBar.classList.add('active-expanded');
      if (this.btnRestore) this.btnRestore.classList.add('hidden');
      const appShell = typeof document.querySelector === 'function' ? document.querySelector('.app-shell') : null;
      if (appShell) appShell.classList.add('has-active-player');
    }
    
    // Update labels
    this.clipTitleEl.textContent = clip.title || clip.id || `Recitation ${index + 1}`;
    this.speakerEl.textContent = clip.speaker || 'Ashtavadhanam 1997';
    this.badgeEl.textContent = `Clip ${index + 1} of ${this.playlist.length}`;
    
    this.audio.play().catch(e => {
      console.warn("Autoplay blocked or user gesture required:", e);
    });

    this.updateActiveCard();
  }

  togglePlayPause() {
    if (this.audio.src) {
      if (this.audio.paused) {
        this.audio.play();
      } else {
        this.audio.pause();
      }
    } else if (this.playlist.length > 0) {
      this.playClip(0);
    }
  }

  playNext() {
    if (this.currentIndex + 1 < this.playlist.length) {
      this.playClip(this.currentIndex + 1);
    } else {
      // Completed all recitations in active round: sound temple chime
      if (window.App && typeof window.App.playTempleChime === 'function') {
        window.App.playTempleChime();
      }
      if (window.App && window.App.currentPageIndex + 1 < 25) {
        // Auto-advance to next page
        window.App.navigateToPage(window.App.currentPageIndex + 2, true);
      }
    }
  }

  playPrevious() {
    if (this.audio.currentTime > 3) {
      this.audio.currentTime = 0;
    } else if (this.currentIndex > 0) {
      this.playClip(this.currentIndex - 1);
    }
  }

  updateActiveCard() {
    document.querySelectorAll('.dialogue-card').forEach((card, idx) => {
      const isCur = (idx === this.currentIndex);
      card.classList.toggle('active', isCur);
      const btn = card.querySelector('.dialogue-audio-btn');
      if (btn) {
        const isThisPlaying = isCur && this.isPlaying;
        btn.classList.toggle('playing', isThisPlaying);
        btn.textContent = isThisPlaying ? '⏸' : '▶';
        btn.title = isThisPlaying ? 'Pause recitation' : (isCur ? 'Resume recitation' : 'Play recitation');
        btn.setAttribute('aria-label', isThisPlaying ? 'Pause recitation' : (isCur ? 'Resume recitation' : 'Play recitation'));
      }
    });
  }

  openVideoModal(videoSrc, title) {
    this.audio.pause();
    this.videoModalTitle.textContent = title || "Performance Video Demonstration";
    this.modalVideo.src = videoSrc;
    this.videoModal.classList.remove('hidden');
    this.modalVideo.play().catch(e => console.log(e));
  }

  pause() {
    if (this.audio && !this.audio.paused) {
      this.audio.pause();
    }
    this.isPlaying = false;
    if (this.btnPlayPause) this.btnPlayPause.textContent = '▶';
    this.updateActiveCard();
  }

  closeVideoModal() {
    this.modalVideo.pause();
    this.modalVideo.src = "";
    this.videoModal.classList.add('hidden');
  }
}

window.Player = new AshtavadhanamPlayer();
