# Brother Apeh Ceremony Planner

A hardened, standalone burial ceremony planning dashboard prepared for the Brother Apeh family.

## Included files

```text
brother-apeh-planner/
├── index.html
├── .nojekyll
├── 404.html
├── README.md
└── .github/
    └── workflows/
        └── pages.yml
```

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
