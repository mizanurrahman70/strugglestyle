// Outfit builder catalogue: add a garment or fabric here and the builder picks it up.
//
// Each outfit is one image. `outfit` is its path, with:
//   {first}  = the selected full piece or top id, or "none"
//   {second} = the selected bottom id, or "none"
//   {fabric} = the selected fabric id
// e.g. outfits/tee-skirt-denim.webp, outfits/dress-none-silk.webp, outfits/none-pants-jersey.webp.
// The avatar always wears something, so there is no none-none image.
//
// The outfit images are built from outfits/garments/ (the avatar in each white garment) and
// outfits/fabrics/ (swatches) by outfits/compose_outfits.py; re-run it after adding a garment or fabric.
// Garment types: "full" (worn alone), "top", "bottom".
// `crop: [x%, y%, scale]` zooms a garment's tile onto the part of the full-body render it covers.
//
// Hangtag specs — SAMPLE values, to be confirmed by Struggle Style before launch:
//   garment `code` + fabric `code` make the style code (e.g. SS-TSSK-DN),
//   `moq` (pieces per colour) and `lead` (bulk days [min, max]) — the tag shows the strictest of the look.
window.OUTFIT_CONFIG = {
  outfit: 'outfits/{first}-{second}-{fabric}.webp',
  quoteUrl: 'quote.html',
  sampleDays: [7, 10],
  tagNote: 'Sample specs · to be confirmed',
  defaultFabric: 'denim',
  initial: {top: 'tee', bottom: 'skirt'},
  garments: [
    {id: 'dress',  label: 'Dress',   type: 'full',   code: 'DR', moq: 300, lead: [45, 60], thumb: 'outfits/garments/dress.webp',  crop: [-35, -23.8, 1.7]},
    {id: 'shirt',  label: 'Shirt',   type: 'top',    code: 'SH', moq: 300, lead: [40, 55], thumb: 'outfits/garments/shirt.webp',  crop: [-60, -31.2, 2.2]},
    {id: 'blazer', label: 'Blazer',  type: 'top',    code: 'BZ', moq: 200, lead: [55, 70], thumb: 'outfits/garments/blazer.webp', crop: [-65, -32.5, 2.3]},
    {id: 'pants',  label: 'Pants',   type: 'bottom', code: 'PT', moq: 300, lead: [45, 60], thumb: 'outfits/garments/pants.webp',  crop: [-32.5, -59.8, 1.65]},
    {id: 'skirt',  label: 'Skirt',   type: 'bottom', code: 'SK', moq: 300, lead: [40, 55], thumb: 'outfits/garments/skirt.webp',  crop: [-120, -124.8, 3.4]},
    {id: 'tee',    label: 'T-shirt', type: 'top',    code: 'TS', moq: 500, lead: [30, 45], thumb: 'outfits/garments/tee.webp',    crop: [-125, -57.5, 3.5]}
  ],
  // `color` fills the tile when its swatch image is missing
  fabrics: [
    {id: 'denim',  label: 'Denim',  code: 'DN', gsm: '340 GSM', comp: '98% cotton, 2% elastane',   color: '#3D4E77', thumb: 'outfits/fabrics/denim.webp'},
    {id: 'jersey', label: 'Jersey', code: 'JR', gsm: '160 GSM', comp: '100% organic cotton',       color: '#C7ACAD', thumb: 'outfits/fabrics/jersey.webp'},
    {id: 'silk',   label: 'Satin',  code: 'ST', gsm: '95 GSM',  comp: '100% recycled polyester',   color: '#533F41', thumb: 'outfits/fabrics/silk.webp'}
  ]
};
