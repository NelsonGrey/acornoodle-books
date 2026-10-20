# Acornoodle Books: guide for Claude sessions

Children's coloring-book imprint of Nelson Grey LLC (ages 5–9), pre-launch. This repo holds the book production pipeline, the shared brand system, business docs, and the static website. Read `README.md` first; brand rules are in `brand/acornoodle/BRAND-GUIDE.md`.

## Commands
- `pip install -r requirements.txt`: book script dependencies (Python 3.11+, macOS fonts).
- `python3 scripts/check-site.py`: validates every HTML page (lang, title, viewport, description, local links) and the Firebase JSON config.
- `python3 scripts/check-books.py`: syntax-checks `books/scripts/*.py` and sanity-checks `books/prompts/manifest-v2.csv`. CI runs both.
- `firebase emulators:start --only hosting`: preview `website/dist/` locally (localhost is never gated).
- `gitleaks detect --source . --config .gitleaks.toml --redact`: secret scan.

## Layout
- `books/`: `scripts/` and `prompts/` are tracked. `art/`, `print-masters/`, `builds/`, `kdp-packages/`, `archive/` are **local only** (several GB, in `.gitignore`); never force-add them.
- `website/dist/`: the deployed static site (plain HTML, CSS, vanilla JS; no build step). `website/coming-soon/`: standalone production placeholder.
- `firebase.{dev,staging,prod}.json`: per-environment hosting config; the deploy workflow copies the right one to `firebase.json`. Dev and staging send noindex and a strict CSP (Google Fonts and inline styles are allowed because the pages use them).
- `brand/`, `docs/`: logos and mascot, business plan, name screening, marketing, product development.

## Rules that must keep holding
- Flow is `feature/*` → `develop` → `staging` → `main`. Never push or open a PR to `main`, and never deploy to prod, unless the user explicitly says to. Prod is **not live**: `main` deploys the coming-soon page unless the `SHOW_COMING_SOON` variable in the `production` GitHub Environment is exactly `false`.
- Use only the name **Acornoodle Books**; earlier working names are retired. Legal and publisher-facing copy says "an imprint of Nelson Grey LLC".
- This is a children's publisher: no data collection, forms, or accounts on the website, and no personal information about children anywhere. Check facts in books before they enter the prompt manifest.
- Layout (global rule, also in `~/.claude/CLAUDE.md`): all content and its backgrounds sit in a centered 1280px column (`--site-content-width` in `website/dist/theme.css`); outside it the page is white; only the header and footer span the full width.
- Book standard: 8.5 x 11 in paperback, 60-page black-and-white no-bleed interior, glossy full-color cover; KDP Print Previewer and a physical proof before each title publishes.
- Dev and staging sit behind a Google sign-in gate (`website/dist/assets/auth-gate.js`). The allowlist comes from the `ALLOWED_EMAIL_DOMAINS` and `ALLOWED_EMAILS` secrets in each GitHub Environment and is written to `assets/env-config.js` at deploy time. An empty allowlist locks everyone out. Never commit real addresses or API keys.
- Deploys are keyless (Workload Identity Federation) because org policy forbids service-account keys. Never create or commit a service-account key.
- The org is on the GitHub Free plan: private repos have no branch protection, secret scanning, or code scanning. CI's "Promotion guard" is advisory only.

## Working style with this user (Mark Nelson)
- Give a recommendation and continue; outward-facing or costly actions (publishing, pushing to `main`, deploying to prod, creating cloud resources, spending money) need their explicit say-so.
- Commit in small commits ending with the co-author line from the session, and open PRs against `develop`.
- Be explicit about what is verified versus not (for example, real Google sign-in has only been tested up to the popup).
