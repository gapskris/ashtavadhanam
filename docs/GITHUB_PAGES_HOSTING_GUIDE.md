# How to Host Ashtavadhanam Modern on GitHub Pages (Step-by-Step Guide)

**Project:** Ashtavadhanam — The Wonder that is Sanskrit (1997–2026)  
**Target Platform:** GitHub Pages (Free, Fast Global CDN, Automatic HTTPS/SSL)  
**Location:** `C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern`

---

## 1. Why GitHub Pages is a Perfect Fit

The modernized application is built entirely on modern open web standards (**pure static HTML5, CSS3, Vanilla ES6 JavaScript, Web Audio API, H.264 MP4, and AAC/MP3 audio**). It requires **zero server-side code, zero Node.js runtime, and zero database setup**.

### Technical Compatibility & Size Audit

| Metric | GitHub Pages Limit | Ashtavadhanam Modern Status | Verdict |
| :--- | :---: | :---: | :---: |
| **Total Repository Size** | 1,000 MB (1 GB recommended) | **219.67 MB** | ✅ **Passed** (well within limit) |
| **Largest Single File** | 100 MB hard limit (50 MB warning) | **19.48 MB** (`GLIMPSE2.mp4`) | ✅ **Passed** (No Git LFS needed) |
| **Monthly Bandwidth** | 100 GB / month free | Fast GitHub CDN caching | ✅ **Passed** |
| **Asset Paths** | Relative paths required | 100% relative (`assets/...`, `css/...`) | ✅ **Passed** (Works under subpaths) |
| **Service Worker Scope** | Directory-relative | Auto-registers within directory | ✅ **Passed** |

---

## 2. Step-by-Step Deployment Instructions

### Step 1: Create a New GitHub Repository

1. Log into your account on [GitHub.com](https://github.com).
2. Click the **`+`** icon at the top right and select **New repository**.
3. Configure the repository:
   - **Repository name**: `ashtavadhanam` (or `ashtavadhanam-modern`)
   - **Description**: *Historic 1997 Sanskrit Ashtavadhanam Performance — Sri Aurobindo Society & Pondicherry University*
   - **Visibility**: Select **Public** (required for free GitHub Pages hosting)
   - **Initialize repository**: **Do NOT check** "Add a README", ".gitignore", or "Choose a license" (these are already configured locally)
4. Click **Create repository**.

---

### Step 2: Initialize Git and Push from Your PC

Open **PowerShell** or Command Prompt and execute the following commands in order:

```powershell
# 1. Change directory to the modernized project folder
cd "C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern"

# 2. Initialize a local Git repository on the 'main' branch
git init -b main

# 3. Stage all files (HTML, CSS, JS, 173 audio tracks, 15 videos, canvases, data)
git add .

# 4. Commit all files
git commit -m "Initial commit: Complete Ashtavadhanam PWA (25 rounds, 173 audios, 15 videos, 3-way Sanskrit display)"

# 5. Link your local repo to your GitHub repository
# (Replace <YOUR-USERNAME> and <REPO-NAME> with your actual GitHub details)
git remote add origin https://github.com/<YOUR-USERNAME>/<REPO-NAME>.git

# 6. Push all files to GitHub
git push -u origin main
```

*(Note: Uploading the ~219 MB repository will take roughly 1 to 3 minutes depending on your internet upload speed).*

---

### Step 3: Enable GitHub Pages in Repository Settings

Once your files are pushed to GitHub:

1. Open your repository on GitHub in your web browser.
2. Click the **Settings** tab (the gear icon at the top right of the repo).
3. In the left-hand sidebar, click **Pages** (under the *Code and automation* section).
4. Under **Build and deployment**:
   - **Source**: Select **`Deploy from a branch`**
   - **Branch**: Select **`main`**
   - **Folder**: Leave as **`/ (root)`**
5. Click **Save**.

```
Settings ──► Pages ──► Source: [Deploy from a branch] ──► Branch: [main] [/ (root)] ──► [Save]
```

---

### Step 4: Access Your Live Application

GitHub Actions will automatically build and publish the site within 1 to 2 minutes.

Your application will be live at:
```
https://<YOUR-USERNAME>.github.io/<REPO-NAME>/
```

---

## 3. Post-Deployment Features & Advantages

1. **Free Global CDN & Automatic SSL**:  
   GitHub provides enterprise-grade Content Delivery Network (Fastly CDN) caching and automatic HTTPS encryption free of charge.
2. **Instant Mobile PWA Installation**:  
   When visitors open the link on Android (Chrome) or iPhone/iPad (Safari), they can tap **"Add to Home Screen"** or **"Install App"** to use it as a standalone full-screen app.
3. **Smart TV Viewing**:  
   Open the TV browser on any Samsung Tizen, LG webOS, Sony Google TV, Fire TV, or Apple TV browser and navigate to the URL. The built-in spatial D-pad controller will activate automatically.
4. **Optional Custom Domain**:  
   To point an institutional or custom domain (e.g. `ashtavadhanam.aurobindosociety.org` or `ashtavadhanam.org`):
   - Go to **Settings → Pages → Custom domain**.
   - Enter your domain name and check **Enforce HTTPS**.
   - Add a CNAME DNS record pointing to `<YOUR-USERNAME>.github.io`.

---

## 4. How to Update the Site in the Future

Whenever you make future edits to the text, CSS, or scripts, simply push your updates with three quick commands:

```powershell
cd "C:\DataScience\Vijay Ji's Music Conversion\Ashtavadhanam_modern"
git add .
git commit -m "Update: description of changes"
git push
```
GitHub Pages will automatically rebuild and update the live website within 60 seconds.
