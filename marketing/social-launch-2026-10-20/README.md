# Acornoodle Books Social Launch Kit

Post-ready campaign materials for the October 20, 2026 launch of **Crawling Bugs**, **Roaring Dinosaurs**, and **Working Vehicles**.

## What is included

- 15 finished JPG graphics: five concepts sized for Pinterest, Instagram, and Facebook
- `POST-COPY.md`: platform-ready captions, titles, descriptions, alt text, hashtags, and profile copy
- `POSTING-CALENDAR.md`: a practical two-week launch sequence
- `content-calendar.csv`: sortable campaign schedule and destination URLs
- `scripts/build_social_launch_kit.py`: repeatable source builder
- `social-kit-contact-sheet.jpg`: visual proof of the whole set

## Image inventory

| Asset | Purpose |
| --- | --- |
| `01-launch-trio.jpg` | Launch announcement and three-book overview |
| `02-crawling-bugs.jpg` | Crawling Bugs title spotlight |
| `03-roaring-dinosaurs.jpg` | Roaring Dinosaurs title spotlight |
| `04-working-vehicles.jpg` | Working Vehicles title spotlight |
| `05-inside-the-books.jpg` | Product-format and learning-value explainer |

Each asset is exported in:

- Pinterest: 1000 × 1500 px
- Instagram: 1080 × 1350 px
- Facebook: 1200 × 1500 px

## Campaign links

- Launch Library: https://acornoodlebooks.com/launch
- All books: https://acornoodlebooks.com/books
- Crawling Bugs: https://www.amazon.com/dp/B0HNDYVMT5
- Roaring Dinosaurs: https://www.amazon.com/dp/B0HNF3DYF5
- Working Vehicles: https://www.amazon.com/dp/B0HNHC9C1D

## Publishing notes

1. Put `https://acornoodlebooks.com/launch` in the Instagram bio before the first post.
2. Use the direct Amazon URL as the Pinterest destination for each title spotlight. Use the Launch Library for the trio and inside-the-books posts.
3. Facebook captions may include the relevant direct link.
4. Add the supplied alt text in each platform’s accessibility field rather than appending it to the visible caption.
5. Avoid asking children to comment, submit artwork, send photos, or enter a contest. Calls to action are written for parents, grandparents, educators, librarians, homeschool families, and gift buyers.
6. Organic assets say “Available now on Amazon” but do not state a price, rating, bestseller status, inventory level, shipping promise, or review claim.

## Rebuild

From the repository root:

```bash
python3 scripts/build_social_launch_kit.py
```

The builder composes approved repository assets; it does not modify the book art, cover art, or logos.
