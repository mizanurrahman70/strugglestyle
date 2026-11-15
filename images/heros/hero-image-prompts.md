# Hero slider — image prompts

Prompts for generating the five hero slider images on the home page (`index.html`).
Paste each prompt into an AI image tool (ChatGPT, Gemini, Midjourney, etc.).

## Rules for every image

The headline and paragraph sit **in the centre** of each slide in white text, so every image must:

- Be **landscape 16:9**, at least **2560 × 1440 px** (HD, sharp, not blurry).
- Keep the **centre calm and slightly darker**: put the main subject toward the sides or lower part, and avoid bright white areas in the middle.
- Look like a **real photo** (no illustration, no text, no logos, no watermarks).
- Use **natural, neutral colours** so all five slides look like one set.
- Show clearly that this is a **garment manufacturer** (clothing, fabric, factory, shipping).

Add this line to the end of every prompt:

```
Photorealistic, high resolution, 16:9 landscape, sharp focus, natural soft light,
neutral colours, calm and slightly darker centre area for white headline text,
no text, no logos, no watermark.
```

---

## 1. Finished garments — "Finished garments made to your specification"

**File:** `images/heros/finished-garments.jpg`

One image made from **four garment categories**: denim, sweaters, woven shirts and knits.

```
A single wide photo of a premium garment showroom table seen from slightly above,
divided into four neat groups of finished clothing: folded indigo denim jeans on the
left, stacked knitted sweaters in oatmeal and grey, crisp white and light blue cotton
poplin shirts, and soft cotton knit t-shirts on the right. Neatly folded with hang
tags, on a light wooden table, garments placed toward the edges and bottom so the
middle of the frame stays quiet.
```

**Option B: 2×2 collage.** If the tool can't fit all four in one scene, generate four
square photos (denim, sweater, poplin shirt, knit tee) with the same light and
background, then place them in a 2×2 grid (2560 × 1440).

---

## 2. Raw materials — "Responsible raw materials from the field"

**File:** `images/heros/cotton-spinning.png`. **Done:** your reference image is already used here.

Prompt, in case you want a new version:

```
Inside a clean, bright cotton spinning mill. A worker's hands on the left pull soft
raw white cotton fibre from a pile and feed it into a spinning machine; the cotton
turns into yarn on rows of white yarn cones on the right. Large windows in the
background, white and soft grey tones, shallow depth of field.
```

---

## 3. Production — "Skilled hands on a fair floor"

**File:** `images/heros/production.jpg`

```
A modern, well-lit garment factory floor. Rows of sewing machine operators in clean
uniforms stitching cotton garments, one operator in the foreground on the left
carefully sewing a shirt collar. Organised workstations, daylight from large windows,
calm and respectful atmosphere, people shown at work, not posing.
```

---

## 4. Energy — "Working toward cleaner energy and efficiency"

**File:** `images/heros/clean-energy.jpg`

The image must show **both energy and the garment factory**, not just solar panels.

```
Wide aerial view of a modern textile and garment factory building with its whole roof
covered in solar panels, a few trees and green space around it, clear blue sky with
light clouds at golden hour. The factory sits in the lower part of the frame and the
sky fills the top and centre.
```

Alternative (indoor):

```
Inside a modern garment factory with energy-efficient LED lighting and new
energy-saving sewing machines; through large windows, rows of solar panels are
visible on the neighbouring roof. Bright, clean and orderly.
```

---

## 5. Shipping — "Shipped to brands around the world"

**File:** `images/heros/cargo-ship.avif`. **Done:** already used here.

Prompt, in case you want a new version:

```
A large container cargo ship loaded with colourful shipping containers sailing out of
a busy port at sunrise, with cranes at the port on one side. Ship placed in the
lower third, wide calm sky above.
```

---

## After generating

1. Save each image in `images/heros/` with the file name shown above.
2. Keep each file under about **500 KB**: save as `.jpg` at 80% quality or convert to
   `.webp` / `.avif` (for example with https://squoosh.app).
3. Tell Claude the file names to update the slides in `index.html`.
