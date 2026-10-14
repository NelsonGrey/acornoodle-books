# Contributing to Acornoodle Books

This is a private, proprietary repository owned by Nelson Grey LLC. Contributions are by invitation only, and all contributed work belongs to Nelson Grey LLC (see [LICENSE](LICENSE)).

## Branches and environments

| Branch | Purpose | Firebase project |
| --- | --- | --- |
| `develop` | Default branch; integration of all new work | `acornoodle-books-dev` |
| `staging` | Release candidate; final review | `acornoodle-books-staging` |
| `main` | Production | `acornoodle-books-prod` |

Work flows one way: `feature/*` → `develop` → `staging` → `main`. Do not commit directly to `staging` or `main`. Pushes to those branches deploy the website automatically (see [README](README.md#deployment)).

## Workflow

1. Branch from `develop`: `git switch -c feature/short-description develop` (use `fix/` for fixes, `docs/` for documentation, `book/<slug>/` for book work).
2. Make focused changes. Keep unrelated changes in separate pull requests.
3. Open a pull request into `develop` and complete the PR template.
4. After review and merge, promote with pull requests `develop` → `staging` → `main`.

Use clear, imperative commit messages ("Add Sleepy Dinosaurs back-cover copy"), with a short body when the reason is not obvious.

## What belongs in git

Source, scripts, prompts, brand assets, docs, and the deployable website (`website/dist/`) are tracked. Large generated assets (source art, print masters, KDP packages, archive, scratch) are **ignored** (see [.gitignore](.gitignore)) and live locally. Never force-add them. GitHub rejects files over 100 MB.

Never commit credentials, service-account keys, API tokens, or `.env` files.

## Books

- Follow the [production standard](README.md#production-standard): 8.5 x 11 in, 60-page black-and-white interior, no-bleed interior, glossy full-color cover.
- Use only the **Acornoodle Books** name. Earlier working names are retired and must not appear in covers, interiors, metadata, or marketing.
- Follow the [brand guide](brand/acornoodle/BRAND-GUIDE.md) for logo, palette, and mascot use.
- Check facts in books before they are added to the prompt manifest. The target reader is a child ages 5–9.
- Every title needs a KDP Print Previewer check and a physical proof before publication.

## Website

- Edit and test the site, then update `website/dist/`. It is plain static HTML, CSS, and JS with no build step.
- Check pages at mobile and desktop widths, keep contrast accessible, and keep the footer copyright: "Acornoodle Books, an imprint of Nelson Grey LLC."
- Test locally with `firebase emulators:start --only hosting` or any static server.

## Scripts

- Python 3.11+. Install dependencies with `pip install -r requirements.txt`.
- Scripts resolve paths from the repository root; keep it that way and avoid absolute paths.

## Questions

See [SUPPORT.md](SUPPORT.md).
