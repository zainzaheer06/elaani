# Pure Signage — Claude Code Memory

Bilingual (Arabic/English) digital signage marketplace. Connects screen owners (vendors), advertisers, and end customers. Inventory is Egyptian (Cairo / Alexandria / Obour) digital billboards, priced in EGP. This file is auto-loaded into Claude Code's context — keep it concise.

## Tech stack

- **Backend:** Flask 2.3.3, Flask-Babel 3.1.0 (i18n), Jinja2 templates
- **Frontend:** Server-rendered Jinja + TailwindCSS (CDN, `cdn.tailwindcss.com`), Font Awesome 6
- **Maps:** Leaflet 1.9.4 + OpenStreetMap tiles (no API key needed)
- **i18n:** gettext .po/.mo files in `translations/ar/LC_MESSAGES/` and `translations/en/LC_MESSAGES/`. Default locale is **Arabic** (`ar`); RTL layout is the default.
- **Realtime / video:** LiveKit (self-hosted at `app.saadzaheer.com`) — utility scripts only, not wired into Flask routes.
- **Persistence:** None. All data is hardcoded Python lists inside `app.py`. There is no database, no ORM, no migrations.

## Repo layout

Single Flask app, port 5900. (A second app `Pure Signage-New/` was deleted on 2026-04-27 — only this app remains.)

```
C:\Users\DELL\Pure Signage\           (outer workspace folder)
└── Pure Signage\                     (project root — Flask app lives here)
    ├── app.py                   Main Flask app — port 5900, vendor + customer flows
    ├── templates/
    │   ├── base.html            Vendor sidebar layout
    │   ├── base_customer.html   Customer-facing layout
    │   ├── base_public.html     Marketing/public layout
    │   ├── customer/            Customer dashboard pages
    │   ├── screen_detail.html   Per-screen detail view (vendor/customer share)
    │   └── components/language_switcher.html
    ├── static/
    │   ├── css/{ltr,rtl}.css    Direction-specific overrides
    │   ├── images/              Per-billboard photos (named by address+district)
    │   └── Pure Signage-logo*.png
    ├── translations/{ar,en}/LC_MESSAGES/messages.{po,mo}
    ├── generate_token.py        LiveKit JWT minter (PyJWT)
    ├── livekit-code.py          LiveKit REST API smoke test
    ├── sip_call.py              SIP outbound call helper
    ├── quick-checlk.py          (typo in filename — a quick check script)
    ├── t.py / test-livekit.py   Ad-hoc test scripts
    ├── babel.cfg                pybabel extraction config
    ├── requirements.txt
    ├── rename_script.py         (dormant — original Elaani→Pure Signage rename utility)
    ├── rename_to_Pure Signage.py (dormant — one-shot Elaani/Elanni→Pure Signage rename)
    └── RENAME_INSTRUCTIONS.md   (obsolete — rename is done; safe to delete)
```

## How to run

```bash
cd Pure Signage
python app.py            # http://127.0.0.1:5900

# Compile translations after editing .po files
pybabel compile -d translations
```

## Conventions

- **Currency:** Egyptian Pound (EGP). The custom Jinja filter `format_egp` appends `EGP`. Prices are monthly rentals; VAT is 14%.
- **Locales:** `ar` (default, RTL) and `en` (LTR). Templates check `session.get('lang', 'ar')` to pick `rtl.css` vs `ltr.css`. Always wrap user-facing strings in `{{ _('...') }}` or `gettext('...')` in Python — never hardcode Arabic/English copy.
- **Tailwind tokens:** Use the brand color classes `Pure Signage-primary` (#005430 dark green), `Pure Signage-secondary` (#057f48), `Pure Signage-light` (#e8f5e8). Defined inline in each `base*.html`'s `tailwind.config`.
- **Mock data lives in `app.py`** as module-level lists (`screens_data`, `bookings_data`, `clients_data`). The screen list is sourced from the Yafta Map quotation PDF dated 2026-01-13; ~75 entries, each tied to an image in `static/images/` named after its address. Mutating them in routes is fine for the demo but resets on server restart.
- **No build step.** Tailwind is via CDN. Don't introduce a bundler unless the user asks.
- **Template inheritance:** every page extends one of `base.html`, `base_customer.html`, or `base_public.html`. Don't create a new base layout — reuse one.

## Screen detail page

`/vendor/screen/<id>` and `/dashboard/customer/screen/<id>` both render `screen_detail.html`, which mirrors the Yafta Map quotation layout: large photo + Leaflet mini-map on the left; Location/GPS, Media Type, Rate Card vs Promotion Rate, and Screen Specification panel on the right. Many fields (GPS, traffic estimates, content pixel, screening hours, etc.) are deliberately blank in the data — the user fills these in per-screen.

## Known issues / debt

- **Hardcoded secrets in source.** `generate_token.py` and `livekit-code.py` contain plaintext LiveKit `API_KEY` and `API_SECRET`. `app.py` has a hardcoded `app.secret_key`. These should move to environment variables before any public deploy. Flag this if the user asks about deployment, sharing, or committing to a public repo.
- **Test routes still in production code.** `/test-i18n`, `/test-ar`, `/test-en` are live in `app.py`. Remove before deploy.
- **No auth middleware.** The "customer" routes assume a hardcoded `current_user_data` from `inject_current_user()`. There is no real session/login enforcement.
- **`quick-checlk.py`** has a typo in the filename (should be `quick-check.py`) — leave it unless the user asks, to avoid breaking external references.

## Brand rename history

The project was renamed from **Elaani / Elanni** → **Pure Signage** in April 2026 and the on-disk folder rename was finished on 2026-04-27. As of the latest sweep, the only remaining mentions of the old names live in `RENAME_INSTRUCTIONS.md`, `rename_script.py`, and `rename_to_Pure Signage.py` — all dormant historical files. Active code, templates, translations, and assets are clean.

## Out of scope (don't volunteer)

- Don't add a real database, ORM, or migrations unless asked.
- Don't extract templates into a frontend SPA (React/Vue) unless asked.
- Don't introduce a Tailwind build pipeline; the CDN is intentional for now.
