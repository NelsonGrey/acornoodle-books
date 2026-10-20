# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.2.0] - 2026-10-20 (public launch)

### Launch
- Production now serves the full site at https://acornoodlebooks.com (`SHOW_COMING_SOON=false`). Crawling Bugs, Roaring Dinosaurs, and Working Vehicles are live on Amazon.com and linked from the Books and Launch pages.
- Support email (support@acornoodlebooks.com) published; stale private-preview wording removed from the Support and Privacy pages.
- Pinterest, Instagram, and Facebook linked in the footer; Pinterest domain verification added.
- `robots.txt`, `sitemap.xml`, 404 page, canonical, Open Graph, and Twitter card tags.
- Layout: content and backgrounds confined to a centered 1280px column (global rule); all 12 site covers re-rendered from the current cover script.

### Changed
- **Lonely Fish renamed Curious Fish** (display title; slug unchanged).
- Repo setting "Automatically delete head branches" turned off after it deleted `staging` on a promotion merge.

### Added
- Repository standards: CI (site checks, book script and manifest checks, gitleaks secret scan, advisory promotion guard, Pipeline Summary), CLAUDE.md, expanded SECURITY policy, `.gitattributes`, `.gitleaks.toml`, grouped Dependabot, and a filled-in GitHub About section.
- Coming-soon page for production, controlled by the `SHOW_COMING_SOON` environment variable.
- Google sign-in access gate on dev and staging with domain and exact-email allowlists (same model as vehicle-vitals).
- Keyless deploys via Workload Identity Federation (org policy forbids service-account keys).
- Per-environment Firebase hosting configs; dev and staging send noindex and a strict CSP.

### Added
- Repository documentation: LICENSE, CONTRIBUTING, SECURITY, SUPPORT, CODE_OF_CONDUCT, issue and PR templates, CODEOWNERS, Dependabot, EditorConfig.

## [0.1.0] - 2026-10-13

### Added
- Reorganized project into `books/`, `website/`, `brand/`, `docs/`, and `scratch/`.
- Firebase Hosting for `dev`, `staging`, and `prod` environments.
- GitHub repository under NelsonGrey with `develop`, `staging`, and `main` branches.
- GitHub Actions workflow deploying the website per branch.
- Three KDP-ready launch titles: Crawling Bugs, Roaring Dinosaurs, Working Vehicles.
