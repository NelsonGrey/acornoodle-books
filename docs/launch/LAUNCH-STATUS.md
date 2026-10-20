# Launch status

**Public launch: 2026-10-20.** The full site is live at https://acornoodlebooks.com (production `main`, `SHOW_COMING_SOON=false`). Three titles are live on Amazon.com.

## What is live

| Item | State |
| --- | --- |
| Website | Live; Home, Launch, Books, Inside, About, Support, Privacy, Terms, Cookies |
| Books on Amazon | Crawling Bugs (`B0HNDYVMT5`), Roaring Dinosaurs (`B0HNF3DYF5`), Working Vehicles (`B0HNHC9C1D`); linked from the Books and Launch pages |
| Other nine titles | "Coming soon" |
| Support email | support@acornoodlebooks.com (Support and Privacy pages) |
| Social profiles | Pinterest, Instagram, Facebook linked in the site footer |
| SEO files | `robots.txt`, `sitemap.xml`, canonical, Open Graph, Twitter card, 404 page |
| Layout | Centered 1280px column, white outside, header and footer full width (global rule) |
| Analytics | None by design (children's publisher; see the Cookies and Privacy pages) |

## Verified versus not

- Verified: the live site served the expected pages, Amazon links, cover images, support email and layout CSS after each deploy; CI and deploys passed on every promotion.
- Verified in a browser: the Amazon links open the normal amazon.com listing for visitors who are not signed in to an Amazon Business account.
- Not verified: the Crawling Bugs and Working Vehicles listing text (Amazon blocked automated reads); the Facebook, Pinterest, and Instagram URLs; Pinterest domain verification; real Google sign-in beyond the popup on dev and staging.

## Follow-ups

1. **Google Search Console** (owner action): add `acornoodlebooks.com` as a domain property (DNS TXT record), submit `https://acornoodlebooks.com/sitemap.xml`, request indexing for Home, Books, and Launch.
2. **Curious Fish (renamed from Lonely Fish, 2026-10-20):** site, manifests, and cover script use the new title; the `lonely-fish` slug and local art folders are unchanged. Check the interior PDF and print master for the old title before the book is printed or published.
3. **KDP:** confirm the AI-generated content disclosure was made for the three live books, and click through all three listings.
4. **Ages:** the site and covers say "Ages 5–9". A move to "Ages 3 and up" was discussed and is on hold; it would touch the site, cover and print-master scripts, brand guide, marketing docs, the legal pages, and the KDP listings.
5. **Structured data:** `Book` and `Organization` JSON-LD is not added yet.
6. **Privacy page date:** still "Effective October 10, 2026" although the contact and retailer wording changed on launch day; decide whether to bump it.
7. **Digital coloring books:** printable PDFs sold through a third party (Etsy or Gumroad) were discussed as the option that fits the no-data rule; not started.
8. **Other sites:** the global 1280px layout rule (`~/.claude/CLAUDE.md`) is applied here and in Wishlist Wizard only.

## Incident notes

- 2026-10-20: merging `staging` into `main` deleted the `staging` branch because the repo had "Automatically delete head branches" on. The branch was restored at the `main` commit and the setting is now off. Keep it off.

## Rollback

Set `SHOW_COMING_SOON` to `true` in the `production` GitHub Environment and re-run Deploy Website on `main`. That serves the coming-soon page again.
