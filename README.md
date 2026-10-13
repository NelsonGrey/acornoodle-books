# Acornoodle Books Publishing Project

**Acornoodle Books** is the consumer-facing children's publishing imprint of **Nelson Grey LLC**. **Mark Nelson** is the author of the current books.

## Current series

**Acornoodle Discovery Coloring Books** is an unordered series for children ages 5–9.

## Repository layout

| Folder | Initiative | Contents |
| --- | --- | --- |
| `books/` | Coloring books (KDP) | Everything for producing the books (see below) |
| `website/` | Acornoodle Books website | Own git repo; `dist/` is the deployed static site |
| `brand/` | Shared brand | `acornoodle/` source assets, `proofs/` review images, brand-kit zip |
| `docs/` | Business | Business plan, brand/name screening, marketing, product development |
| `scratch/` | Throwaway | Review renders and contact sheets; safe to delete |

### `books/`

- `scripts/` — build scripts (run from anywhere; paths resolve from the repo root)
- `prompts/` — art prompt manifests
- `art/` — source art: `interior-v2/`, `cover-v3/`, `cover-v3-print/`, `print-art/`
- `print-masters/` — working print masters per title
- `builds/` — generated intermediate builds (`final-kids-v3/`)
- `kdp-packages/` — **canonical upload packages** (below)
- `archive/` — superseded work (v1 art, v2 builds, pre-Acornoodle PDFs); not upload sources

## Canonical KDP packages

Only these ZIP files in `books/kdp-packages/` are current upload packages:

- `acornoodle-books-crawling-bugs-complete-print-master.zip`
- `acornoodle-books-roaring-dinosaurs-complete-print-master.zip`
- `acornoodle-books-working-vehicles-complete-print-master.zip`
- `acornoodle-books-launch-trio-kdp-packages.zip` — convenience bundle containing the three packages above

Working print masters are under `books/print-masters/`, brand assets under `brand/acornoodle/`, and the current business plan under `docs/business-plan/`.

## Production standard

- Paperback, 8.5 x 11 inches
- 60-page black-and-white interior on white paper
- No bleed interior
- Glossy full-color cover
- Large, age-appropriate illustrations with names and short facts
- Single-sided coloring artwork
- KDP Print Previewer and a physical proof remain required for each title before publication

Everything under `books/archive/` is development-stage or historical artwork and are not KDP upload sources unless rebuilt into a canonical Acornoodle package.

## Brand status

All earlier working names are retired. Only Acornoodle Books may be used in covers, interiors, metadata, marketing, or publishing accounts.
