# Category hover clips — concepts & prompts

Two short, silent, looping clips for the Denim and Woven cards in "Offering a diverse range of products"
(`products.html`, `index.html`). Card frame is **3:4 portrait**, so render at 720×960 or 1080×1440.

`make_clips.py` renders both concepts from the site's own photos and 3D avatar renders (motion graphics, not AI
footage). The prompts below are for an AI video tool (Veo, Sora, Kling, Runway) to produce live footage
of the same concepts later. Drop the result in this folder with the same filename and the cards pick it up.

---

## 1. Denim — "Stitch & Reveal"

**Idea:** the clip opens on raw indigo fabric being sewn. The seam splits open like a jacket front and reveals
the finished garment on a model. Then detail panels slide past and the fabric closes again. It reads as
"from fabric to finished denim".

**Beats (≈10 s, seamless loop)**
| Time | Beat |
|---|---|
| 0.0–2.0 s | Faded indigo denim fills the frame and drifts slowly. A double row of gold contrast stitching sews itself down the centre. The serif title **Denim** rises in, with "Jeans · Jackets · Vests" under it. |
| 2.0–2.8 s | The fabric splits along the stitch line and both halves slide apart, revealing the model behind. |
| 2.8–4.6 s | Slow push-in on the jacket-and-jeans look. A pulsing hotspot marks the button placket and a label chip slides in: "Hand-finished vintage wash". |
| 4.6–6.8 s | Three detail panels (button placket · distressed knee · hem) slide in from alternating directions, each with a slow parallax drift. |
| 6.8–8.6 s | The panels slide away to reveal a second look, a vest with a panelled maxi skirt. Label chip: "Panelled maxi skirt · 12 oz". |
| 8.6–10 s | The fabric halves close back over the frame with the stitch and title, then fade back to the opening frame for a clean loop. |

**AI video prompt**
> Vertical 3:4 fashion product film, 10 seconds, seamless loop, no audio. Extreme close-up of faded light-blue
> vintage-wash denim fabric filling the frame, soft studio light raking across the twill weave. A double row
> of golden contrast stitching is sewn down the centre of the fabric in one continuous motion, needle visible.
> The fabric parts along the new seam like a jacket opening, revealing a young woman in a matching
> light-wash denim jacket and wide-leg jeans standing against a seamless pale grey studio backdrop. The camera
> slowly pushes in. Cut to macro detail shots of metal shank buttons, a distressed knee and a raw hem, each
> sliding across the frame. End on the model in a ribbed denim vest and a long panelled denim skirt, then
> the denim fabric closes over the frame again. Clean, premium, editorial, natural colour, shallow depth of field.

**Negative prompt:** text, logos, watermarks, distorted hands, extra limbs, flicker, warped fabric, dark grading.

---

## 2. Woven — "3D Fitting Room"

**Idea:** a digital fitting room. A 3D avatar stands on a studio floor and a green scan line sweeps down
the body, re-dressing it into the next woven look as it passes. The scan line reads as live motion, and the
look counter, fabric label and colour swatch make clear this is a sampling tool and not a still photo.

**Beats (≈9.6 s, six looks × 1.6 s, seamless loop)**
| Each look | Beat |
|---|---|
| 0.0–0.7 s | A green scan line with a glow and a fine grid band sweeps top to bottom. Above the line the avatar wears the new look; below it, the previous one. |
| 0.7–1.6 s | Hold. The avatar "breathes" slightly. The bottom label (garment name, fabric and a round fabric swatch) slides up, and the "LOOK 0X / 06" counter ticks over. |

Looks: shirt & trousers (white/sage) → shirt & trousers (sky/white) → satin blazer suit (champagne) →
satin blazer suit (emerald) → linen maxi dress (sage) → satin shirt & skirt (lilac) → loop.

**AI video prompt**
> Vertical 3:4 3D fashion visualisation, 10 seconds, seamless loop, no audio. A faceless light-wood mannequin
> avatar stands centred on a soft mint-white studio floor with a subtle perspective grid and a soft contact
> shadow. A thin glowing emerald-green scan line sweeps slowly from head to toe; as it passes, the avatar's
> outfit changes from a white cotton shirt with sage wide-leg trousers to a champagne satin blazer suit, then an
> emerald satin suit, then a sage linen maxi dress, then a lilac satin shirt and mini skirt. Fabrics
> drape realistically, with gentle idle breathing motion. Clean CLO3D / Marvelous Designer render style, soft global
> illumination, minimal UI overlay feel, premium apparel manufacturer aesthetic.

**Negative prompt:** human face, text, logos, watermark, glitches, cloth clipping, harsh shadows, dark background.
