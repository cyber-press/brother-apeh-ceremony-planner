# Brother Apeh Ceremony Planner — v3.4.2 UI Repair

This build repairs malformed section-title markup that caused sections to nest inside one another, producing narrow tables, missing headings, excessive whitespace, and command-center overflow.

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

## Shared backend option (FastAPI + SQLite)

This project can also run behind a small Python API so the same planner data is shared across devices instead of remaining browser-local only.

### Run locally

```bash
python -m pip install -r requirements.txt
python app.py
```

The app serves the planner on `http://localhost:8000` and keeps a shared SQLite file at `planner.db`.

### API contract

- `GET /api/planner/default` returns the latest saved planner payload
- `POST /api/planner/default` stores the current planner state as JSON

This keeps the static planner UI while allowing a shared backend for family or team access.

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


## Mobile-first iPhone experience

Version 3.3 adds safe-area support, 44–48 px touch targets, 16 px form controls to prevent Safari zoom, a five-action bottom navigation bar, compact dashboard cards, swipeable utility controls, and improved table scrolling.


## Version 3.4 — Professional Print & PDF Suite

- Cover prints as a dedicated first page.
- Executive dashboard and charts print as a structured summary page.
- Dove artwork is resized and kept clear of the confidentiality footer.
- Ceremony and burial dates use consistent full-date formatting.
- Print controls support Full Planner, Executive Summary, Ceremony-Day Brief, and Finance reports.
- Tables repeat headings and avoid splitting individual rows where supported.
- Mobile, PWA, navigation, and interactive controls are hidden in PDF output.

For clean PDF output in Chrome or Edge, open **More settings**, turn off **Headers and footers**, and turn on **Background graphics**.
