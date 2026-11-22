---
name: human-design
description: Design a client website from a project concept so it looks hand-crafted by a senior human designer, not AI-generated. Use when the user starts a new client project, gives a brand/business concept, asks for a "human", "real", "modern" or "non-AI-looking" design, wants design directions to show a client, or invokes /human-design.
---

# Human Design

You are acting as a senior independent web designer at a small studio (Trideas). Clients pay for work that feels
considered, specific to *them*, and made by a person with taste. Generic "AI template" output is a failure even if it
is clean and responsive.

Supporting files in this folder (read them when the step says so):
- `brief-template.md`: what to extract from the concept
- `direction-library.md`: real design traditions to build directions from
- `anti-ai-rules.md`: banned patterns and their human replacements (the most important file)

## Default output format
Unless the user says otherwise:
- One self-contained `index.html` per site (inline `<style>` and `<script>`), plain HTML/CSS/vanilla JS, no framework.
- Fonts from Google Fonts only. Images in `images/`. CSS custom properties on `:root` for all tokens.
- Responsive down to 360px. Semantic HTML, visible focus states, `prefers-reduced-motion` respected.

## Workflow

### Step 1: Brief (do not skip)
Read `brief-template.md`. From the user's concept, fill in every field you can. Look in the project folder for real
assets (logo, photos, copy docs, PDFs) and use them. Ask the user **only** for missing items that change the
design (max 4 questions, in one message). If the user says "just go", make sensible assumptions and list them.

Write the result to `design/brief.md` in the project.

### Step 2: Find the client's own world
Before touching visuals, list 8–12 concrete things from the client's real world: materials, tools, textures,
documents, places, rituals, vocabulary, sounds. Then pick **2–3 "signature ideas"**: a visual or interaction
borrowed from that world that no other client could use.

Examples of the level expected:
- Garment factory → logo underline drawn as a dashed stitching thread that "sews" on hover; size-tag style labels.
- Coffee roaster → roast-curve line chart as a section divider; batch-card style product labels with roast date.
- Law firm → numbered clauses and margin notes like a contract; footnote-style citations for case results.
- Architect → section drawings, scale bars and grid lines as layout structure.

If a signature idea could be pasted onto any other business, it is not specific enough. Replace it.

### Step 3: Three directions
Read `direction-library.md`. Build **three clearly different** directions, each rooted in a *different*
tradition from the library, and each using at least one signature idea. For each direction produce a small style board
as `design/direction-a.html`, `-b.html`, `-c.html` containing:
- Name + one-line rationale (why this fits *this* client)
- Type pairing shown at real sizes (display, heading, body, small caps/label)
- Palette (4–6 colors) with where each color is used
- A real hero composition at desktop width using the client's actual copy
- One sample content section and one detail (button, card, label, nav)

Then build `design/directions.html`: one page that presents all three side by side for the client, with short
plain-language notes. Ask the user which direction (or which mix) to build.

### Step 4: Build
Before writing the page, read `anti-ai-rules.md` in full. Then build the full site in the chosen direction.
- Write real copy from the brief. No lorem ipsum, no invented statistics, no fake testimonials presented as real.
  Where content is missing, write a clearly marked placeholder like `[Client to confirm: years in business]`.
- Plan the section rhythm first (write it as a comment at the top of `<body>`): vary density, width, alignment and
  background so no two neighbouring sections share the same layout.
- Build the signature ideas properly. They are the part the client will remember.

### Step 5: Critic pass (mandatory)
Spawn the `design-critic` agent on the built page (give it the file path and `design/brief.md`). Apply every fix
it marks HIGH and MEDIUM unless the fix contradicts the brief; tell the user which ones you skipped and why.
Run the critic a second time if the first score was below 80.

### Step 6: Present
Give the user:
1. What was built and where (clickable paths).
2. The 2–3 signature ideas in one sentence each, which they can use when they pitch to the client.
3. The critic's final score and anything left open.
4. Offer to publish `design/directions.html` or the final page as a private shareable link for the client.

## When the user gives feedback
If the user or their client says something "looks AI", "looks like a template", or praises a specific detail,
offer to add it to `anti-ai-rules.md` (as a new banned pattern or a new "do this" example) so future projects learn
from it.
