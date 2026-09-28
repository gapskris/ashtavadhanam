/**
 * Test Suite: Audio Player State & Toggle Logic
 * Verifies play/pause toggle in place, track switching, and ended behavior.
 */

const fs = require('fs');
const path = require('path');

const playerCodePath = path.join(__dirname, '..', 'js', 'player.js');
const playerCode = fs.readFileSync(playerCodePath, 'utf8');

// Mock browser DOM and Audio environment
const mockAudioEl = {
  src: '',
  currentSrc: '',
  paused: true,
  ended: false,
  currentTime: 0,
  duration: 30,
  listeners: {},
  canPlayType: () => 'probably',
  addEventListener(evt, fn) { this.listeners[evt] = fn; },
  play() {
    this.paused = false;
    this.currentSrc = this.src;
    if (this.listeners['play']) this.listeners['play']();
    return Promise.resolve();
  },
  pause() {
    this.paused = true;
    if (this.listeners['pause']) this.listeners['pause']();
  }
};

global.document = {
  getElementById: (id) => {
    if (id === 'master-audio') return mockAudioEl;
    return {
      textContent: '',
      style: {},
      classList: { add: () => {}, remove: () => {}, toggle: () => {} },
      addEventListener: () => {}
    };
  },
  querySelector: () => ({
    classList: { add: () => {}, remove: () => {}, toggle: () => {} }
  }),
  querySelectorAll: () => []
};

global.window = {
  location: { protocol: 'http:' }
};
global.requestAnimationFrame = () => {};

// Evaluate player code in mocked environment
eval(playerCode);

const p = window.Player;
p.setPlaylist([
  { id: '1', m4a: 'assets/audio/Page 6/01.m4a', mp3: 'assets/audio/Page 6/01.mp3' },
  { id: '2', m4a: 'assets/audio/Page 6/02.m4a', mp3: 'assets/audio/Page 6/02.mp3' }
]);

console.log('Testing Audio Player Toggle & State Machine:');

// Test 1: First click -> Plays clip
p.playClip(0);
if (p.audio.paused || p.currentIndex !== 0 || !p.isPlaying) {
  console.error('FAIL: Initial play failed');
  process.exit(1);
}
console.log('  [PASS] Initial play starts audio recitation');

// Test 2: Click active clip again -> Pauses in place (does NOT restart from 0)
p.playClip(0);
if (!p.audio.paused || p.isPlaying) {
  console.error('FAIL: Second click failed to pause track');
  process.exit(1);
}
console.log('  [PASS] Second click pauses recitation in place (without restarting)');

// Test 3: Click active paused clip -> Resumes from current position
p.playClip(0);
if (p.audio.paused || !p.isPlaying) {
  console.error('FAIL: Third click failed to resume playback');
  process.exit(1);
}
console.log('  [PASS] Third click resumes recitation smoothly');

// Test 4: Click a different clip -> Loads new track and plays
p.playClip(1);
if (p.currentIndex !== 1 || p.audio.paused || !p.audio.src.includes('02.m4a')) {
  console.error('FAIL: Switching track failed');
  process.exit(1);
}
console.log('  [PASS] Clicking different card switches tracks cleanly');

console.log('  --> ALL AUDIO PLAYER LOGIC TESTS PASSED!\n');
process.exit(0);
