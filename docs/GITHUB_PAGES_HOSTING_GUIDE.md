# How to Host Ashtavadhanam Modern on GitHub Pages (Step-by-Step Guide)

**Project:** Ashtavadhanam — The Wonder that is Sanskrit (1997–2026)  
**Target Platform:** GitHub Pages (Free, Fast Global CDN, Automatic HTTPS/SSL)  
**Production Remote:** `https://github.com/gapskris/ashtavadhanam`  
**Live Production URL:** `https://gapskris.github.io/ashtavadhanam/`

---

## 1. Why GitHub Pages is a Perfect Fit

The modernized application is built entirely on modern open web standards (**pure static HTML5, CSS3, Vanilla ES6 JavaScript, Web Audio API, H.264 MP4, and AAC/MP3 audio**). It requires **zero server-side code, zero Node.js runtime, and zero database setup**.

### Technical Compatibility & Size Audit

| Metric | GitHub Pages Limit | Ashtavadhanam Modern Status | Verdict |
| :--- | :---: | :---: | :---: |
| **Total Repository Size** | 1,000 MB (1 GB recommended) | **~245 MB** | ✅ **Passed** (well within limit) |
| **Largest Single File** | 100 MB hard limit (50 MB warning) | **19.48 MB** (`GLIMPSE2.mp4`) | ✅ **Passed** (No Git LFS needed) |
| **Monthly Bandwidth** | 100 GB / month free | Fast GitHub CDN caching | ✅ **Passed** |
| **Asset Paths** | Relative paths required | 100% relative (`assets/...`, `css/...`) | ✅ **Passed** (Works under subpaths) |
| **Service Worker Scope** | Directory-relative | Auto-registers within `/ashtavadhanam/` | ✅ **Passed** |
| **Media Streaming (HTTP 206)**| Native Fastly CDN Range Support | Full RFC 7233 Byte-Range streaming | ✅ **Passed** |

---

## 2. GitHub Pages Configuration & Deployment

### Step 1: Remote Repository
The project is connected to the official repository:
```text
https://github.com/gapskris/ashtavadhanam.git
```

### Step 2: Enable GitHub Pages in Repository Settings
1. Open `https://github.com/gapskris/ashtavadhanam/settings/pages`.
2. Under **Build and deployment**:
   - **Source**: Select **`Deploy from a branch`**
   - **Branch**: Select **`main`**
   - **Folder**: Leave as **`/ (root)`**
3. Click **Save**.

```
Settings ──► Pages ──► Source: [Deploy from a branch] ──► Branch: [main] [/ (root)] ──► [Save]
```

### Step 3: Jekyll Bypass (`.nojekyll`)
A `.nojekyll` file is present in the repository root. This prevents GitHub Pages' default Jekyll engine from ignoring files or directories starting with underscores or containing specialized assets.

### Step 4: Service Worker & Caching Strategy
* **Subpath Awareness**: The service worker (`sw.js`) registers relative to the repository path (`/ashtavadhanam/`).
* **Cache Versioning**: Cache-busting parameters (`?v=1.2.2`) ensure clients instantly receive new JavaScript and CSS updates upon deployment.
* **Network-First Strategy**: Assets are fetched from the network first, cleanly falling back to cache when offline.
* **Range-Request Bypass**: Media streams (`.mp4`, `.m4a`) pass through directly to GitHub's Fastly CDN, which natively supports HTTP 206 Partial Content byte-range seeking.

---

## 3. Post-Deployment Features & Advantages

1. **Free Global CDN & Automatic SSL**:  
   GitHub provides enterprise-grade Content Delivery Network (Fastly CDN) caching and automatic HTTPS encryption free of charge.
2. **Instant Mobile PWA Installation**:  
   When visitors open the link on Android (Chrome) or iPhone/iPad (Safari), they can tap **"Install Web App"** directly in the app header to use it as a standalone full-screen app with the official circular gold emblem.
3. **Smart TV Viewing**:  
   Open the TV browser on any Samsung Tizen, LG webOS, Sony Google TV, Fire TV, or Apple TV browser and navigate to the URL. The built-in spatial D-pad controller will activate automatically.
4. **Optional Custom Domain**:  
   To point an institutional or custom domain (e.g. `ashtavadhanam.aurobindosociety.org` or `ashtavadhanam.org`):
   - Go to **Settings → Pages → Custom domain**.
   - Enter your domain name and check **Enforce HTTPS**.
   - Add a CNAME DNS record pointing to `gapskris.github.io`.

---

## 4. How to Push Updates

Whenever you make future edits to the text, CSS, or scripts, simply push your updates:

```powershell
cd "C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern"
git add .
git commit -m "feat/fix: description of changes"
git push origin main
```
GitHub Pages will automatically rebuild and update the live website within 60 seconds.
