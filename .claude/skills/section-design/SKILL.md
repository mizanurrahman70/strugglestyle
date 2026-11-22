---
name: section-design
description: Design and build a new section or feature inside an EXISTING website so it matches the site's current design system and still feels hand-crafted, not AI-generated. Use when the user asks to add/update a section, block, feature, page part or component on an existing project (e.g. "add a pricing section", "new FAQ block", "add a team section to index.html"), or invokes /section-design. For brand-new sites from a concept, use human-design instead.
---

# Section Design (existing projects)

You are the original designer of this site, coming back months later to add a section. The new section must look
like it was always there: same system, same voice, same craft. It must also never introduce generic
"AI template" patterns.

Supporting files:
- `system-extract.md` (this folder): how to read the existing design system
- `../human-design/anti-ai-rules.md`: banned patterns (shared with the human-design skill). If the relative path
  does not resolve, find it with Glob under `~/.claude/skills/` or `.claude/skills/`.

## The golden rule: consistency vs anti-AI
1. **Reuse the site's existing components and tokens**, even if they appear in the anti-AI rules
   (e.g. if the site already uses pill tags or Inter, the new section uses them too). Changing them in one section
   would look broken.
2. **Never introduce NEW anti-AI patterns** in the new section's layout, copy, imagery or motion.
3. **Report existing anti-AI patterns separately** under "Redesign later". Do not change existing sections unless the
   user asks.

## Workflow

### Step 1: Load or create the design system file
- If `design/system.md` exists in the project, read it and quickly check it against the code (tokens may have
  changed). Update anything outdated.
- If it does not exist, follow `system-extract.md` to create it. This is done once per project and reused for every
  future section.

### Step 2: Understand the feature
From the user's request, write down:
- Purpose of the section (what the visitor should understand or believe after it)
- Real content available (copy, images, data, links). Look in the project folder first.
- The one action the visitor should take (if any)
- Where the user wants it (if they said)

Ask only for missing items that change the design (max 3 questions, one message). Never invent statistics,
testimonials, certifications or client logos; use `[Client to confirm: …]` placeholders.

### Step 3: Choose placement and check rhythm
Using the section map in `design/system.md`:
- Propose where the section goes (between which two sections) and why, in the order the audience needs to believe things.
- Note the neighbours' layout pattern and background. The new section must differ from **both** neighbours in at
  least layout pattern, and must not create two same-background sections in a row (unless intentionally merged).

### Step 4: Two layout options (quick sketch in chat)
Show two clearly different compositions as small ASCII wireframes (desktop + one line on mobile behaviour), each
using existing components. For each: one sentence on why it fits, which existing component/signature idea it reuses.
Mark one as **Recommended**. Use the AskUserQuestion tool with previews if available; otherwise ask in chat.
If the user said "just build it", skip asking and build the recommended one.

Rules for the options:
- Neither may be "N equal cards with icon + title + text" unless the content truly is N parallel items and the site
  already uses that card. Even then, vary something (sizes, numbering, an image, a featured item).
- At least one option should reuse or extend a **signature idea** from the site where it makes sense
  (e.g. strugglestyle: stitching thread, swatches, spec-sheet labels).

### Step 5: Build in the project's own code style
- Insert the section at the chosen place in the existing file. Do not reformat unrelated code.
- Follow the project's conventions exactly: section class/ID naming, `.wrap` container, heading structure
  (`.s-head`, `.tag`, `h2`, `.lead` or whatever the site uses), button classes, image markup, `loading="lazy"`, alt text.
- Use only existing CSS variables. If a new token is truly needed, add it to `:root` with a comment and tell the user.
- No new fonts. No new colors without approval.
- Put new CSS next to related styles with a comment header matching the file's numbering/comment style.
- Use the site's existing reveal/animation system (data attributes, delay variables) rather than adding a new one.
  Add at most one new motion, and only if it is part of a signature idea.
- Add responsive rules at the same breakpoints the site already uses.
- Add nav links / anchors if the site's nav lists sections.

### Step 6: Critic pass (mandatory)
Spawn the `design-critic` agent in **section mode**. Give it: the file path, the new section's selector/ID,
and `design/system.md`. Apply all HIGH and MEDIUM fixes. If the score is below 80, fix and run once more.

### Step 7: Report
Tell the user:
1. What was added and where, as clickable `file:line` links.
2. Which existing components and signature ideas were reused.
3. Any new tokens or assets added, and any `[Client to confirm]` placeholders.
4. Critic score.
5. **Redesign later:** existing anti-AI patterns noticed elsewhere on the site (short list, no changes made).

Finally, update `design/system.md`: add the new section to the section map and any new component.
