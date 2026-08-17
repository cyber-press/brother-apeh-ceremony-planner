# Brother Apeh Planner v3.4.4.9 — Data Integrity Pass

Verified provisional budget arithmetic and all summary calculations; removed unsupported sample numbers and auto-filled dates; neutralized unconfirmed status defaults; made the draft-total badge dynamic; fixed Received-state CSV export; locked the working draft to Nigerian Naira to prevent symbol-only currency relabeling.

# Brother Apeh Planner v3.4.4.3

Draft Funding Status release: planned contributions are separate from officially received funds. Only rows marked Received count toward Amount Received in dashboard, charts, print summary, backups, and CSV.

# Brother Apeh Planner v3.4.4.2 — Budget & Vendor Import

Imports the 12-line provisional burial budget draft (₦2,135,100) and adds business/vendor, phone, and optional portfolio/reference tracking to every budget row.

# Brother Apeh Ceremony Planner — v3.4.4.1 Layout Stabilization

This release repairs all 18 section heading elements, prevents nested/contracted sections, contains wide finance tables inside their section cards, preserves horizontal table scrolling, and keeps the v3.4.4 dark-mode contrast improvements.

# Brother Apeh Ceremony Planner — v3.4.4 Deployment Repair

This release restores the canonical `assets/icons/` PWA structure, installs the static GitHub Pages workflow at `.github/workflows/pages.yml`, and deploys the v3.4.4 Dark Mode Polish build.

# Brother Apeh Ceremony Planner

A hardened, standalone burial ceremony planning dashboard prepared for the Brother Apeh family.

## Included files

```text
brother-apeh-planner/
├── index.html
├── .nojekyll
├── 404.html
├── README.md
├── manifest.webmanifest
├── service-worker.js
├── offline.html
├── assets/
│   └── icons/
│       ├── icon-32.png
│       ├── icon-192.png
│       ├── icon-512.png
│       ├── icon-maskable-192.png
│       └── icon-maskable-512.png
└── .github/
    └── workflows/
        └── pages.yml
```


## Progressive Web App

This build can be installed as an application on supported phones, tablets, and computers. After the first successful online visit, the service worker caches the planner shell so it can reopen during an internet interruption.

### Install

- **Chrome / Edge on desktop or Android:** select **Install app** when the planner offers it, or use the browser installation icon.
- **iPhone / iPad:** open the Share menu and select **Add to Home Screen**.
- **Offline test:** load the site once, close it, disable the network, and reopen it from the installed icon.

### PWA files

- `manifest.webmanifest` defines the installed application name, colors, icons, scope, and display mode.
- `service-worker.js` caches the application shell and approved CDN assets.
- `offline.html` provides a controlled fallback when a requested page is not yet cached.
- `assets/icons/` contains standard and maskable installation icons.

When updating cached application files, increment the `VERSION` constant in `service-worker.js` so prior caches are removed cleanly.

## Privacy model

This version has no server-side backend or shared database. Planner information is stored in the browser on the device where it is entered.

- Do not commit completed backup files, family contact details, contribution records, passwords, tokens, or API keys.
- Do not use a public or shared computer for private ceremony records.
- Download JSON backups regularly and store them in a protected location.
- Data entered on one device will not automatically appear on another device.
- Clearing browser storage may remove locally saved planner data.

## Deploy with GitHub Pages

1. Create a GitHub repository named `brother-apeh-planner`.
2. Upload this complete folder structure to the repository root.
3. Commit the files to the `main` branch.
4. Open **Settings → Pages**.
5. Under **Build and deployment**, set **Source** to **GitHub Actions**.
6. Open the **Actions** tab and confirm that the deployment workflow completes successfully.
7. Return to **Settings → Pages** and enable **Enforce HTTPS** when available.

The workflow also supports manual deployment from **Actions → Deploy Brother Apeh Planner to GitHub Pages → Run workflow**.

## Local testing

You may open `index.html` directly. For behavior closest to GitHub Pages, run a local static server:

```bash
python -m http.server 8080
```

Then visit `http://localhost:8080`.

## Updating the planner

Replace `index.html` with the newer approved build, commit the change, and push it to `main`. GitHub Actions will publish the update automatically.

## Current limitations

- No accounts or user roles
- No shared real-time editing
- No cloud synchronization
- No server audit trail
- Browser storage is not encrypted

A private authenticated backend should be introduced before adding multi-user collaboration, online contribution processing, or centralized family records.


## v3.4.4.9 Live Financial Dashboard
Dashboard metrics recalculate from live budget estimates, actual costs, contribution entries, received toggles, and payouts.


## v3.4.4.9 Identity details
- Religious affiliation: Pentecostal
- Requested title: Mr.


## v3.4.4.9 Editable Profile + Auto-save
Section 1 remains fully editable. Changes are saved in browser localStorage after input and are flushed immediately on completed changes, page hide, refresh, or close. The supplied Brother Apeh values are starting defaults, not locked fields.


## v3.4.4.10 — Family / Next of Kin
- Section 2 populated with verified family/contact information.
- All Section 2 fields remain editable and auto-save locally.
- One-time browser migration replaces legacy/sample family values with the verified starting data without repeatedly overriding later edits.


## v3.5.0 — Multi-User Shared Master Sync

This build adds a FastAPI + SQLite synchronization layer while keeping the existing browser autosave as an offline fallback.

### Architecture

- Frontend: static planner (`index.html`) — suitable for GitHub Pages.
- Backend: FastAPI REST API.
- Database: SQLite in WAL mode on a persistent disk/volume.
- Shared planner ID: `brother-apeh-master`.
- Protection: server-side `PLANNER_ACCESS_KEY`, entered by each authorized family member and stored only in that browser's localStorage.
- Concurrency: optimistic version numbers. A stale browser receives HTTP 409 instead of silently overwriting a newer family edit.
- Offline behavior: localStorage continues to save changes immediately. When the API is reachable, the browser pushes the latest state after a debounce.

### Local test

1. Backend:
   ```bash
   cd backend
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   set PLANNER_ACCESS_KEY=your-test-key
   # macOS/Linux: export PLANNER_ACCESS_KEY=your-test-key
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

2. Frontend (do not open with `file://` for API testing):
   ```bash
   cd ..
   python -m http.server 5500
   ```
   Open `http://127.0.0.1:5500`.

3. Click **Shared sync**, enter the same access key, optionally enter your name, and approve creation of the first shared master.

### GitHub Pages + hosted API

1. Deploy `/backend` to one persistent FastAPI host.
2. Configure a persistent disk/volume for SQLite.
3. Set:
   - `PLANNER_ACCESS_KEY`
   - `PLANNER_DB_PATH` (for example `/data/planner.db`)
   - `PLANNER_ALLOWED_ORIGINS=https://cyber-press.github.io`
4. Edit `sync-config.js`:
   ```js
   window.PLANNER_SYNC_CONFIG = Object.freeze({
     enabled: true,
     apiBaseUrl: "https://YOUR-API-HOST.example.com",
     plannerId: "brother-apeh-master"
   });
   ```
5. Deploy the static files to GitHub Pages.

### Important security boundary

The shared access key is a family-wide gate, not per-user authentication. It is intentionally a lightweight next step. For individual accounts, roles, audit history, password recovery, or multiple planner workspaces, migrate the backend to Postgres/Supabase or add a full authentication layer.

### SQLite deployment rule

Run **one FastAPI application instance** against the SQLite file. Do not horizontally scale multiple containers against separate ephemeral SQLite files. If multi-instance scaling is required, move the store to Postgres.
