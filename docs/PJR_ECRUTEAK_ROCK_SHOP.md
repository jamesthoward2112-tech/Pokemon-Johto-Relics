# Ecruteak Rock Shop

Feature branch: `pjr-rock-shop-ecruteak`

## Purpose
Create a dedicated Rock Shop in Ecruteak City, inspired by the Rock Shop presentation in Azul Agua / Water Blue Beta 1.4 ML.

## Integration
- Reuses Ecruteak's existing spare doorway warp at (39,46), which previously led to TEST_MAP1.
- Adds a dedicated indoor map and layout.
- Initial layout is a known-good Poké Mart-derived scaffold so map registration, collision, warp and scripts can be compiled/tested before graphical replacement.
- Basic stock: Fire, Water, Thunder, Leaf, Ice, Moon and Sun Stones.
- After the Fog Badge: Shiny, Dusk and Dawn Stones are added.

## Azul Agua donor pass
The visual pass must use the retained Azul Agua donor asset bank (raw/compressed 4bpp tilesets, palettes, manifests and preview sheets). Reconstruct compatible PJR metatiles/palettes rather than copying opaque map scripts or economy logic.

Source/provenance: Azul Agua / Water Blue Beta 1.4 ML, by gameboy_cl. Keep donor credit in final release documentation if graphics are imported.
