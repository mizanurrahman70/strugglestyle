# Extracting an Existing Design System

Goal: produce `design/system.md` in the project, a short, accurate reference that lets any future section match
the site perfectly. Base everything on the actual code; never guess. Include selectors and line numbers so it
can be verified.

## How to read the project
1. Find the pages: `index.html`, other `*.html`, and any CSS/JS files (Glob).
2. Read the `<head>`: fonts loaded (Google Fonts URL), meta theme color.
3. Read `:root` and any theme blocks: every custom property.
4. Read the base styles: `body`, `section`, `.wrap`, headings, links, focus styles.
5. Read the component styles: buttons, tags/labels, cards, links, forms, images, nav, footer.
6. Read each `<section>` in order: class/ID, layout, background, components used.
7. Read the JS: reveal/scroll animations, sliders, interactive widgets, and the data attributes they rely on.
8. Grep for counts to find the *real* conventions, e.g.:
   - `border-radius:` values (which ones are common?)
   - `@media` breakpoints
   - `padding:` on sections
   - color hex values used outside `:root` (hard-coded colors = inconsistencies to note)

## Template for design/system.md

```markdown
# Design System: <Project name>
_Last checked against code: YYYY-MM-DD_

## Files
- Main page: index.html (~N lines). CSS inline in <style> (lines A–B). JS inline / js/*.js

## Fonts
| Role | Family | Weights | Variable | Used on |
- Font loading URL:

## Color tokens
| Token | Value | Used for |
- Hard-coded colors found outside tokens (inconsistencies):

## Spacing & layout
- Container: `.wrap` max-width, side padding (desktop / mobile)
- Section padding: desktop / tablet / mobile
- Grid patterns in use (columns, gaps)
- Breakpoints: e.g. 1100px, 900px, 640px

## Shape & depth
- Radii in use (token + where)
- Shadows (token + where)
- Borders / rules

## Typography scale
| Element | Size | Weight | Line-height | Tracking |
- Section header pattern (markup): e.g. `.s-head > div > .tag + h2 + .lead`, link on right

## Components (with markup snippets)
- Buttons: classes + variants + when each is used
- Tags / labels / eyebrows
- Cards (each type)
- Links
- Images (ratio, radius, captions?)
- Forms
- Icons (style, stroke width, size)

## Motion system
- Reveal mechanism (class / data attribute / IntersectionObserver), delay variable, easing token
- Hover conventions
- Reduced-motion handling

## Signature ideas (what makes this site specific)
- e.g. Wordmark with dashed "thread" underline that animates like stitching on hover (`.wm .thread`)
- ...

## Voice & copy
- Tone (formal / friendly / technical), person (we/you), sentence length
- Typical CTA wording
- Example headline and lead from the site

## Section map
| # | ID / class | Purpose | Layout pattern | Background | Notes |

## Redesign later (existing anti-AI patterns)
- Pattern, where, which rule # in anti-AI rules
```

Keep it factual and concise. If something is inconsistent in the code (e.g. three different radii for similar
cards), record what is most common and note the outliers.
