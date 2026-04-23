# GG33Academy.org Cleanup + SEO Foundation Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Clean up crawl/indexation issues, make `slot.html` the clear canonical game page, keep `master-vault.html` private, and prepare the site for evergreen search growth without breaking the live experience.

**Architecture:** Keep the existing static-site structure. Do not redesign the site framework. Make small, controlled edits to existing HTML files, `sitemap.xml`, and `robots.txt`. Treat `slot.html` as the authoritative game URL. Treat `slot_v4.html` as backup cruft, not a public entrypoint.

**Tech Stack:** Static HTML/CSS/JS, GitHub Pages-style repo layout, XML sitemap, robots.txt, JSON-LD schema.

---

## Ground Truth Collected

- Repo: `/home/vboxuser/Desktop/claude_data/garrygrinberg.github.io`
- Live game path in site links: `slot.html`
- Internal refs to `slot.html`: 61
- Internal refs to `slot_v4.html`: 0
- `slot_v4.html` canonical already points to `https://www.gg33academy.org/slot.html`
- `master-vault.html` is secret/internal and should not be public or indexed
- `sitemap.xml` currently lists only 4 URLs while repo contains 36 HTML files
- Many important pages have no semantic `<h1>`
- `lifepath.html` still contains `garrygrinberg.github.io` canonicals/OG URLs

---

## Rules for Implementation

1. Do **not** break `slot.html` behavior.
2. Do **not** expose `master-vault.html` more than it already is.
3. Do **not** include backup, secret, verification, or staging pages in the sitemap.
4. Prefer minimal edits over broad rewrites.
5. Verify every page edit by reading the file back and checking the exact tag exists.
6. No speculative claims about Gary beyond what is already in repo copy.

---

## Phase 1 — Canonical Surface Cleanup

### Task 1: Save a repo inventory snapshot

**Objective:** Capture the current public HTML surface before edits.

**Files:**
- Create: `docs/plans/site-inventory-2026-04-21.txt`

**Step 1: Generate HTML inventory**

Run:

```bash
cd /home/vboxuser/Desktop/claude_data/garrygrinberg.github.io
find . -type f -name '*.html' | sort
```

**Step 2: Save the output**

Store the exact list in:

```text
./about.html
./archive.html
./index.html
./lifepath.html
./master-vault.html
./privacy-policy.html
./slot.html
./slot_v4.html
./terms.html
./newsletters/...
```

**Step 3: Verify file exists**

Run:

```bash
test -f docs/plans/site-inventory-2026-04-21.txt && echo OK
```

Expected: `OK`

---

### Task 2: Mark `slot.html` as the canonical game page in planning notes

**Objective:** Make the repo’s intended public game URL explicit.

**Files:**
- Modify: `docs/plans/2026-04-21-gg33-site-cleanup-plan.md`

**Step 1: Add note if missing**

Ensure the plan explicitly states:

```md
- Canonical public game URL: `slot.html`
- Backup/old variant: `slot_v4.html`
```

**Step 2: Verify with search**

Run:

```bash
grep -n "Canonical public game URL" docs/plans/2026-04-21-gg33-site-cleanup-plan.md
```

Expected: one matching line.

---

### Task 3: De-index `master-vault.html`

**Objective:** Stop the secret vault page from being an indexable public page.

**Files:**
- Modify: `master-vault.html`

**Step 1: Add or replace robots meta**

Inside `<head>`, ensure this exact tag exists:

```html
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">
```

**Step 2: Add a canonical away from itself only if appropriate**

Preferred minimal option: no canonical change unless current canonical is self-referential and harmful.

**Step 3: Verify**

Run:

```bash
grep -n 'noindex, nofollow, noarchive, nosnippet' master-vault.html
```

Expected: one match.

---

### Task 4: Decide how to handle `slot_v4.html`

**Objective:** Keep the backup out of public SEO paths without deleting history blindly.

**Files:**
- Modify: `slot_v4.html`
- Optional create: `docs/plans/slot-v4-notes.md`

**Step 1: Add backup note comment at top of file**

Insert a clear HTML comment near the top:

```html
<!-- Backup/legacy variant of slot game. Public canonical game page is /slot.html. Do not link or include in sitemap. -->
```

**Step 2: Change robots to noindex**

Set:

```html
<meta name="robots" content="noindex, follow">
```

Keep canonical pointing to `https://www.gg33academy.org/slot.html`.

**Step 3: Verify**

Run:

```bash
grep -n 'Backup/legacy variant' slot_v4.html
grep -n '<meta name="robots" content="noindex, follow">' slot_v4.html
```

Expected: two matches total.

---

## Phase 2 — Sitemap + Indexation Hygiene

### Task 5: Replace the sitemap with an intentional indexable-only list

**Objective:** Expand coverage for real pages and exclude secret/backup/junk pages.

**Files:**
- Modify: `sitemap.xml`

**Include:**
- `https://www.gg33academy.org/index.html`
- `https://www.gg33academy.org/about.html`
- `https://www.gg33academy.org/archive.html`
- `https://www.gg33academy.org/slot.html`
- `https://www.gg33academy.org/lifepath.html` if kept public
- `https://www.gg33academy.org/privacy-policy.html`
- `https://www.gg33academy.org/terms.html`
- all real `newsletters/*.html` pages except any promotional junk page the user does not want indexed

**Exclude:**
- `master-vault.html`
- `slot_v4.html`
- verification HTML files
- duplicate/legacy pages

**Step 1: Build a clean URL list**

Use exact `<url>` blocks like:

```xml
<url>
  <loc>https://www.gg33academy.org/slot.html</loc>
  <priority>0.9</priority>
  <changefreq>weekly</changefreq>
</url>
```

**Step 2: Preserve XML header and namespace**

Root element must remain:

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
```

**Step 3: Verify XML parses**

Run:

```bash
python - <<'PY'
import xml.etree.ElementTree as ET
ET.parse('sitemap.xml')
print('OK')
PY
```

Expected: `OK`

**Step 4: Count URLs**

Run:

```bash
python - <<'PY'
import re
print(len(re.findall(r'<loc>', open('sitemap.xml').read())))
PY
```

Expected: materially more than 4.

---

### Task 6: Tighten `robots.txt` comments if needed

**Objective:** Keep robots behavior aligned with the new sitemap.

**Files:**
- Modify: `robots.txt`

**Step 1: Keep the global allow unless intentionally changing**

Core should remain valid:

```txt
User-agent: *
Allow: /
```

**Step 2: Confirm sitemap reference stays correct**

Must include:

```txt
Sitemap: https://www.gg33academy.org/sitemap.xml
```

**Step 3: Optional note**

Add a comment clarifying that secret pages are excluded by page-level `noindex`, not by robots blocking.

**Step 4: Verify**

Run:

```bash
grep -n 'Sitemap:' robots.txt
```

Expected: one match.

---

## Phase 3 — Semantic HTML Cleanup

### Task 7: Add a real H1 to `about.html`

**Objective:** Give the About page a semantic primary heading.

**Files:**
- Modify: `about.html`

**Step 1: Add H1 in page header/container**

Preferred text:

```html
<h1>About Gary Grinberg</h1>
```

**Step 2: Keep visual style aligned**

If needed, reuse existing page-title styles or add an H1 style near the current header styles.

**Step 3: Verify**

Run:

```bash
grep -n '<h1>About Gary Grinberg</h1>' about.html
```

Expected: one match.

---

### Task 8: Add a real H1 to `archive.html`

**Objective:** Give the archive page a semantic primary heading.

**Files:**
- Modify: `archive.html`

**Step 1: Add H1 near the page header**

Use:

```html
<h1>GG33 Newsletter Archive</h1>
```

**Step 2: Verify**

Run:

```bash
grep -n '<h1>GG33 Newsletter Archive</h1>' archive.html
```

Expected: one match.

---

### Task 9: Add a real H1 to `slot.html`

**Objective:** Make the core game page semantically clear.

**Files:**
- Modify: `slot.html`

**Step 1: Add H1 in visible hero/header area**

Use:

```html
<h1>GG33 Life Path Calculator & Lucky Number Slot Game</h1>
```

If this is too visually heavy, keep it visually styled down, but do not hide it with junk tactics.

**Step 2: Verify**

Run:

```bash
grep -n 'GG33 Life Path Calculator & Lucky Number Slot Game' slot.html
```

Expected: one match.

---

### Task 10: Add H1 to each newsletter page

**Objective:** Convert article title divs into proper article headings.

**Files:**
- Modify: `newsletters/*.html`

**Step 1: Replace or wrap `.issue-title` with `<h1>`**

For example, convert:

```html
<div class="issue-title">The last year of normal. Are you ready?</div>
```

Into:

```html
<h1 class="issue-title">The last year of normal. Are you ready?</h1>
```

**Step 2: Apply same pattern to all newsletter files**

**Step 3: Verify count**

Run:

```bash
python - <<'PY'
from pathlib import Path
import re
files=list(Path('newsletters').glob('*.html'))
missing=[]
for f in files:
    t=f.read_text()
    if '<h1' not in t:
        missing.append(f.name)
print('missing', len(missing))
for m in missing: print(m)
PY
```

Expected: `missing 0`

---

## Phase 4 — Canonical / Metadata Corrections

### Task 11: Fix `lifepath.html` domain references

**Objective:** Stop splitting canonical signals across `garrygrinberg.github.io` and `gg33academy.org`.

**Files:**
- Modify: `lifepath.html`

**Step 1: Replace canonical**

Change:

```html
<link rel="canonical" href="https://garrygrinberg.github.io/lifepath.html">
```

To:

```html
<link rel="canonical" href="https://www.gg33academy.org/lifepath.html">
```

**Step 2: Replace OG URL**

Change:

```html
<meta property="og:url" content="https://garrygrinberg.github.io/lifepath.html">
```

To:

```html
<meta property="og:url" content="https://www.gg33academy.org/lifepath.html">
```

**Step 3: Replace schema URL**

Change schema `url` to the live domain.

**Step 4: Verify**

Run:

```bash
grep -n 'gg33academy.org/lifepath.html' lifepath.html
```

Expected: multiple matches.

---

### Task 12: Normalize homepage canonical formatting

**Objective:** Keep the live domain format consistent.

**Files:**
- Modify: `index.html`

**Step 1: Make canonical explicit**

Preferred:

```html
<link rel="canonical" href="https://www.gg33academy.org/">
```

**Step 2: Align `og:url`**

Use:

```html
<meta property="og:url" content="https://www.gg33academy.org/">
```

**Step 3: Verify**

Run:

```bash
grep -n 'https://www.gg33academy.org/' index.html
```

Expected: canonical and og:url both match.

---

## Phase 5 — Article Metadata Improvement

### Task 13: Clean junk keyword meta patterns on top pages

**Objective:** Remove obviously weak keyword stuffing without rewriting the whole content system.

**Files:**
- Modify: `index.html`
- Modify: `about.html`
- Modify: `archive.html`
- Modify: `slot.html`
- Modify: `lifepath.html`
- Modify: `newsletters/the-last-year-of-normal.html`
- Modify: `newsletters/is-2027-your-money-year.html`
- Modify: `newsletters/your-birthday-explains-everything.html`

**Step 1: Replace ugly keyword strings**

Example current weak pattern:

```html
<meta name="keywords" content="GG33, numerology, life path, Gary Numbers Guy, the, last, year, of, normal">
```

Replace with tightly scoped phrases, or delete entirely if not useful.

**Step 2: Do not mass-generate nonsense**

Use 5–10 tight phrases max if retained.

**Step 3: Verify by spot reading**

Read each changed file and inspect the exact meta line.

---

### Task 14: Add `Article` schema to newsletter pages

**Objective:** Make article pages machine-readable and consistent.

**Files:**
- Modify: `newsletters/*.html`

**Step 1: Add JSON-LD block near the top of each article page**

Template:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "The last year of normal. Are you ready?",
  "description": "Gary on why money is the foundation, 2027 as an 11 Universal Year, and how your environment determines your destiny.",
  "author": {
    "@type": "Person",
    "name": "Gary Grinberg",
    "alternateName": "The Numbers Guy"
  },
  "publisher": {
    "@type": "Organization",
    "name": "GG33 Numerology Academy",
    "url": "https://www.gg33academy.org/"
  },
  "mainEntityOfPage": "https://www.gg33academy.org/newsletters/the-last-year-of-normal.html"
}
</script>
```

**Step 2: Use page-specific headline/description/URL**

**Step 3: Verify one page first, then propagate**

Run:

```bash
grep -n '"@type": "Article"' newsletters/the-last-year-of-normal.html
```

Expected: one match.

---

## Phase 6 — Internal Linking + Content Direction

### Task 15: Improve nav wording for the core game

**Objective:** Make the game CTA clearer than generic “Game”.

**Files:**
- Modify: `index.html`
- Modify: `about.html`
- Modify: `archive.html`
- Modify: `privacy-policy.html`
- Modify: `terms.html`
- Modify: `slot.html`
- Modify: `newsletters/*.html`

**Step 1: Replace nav label text only**

Change visible nav text from:

```html
Game
```

To either:

```html
Life Path Game
```

or

```html
Unlock Your Numbers
```

Use one label consistently site-wide.

**Step 2: Do not change the href**

Keep href pointing to `slot.html`.

**Step 3: Verify**

Search all HTML for old label if changed.

---

### Task 16: Add a homepage support link to `lifepath.html`

**Objective:** Use the calculator page as a search-supporting entrypoint into the main game.

**Files:**
- Modify: `index.html`

**Step 1: Add one supporting link block**

Example copy:

```html
<p><a href="lifepath.html">Not ready to spin yet? Start with the Life Path Calculator.</a></p>
```

**Step 2: Place it below the main game CTA or in the feature section**

**Step 3: Verify**

Run:

```bash
grep -n 'Life Path Calculator' index.html
```

Expected: new supporting link appears.

---

## Phase 7 — Duplicate / Low-Value URL Review

### Task 17: Review duplicate Hidden 13 article pair

**Objective:** Resolve duplicate-ish content before it confuses search crawlers.

**Files:**
- Review: `newsletters/hidden-13-system-controls-everything.html`
- Review: `newsletters/hidden-13-system-that-controls-everything.html`
- Modify one or both after comparison

**Step 1: Diff both files**

Run:

```bash
diff -u newsletters/hidden-13-system-controls-everything.html newsletters/hidden-13-system-that-controls-everything.html | sed -n '1,120p'
```

**Step 2: Decide**

If they are materially identical:
- keep one URL
- de-index the other or remove from sitemap/internal linking

If they differ materially:
- keep both but sharpen titles/descriptions so they target different intent

**Step 3: Verify chosen loser is not in sitemap**

Run:

```bash
grep -n 'hidden-13-system-controls-everything\|hidden-13-system-that-controls-everything' sitemap.xml
```

---

### Task 18: Review promotional page `gg33-misses-you-26-off.html`

**Objective:** Decide whether a promotional email-style page should be indexed.

**Files:**
- Review: `newsletters/gg33-misses-you-26-off.html`

**Step 1: Read the page**

If it is thin/promo-only, add:

```html
<meta name="robots" content="noindex, follow">
```

and exclude it from sitemap.

**Step 2: Verify**

Run:

```bash
grep -n 'noindex, follow' newsletters/gg33-misses-you-26-off.html
```

---

## Phase 8 — Verification

### Task 19: Run a final repo-wide verification pass

**Objective:** Prove the cleanup happened and didn’t regress obvious basics.

**Files:**
- No new files required

**Step 1: Check sitemap count**

```bash
python - <<'PY'
import re
print('sitemap_urls', len(re.findall(r'<loc>', open('sitemap.xml').read())))
PY
```

**Step 2: Check for missing H1 on key public pages**

```bash
python - <<'PY'
from pathlib import Path
pages=['index.html','about.html','archive.html','slot.html','lifepath.html']
for p in pages:
    t=Path(p).read_text()
    print(p, '<h1' in t)
PY
```

Expected: all `True`

**Step 3: Check noindex pages**

```bash
grep -n 'noindex' master-vault.html slot_v4.html newsletters/gg33-misses-you-26-off.html || true
```

**Step 4: Check live domain canonicals**

```bash
grep -Rni 'garrygrinberg.github.io' *.html newsletters lifepath.html slot.html about.html archive.html index.html || true
```

Expected: ideally zero remaining live-domain canonical/OG references for public pages.

---

## Suggested Commit Breakdown

1. `docs: add gg33 site cleanup implementation plan`
2. `seo: deindex secret and backup pages`
3. `seo: expand sitemap and normalize indexable urls`
4. `seo: add h1 tags to core and newsletter pages`
5. `seo: fix lifepath canonical domain references`
6. `seo: add article schema and clean metadata`
7. `content: improve game nav labeling and internal links`

---

## Recommended Execution Order

1. Task 3 — de-index `master-vault.html`
2. Task 4 — noindex `slot_v4.html`
3. Task 5 — rewrite sitemap
4. Task 7–10 — add H1s
5. Task 11–12 — canonical fixes
6. Task 17–18 — duplicate/low-value page decisions
7. Task 14–16 — schema and internal linking improvements
8. Task 19 — final verification

---

## End State

When this plan is complete:
- `slot.html` is the undisputed game entrypoint
- `slot_v4.html` is non-indexed backup cruft
- `master-vault.html` is non-indexed and harder to surface accidentally
- sitemap covers real public pages
- key pages have semantic H1s
- `lifepath.html` points to the live domain
- newsletters are machine-readable articles instead of semantically sloppy pages
- the site is structurally cleaner and ready for evergreen content expansion
