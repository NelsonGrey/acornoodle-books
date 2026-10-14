# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
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
