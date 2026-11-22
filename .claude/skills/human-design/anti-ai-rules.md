# Anti-AI Rules

Patterns that make a site look AI-generated or template-made, and what a human designer does instead.
**Every rule applies unless the brief explicitly asks for it.** Breaking a rule on purpose is fine; breaking it by
default is not. If you break one, leave a short HTML comment explaining why.

## Typography
1. **Inter, Inter Tight, Poppins, Montserrat, Space Grotesk, DM Sans, Plus Jakarta Sans as the default.** ❌
   → Choose type from the direction library for *this* client. Rotate fonts between projects.
2. **One sans-serif in 3 weights for everything.** ❌ → Real pairing: display face with character + quiet text face.
3. **Even type scale (16/20/24/32/40/48).** ❌ → Dramatic contrast: small body, very large display, few sizes in between.
4. **Every heading center-aligned, two lines, same length.** ❌ → Mostly left-aligned; vary line lengths; let a
   headline run long or be one word.
5. **Gradient text on headlines.** ❌ → Solid color; emphasis through italic, weight, or a single word in accent color.
6. **Tight negative letter-spacing on every heading (-0.025em everywhere).** ❌ → Tune tracking per face and size.
7. **No typographic details.** ❌ → Use proper quotes (" "), en dashes for ranges (9–5), non-breaking spaces,
   tabular numbers in tables, small caps for labels, real italics.

## Layout & composition
8. **Centered hero: pill badge → big headline → subtitle → two buttons → screenshot/blob.** ❌
   → Hero built around the client's strongest real asset (a photo, a product, a number, a quote). Asymmetric.
9. **"Three equal cards with an icon, title and two lines" sections.** ❌ → Vary counts (2, 4, 5), sizes, and
   formats: lists, tables, numbered steps, a single big statement, an image grid with captions.
10. **Every section the same width, padding and structure.** ❌ → Plan a rhythm: wide, narrow, full-bleed, dense,
    airy. Neighbouring sections must differ.
11. **Bento grids of rounded tiles.** ❌ (the 2024–26 AI favourite) → Only if content truly has different weights.
12. **Stat row with icons ("10+ years · 500+ clients · 24/7 support").** ❌ → Put one real number in context,
    in a sentence or a chart, with a source or a date.
13. **Logo wall of grey logos labeled "Trusted by".** ❌ unless the logos are real and permitted.
14. **Everything perfectly symmetrical.** ❌ → Intentional offsets, overlaps, elements that bleed off the grid.
15. **FAQ accordion + newsletter + CTA band at the bottom of every page by default.** ❌ → Only what the brief needs.

## Shape, depth, surface
16. **Rounded everything (16–32px radius on every card, image and button) + pill buttons.** ❌
    → Choose one corner logic per direction: sharp, slightly soft (2–6px), or one deliberate round element.
17. **Soft blurry drop shadows on floating cards.** ❌ → Flat with rules/borders, or a hard offset shadow, or real
    photographic depth.
18. **Glassmorphism (blur + translucent white + thin border).** ❌
19. **Purple-to-blue, or teal-to-violet gradients; mesh gradient blobs; glowing orbs.** ❌
20. **Dot-grid or noise backgrounds added "for texture".** ❌ → Texture from real photography or meaningful linework.

## Color
21. **SaaS palette: indigo/violet primary, slate greys, mint success.** ❌ → Palette derived from the client's
    materials, place, logo or photos. Name each color after something real (e.g. "kiln clay", "indigo vat").
22. **Too many accents.** ❌ → Mostly neutrals + one accent used rarely so it means something.
23. **Pure #FFFFFF background + #000 text by default.** ❌ → Slightly tinted paper and ink that fit the direction
    (unless a stark direction like Swiss calls for pure).
24. **Pale tinted chip/tag with a colored dot before it (e.g. mint pill "● Sustainability").** ❌ → Plain small caps
    label, a number, or a rule.

## Imagery & icons
25. **Stock photos of smiling diverse teams at laptops / handshakes.** ❌ → Real photos of the client's place,
    product, people. If none exist, say so and propose a shot list; use honest placeholders.
26. **Generic line-icon sets (Lucide/Feather/Heroicons) next to every heading.** ❌ → No icon, or custom simple
    SVGs drawn for the client's world, used only where they help scanning.
27. **3D blobby illustrations, isometric people, AI-generated art.** ❌
28. **Images without captions or context.** ❌ → Caption real images (what, where, who).

## Copy
29. **Words: elevate, seamless, unlock, empower, revolutionize, cutting-edge, next-level, game-changer,
    world-class, innovative solutions, tailored, robust, leverage, journey, delve, "in today's fast-paced world".** ❌
30. **Headlines like "Your Partner in X" / "Where X Meets Y" / "X, Reimagined".** ❌ → Say the specific thing:
    who, what, where, how many, how fast.
31. **Three-adjective rhythm ("Fast. Reliable. Affordable.").** ❌
32. **Em-dash heavy sentences everywhere.** ❌ → Vary punctuation; write like the client speaks.
33. **Invented stats, fake testimonials, fake awards.** ❌ → Real or clearly marked `[Client to confirm]`.
34. **CTA "Get Started" / "Learn More".** ❌ → Specific: "Request a sample pack", "Book a factory visit",
    "WhatsApp the bakery".

## Motion & interaction
35. **Fade-up-on-scroll on every element with staggered delays.** ❌ → One or two meaningful motions, tied to a
    signature idea (e.g. the thread that sews). Everything else appears instantly.
36. **Hover lift + shadow on every card.** ❌ → Hover states that fit the direction (underline, color, image change).
37. **Arrow icon that slides right on every link/button hover.** ❌ (use once, not everywhere)
38. **Marquee of logos/words** ❌ unless the direction is brutalist and it is the one loud gesture.
39. **Custom cursors, parallax everything, scroll-jacking.** ❌

## Structure & honesty
40. **Generic section order (Hero → Features → How it works → Testimonials → Pricing → FAQ → CTA).** ❌
    → Order sections by what *this* audience needs to believe, in order.
41. **Footer with 4 equal columns of links that go nowhere.** ❌ → Real address, real hours, real contact, a map link,
    a small human detail (e.g. "Factory visits Sun–Thu, call ahead").

---

## Signs a page *feels* human (aim for these)
- You can tell what the business is from the first screen **without reading the headline**.
- At least one detail that would make the client say "how did you know that about us?"
- Some imperfection by intent: a handwritten note, a slightly rotated label, an unexpected crop.
- Content density varies: some screens are almost empty, some are rich with detail.
- Typography alone carries much of the identity.
- The copy contains names, places, numbers, and dates.

## Project log (add lessons here)
<!-- Format: YYYY-MM-DD · client · what happened · new rule or example -->
