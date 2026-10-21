# Acornoodle Books

[![CI](https://github.com/NelsonGrey/acornoodle-books/actions/workflows/ci.yml/badge.svg)](https://github.com/NelsonGrey/acornoodle-books/actions/workflows/ci.yml)
[![Deploy Website](https://github.com/NelsonGrey/acornoodle-books/actions/workflows/deploy-website.yml/badge.svg)](https://github.com/NelsonGrey/acornoodle-books/actions/workflows/deploy-website.yml)
![License: Proprietary](https://img.shields.io/badge/license-proprietary-lightgrey)

**Acornoodle Books** is the consumer-facing children's publishing imprint of **Nelson Grey LLC**. **Mark Nelson** is the author of the current books.

This repository holds everything for the imprint: the coloring-book production pipeline, the public website, the shared brand system, and the business documents.

| Environment | Branch | Firebase project | URL |
| --- | --- | --- | --- |
| Development | `develop` | `acornoodle-books-dev` | https://acornoodle-books-dev.web.app |
| Staging | `staging` | `acornoodle-books-staging` | https://acornoodle-books-staging.web.app |
| Production | `main` | `acornoodle-books-prod` | https://acornoodle-books-prod.web.app |

## Contents

- [Current series](#current-series)
- [Repository layout](#repository-layout)
- [Getting started](#getting-started)
- [Book production](#book-production)
- [Website](#website)
- [Deployment](#deployment)
- [Branching and releases](#branching-and-releases)
- [Brand](#brand)
- [Documentation](#documentation)
- [Quality and security](#quality-and-security)
- [Contributing, security, and support](#contributing-security-and-support)
- [License](#license)

## Current series

**Acornoodle Discovery Coloring Books** is an unordered series for children ages 5–9. Each title has 26 illustrated subjects with names and short facts, grouped into six themes with two titles each:

| Theme | Titles |
| --- | --- |
| Bugs | Crawling Bugs, Flying Bugs |
| Birds | Singing Birds, Soaring Birds |
| Fish | Schools of Fish, Curious Fish |
| Dinosaurs | Roaring Dinosaurs, Sleepy Dinosaurs |
| Farm animals | Busy Farm Animals, Cuddly Farm Animals |
| Vehicles | Working Vehicles, Racing Vehicles |

**Launch titles** (live on Amazon.com): Crawling Bugs, Roaring Dinosaurs, and Working Vehicles.

## Repository layout

```
acornoodle-books/
├── books/              Coloring-book initiative (KDP)
│   ├── scripts/            Build scripts
│   ├── prompts/            Art prompt manifests (CSV), local only, not in git
│   ├── art/                Source art            (local only, not in git)
│   ├── print-masters/      Working print masters (local only)
│   ├── builds/             Intermediate builds   (local only)
│   ├── kdp-packages/       Canonical upload ZIPs (local only)
│   └── archive/            Superseded work       (local only)
├── website/            Public website
│   └── dist/               Static site deployed to Firebase Hosting
├── brand/              Shared brand system
│   ├── acornoodle/         Logos, mascot, BRAND-GUIDE.md
│   └── proofs/             Review images
├── docs/               Business plan, brand/name screening, marketing, product development
├── scratch/            Throwaway review renders      (local only)
├── .github/            Workflows, issue/PR templates, CODEOWNERS, Dependabot
├── firebase.json       Default Firebase Hosting config (serves website/dist)
├── firebase.{dev,staging,prod}.json  Per-environment hosting configs
└── .firebaserc         Firebase project aliases
```

> **Local-only folders.** Source art, print masters, KDP packages, builds, archive, and scratch are several GB of PDFs and images. They are listed in [.gitignore](.gitignore) and are **not** in GitHub, which rejects files over 100 MB. Keep a backup of them outside this repository.

## Getting started

### Prerequisites

| Tool | Used for |
| --- | --- |
| Python 3.11+ | Book build scripts |
| Node.js + [Firebase CLI](https://firebase.google.com/docs/cli) (`npm i -g firebase-tools`) | Previewing and deploying the website |
| [GitHub CLI](https://cli.github.com/) (optional) | Repo administration |
| macOS | Scripts load Arial from `/System/Library/Fonts/Supplemental/`; on other systems, change the font paths |

### Setup

```bash
git clone https://github.com/NelsonGrey/acornoodle-books.git
cd acornoodle-books
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

The repository is private; you need access to the NelsonGrey organization.

## Book production

### Production standard

- Paperback, 8.5 x 11 inches
- 60-page black-and-white interior on white paper
- No-bleed interior
- Glossy full-color cover
- Large, age-appropriate illustrations with names and short facts
- Single-sided coloring artwork
- KDP Print Previewer **and** a physical proof are required for each title before publication

### Pipeline

1. **Prompts** — `books/prompts/manifest-v2.csv` (local only, gitignored) lists every page: book, subject, art prompt, fact, status, and asset path. Regenerate with `books/scripts/build_prompt_manifest_v2.py`.
2. **Art** — generate illustrations from the prompts into `books/art/interior-v2/<book-slug>/`; covers go in `books/art/cover-v3/`.
3. **Print masters** — assemble the interior and cover PDFs for a title.
4. **KDP package** — zip the print master with the upload data for KDP.

| Script | Purpose |
| --- | --- |
| `build_books_v2.py` | Assemble v2 interior/cover PDFs (output to `books/archive/`) |
| `build_covers_v3.py` | Build full-wrap v3 covers |
| `build_crawling_bugs_print_master.py` | Print master for Crawling Bugs |
| `build_additional_print_masters.py` | Print masters for the other launch titles |
| `facts_v2.py` | Fact text used on pages |

Run scripts from anywhere, for example `python books/scripts/build_covers_v3.py`. Paths resolve from the repository root.

### Canonical KDP packages

Only these ZIP files in `books/kdp-packages/` are current upload packages:

- `acornoodle-books-crawling-bugs-complete-print-master.zip`
- `acornoodle-books-roaring-dinosaurs-complete-print-master.zip`
- `acornoodle-books-working-vehicles-complete-print-master.zip`
- `acornoodle-books-launch-trio-kdp-packages.zip` — convenience bundle of the three above

Everything under `books/archive/` is development-stage or historical work and is not a KDP upload source unless rebuilt into a canonical Acornoodle package.

## Website

A plain static site (HTML, CSS, JavaScript; no build step) in [website/dist/](website/dist/): Home, Books, Inside the Books, Launch, About, Support, Privacy, Terms, and Cookies.

Layout follows the global 1280px rule: content and backgrounds in a centered column (`--site-content-width` in `website/dist/theme.css`), white outside, header and footer full width. The Support page lists support@acornoodlebooks.com.

Preview locally:

```bash
firebase emulators:start --only hosting     # serves website/dist
# or
python3 -m http.server 8000 --directory website/dist
```

## Deployment

The website deploys to Firebase Hosting. Aliases are defined in [.firebaserc](.firebaserc):

```bash
firebase deploy --only hosting --project development   # acornoodle-books-dev
firebase deploy --only hosting --project staging       # acornoodle-books-staging
firebase deploy --only hosting --project production    # acornoodle-books-prod
```

### Automatic deploys

[.github/workflows/deploy-website.yml](.github/workflows/deploy-website.yml) deploys on every push to `develop`, `staging`, or `main` that changes `website/dist/**`, `firebase*.json`, or `.firebaserc`. Each branch maps to its own GitHub Environment (`development`, `staging`, `production`).

Deploys are keyless. The workflow authenticates with [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation) because the organization policy `iam.disableServiceAccountKeyCreation` forbids service-account keys. Each Firebase project has a `github-deploy` service account (Firebase Hosting Admin only) and a GitHub OIDC provider that trusts only this repository and only that environment's branch (`develop`, `staging`, or `main`). Each GitHub Environment holds a `WIF_PROVIDER` variable with the provider's resource name. No credentials are stored in GitHub.

### Non-prod access gate

The dev and staging sites sit behind a Google sign-in wall (`website/dist/assets/auth-gate.js`), the same model as `EnvironmentGate` in vehicle-vitals. Production and `localhost` are never gated. It keeps the public out; it is not a hard auth boundary, because the allowlist ships in the page.

A visitor gets in if their email's **domain** is in `ALLOWED_EMAIL_DOMAINS`, or their exact address is in `ALLOWED_EMAILS`. An empty allowlist locks everyone out. Both are comma-separated secrets set per GitHub Environment (`development`, `staging`); the deploy workflow writes them into `assets/env-config.js` at deploy time and fails if both are empty. It also passes the public Firebase web config from the `FIREBASE_WEB_API_KEY` and `FIREBASE_WEB_APP_ID` secrets.

**Grant someone access:** add their address to `ALLOWED_EMAILS` (or their domain to `ALLOWED_EMAIL_DOMAINS`) under *Settings → Environments → development / staging → Environment secrets*, then re-run the deploy for that branch.

**One-time setup per Firebase project** (`acornoodle-books-dev`, `acornoodle-books-staging`): register a Web app, enable **Google** under Authentication → Sign-in method, and confirm `<project>.web.app` is under Authentication → Settings → Authorized domains.

Dev and staging also send `X-Robots-Tag: noindex, nofollow, noarchive` and a strict CSP (see `firebase.dev.json`, `firebase.staging.json`). Each environment has its own Firebase config; the workflow copies the right one to `firebase.json` before deploying.

### Production coming-soon switch

**The site went live on 2026-10-20** at https://acornoodlebooks.com. Production (`main`) can still serve a standalone coming-soon page from [website/coming-soon/](website/coming-soon/) instead of the full site in `website/dist/`; the deploy workflow swaps it in for `main` pushes when the switch below is not `false`. Dev and staging always deploy the full site.

The switch is the `SHOW_COMING_SOON` variable in the `production` GitHub Environment. It is `false` now (live). Anything other than the exact value `false` serves the coming-soon page (fails safe). **To roll back:** set `SHOW_COMING_SOON` to `true` under *Settings → Environments → production → Environment variables*, then re-run the Deploy Website workflow on `main`. The page collects no data and has no forms, because this is a children's imprint. Launch status and follow-ups: [docs/launch/LAUNCH-STATUS.md](docs/launch/LAUNCH-STATUS.md).

## Branching and releases

```
feature/*  →  develop  →  staging  →  main
               (dev)      (staging)   (production)
```

`develop` is the default branch. Do not commit directly to `staging` or `main`; promote with pull requests. Keep the repo setting "Automatically delete head branches" **off**: with it on, merging `staging` into `main` deletes `staging`. See [CONTRIBUTING.md](CONTRIBUTING.md) and [CHANGELOG.md](CHANGELOG.md).

## Brand

All earlier working names are retired. **Only "Acornoodle Books" may be used** in covers, interiors, metadata, marketing, or publishing accounts. In legal and publisher-facing contexts, identify Acornoodle Books as *an imprint of Nelson Grey LLC*.

Logos, mascot, palette, and usage rules are in [brand/acornoodle/BRAND-GUIDE.md](brand/acornoodle/BRAND-GUIDE.md).

## Documentation

| Document | Location |
| --- | --- |
| Name screening | [docs/brand/](docs/brand/) |
| Launch status and follow-ups | [docs/launch/LAUNCH-STATUS.md](docs/launch/LAUNCH-STATUS.md) |
| Social media strategy | [docs/marketing/SOCIAL-MEDIA-STRATEGY.md](docs/marketing/SOCIAL-MEDIA-STRATEGY.md) |

## Quality and security

| Check | Where | What it does |
| --- | --- | --- |
| Site and config checks | CI (`scripts/check-site.py`) | Every page has `lang`, title, viewport, and description; local links and assets resolve; Firebase JSON is valid |
| Book checks | CI (`scripts/check-books.py`) | Book scripts parse; the prompt manifest has its required columns, no blank titles, and no duplicate pages |
| Secret scan | CI (gitleaks, full history) | Fails on committed keys, tokens, or private keys |
| Promotion guard | CI, pull requests | Fails PRs that skip an environment (advisory; see below) |
| Pipeline Summary | CI | Single pass/fail roll-up of the checks above |
| Dependabot | GitHub | Alerts, security updates, weekly GitHub Actions and monthly Python updates |

The organization is on the GitHub Free plan, so this private repository cannot use branch protection, secret scanning, or code scanning. CI covers what it can; the promotion flow is enforced by convention. See [SECURITY.md](SECURITY.md).

## Contributing, security, and support

- [CONTRIBUTING.md](CONTRIBUTING.md) — workflow and standards
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — expected behavior
- [CLAUDE.md](CLAUDE.md) — guide for AI-assisted sessions
- [SECURITY.md](SECURITY.md) — reporting vulnerabilities
- [SUPPORT.md](SUPPORT.md) — where to get help

## License

Copyright © 2026 Nelson Grey LLC. All rights reserved. This is proprietary material; see [LICENSE](LICENSE).
