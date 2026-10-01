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
- Source of truth: retained **Azul Agua / Water Blue Beta 1.4 ML** ROM.
- Uses the donor Pewter/Brock map geometry (13×17), including the real main exit at (6,15).
- Uses palette banks extracted directly from the donor ROM for both the indoor-building and Pewter/Brock sets.
- PJR's FireRed-compatible building/Pewter tile and metatile structures are deliberately wrapped into the HnS build so the donor map block indices stay valid.
- Clerk position uses Brock's donor-map coordinate (6,3); the collector uses a donor trainer coordinate (3,8).

### Donor ROM trace
- Map-bank table: ~0xA0BD04
- Indoor Pewter bank: group 6
- Pewter Gym map header: 0xA0A47C
- Layout: 0x98EAA8
- Blockdata: 0x98E8EC
- Border: 0x98E8E4
- Primary building tiles: 0x89DAC8; palettes: 0x89FE50
- Secondary Pewter/Brock tiles: 0x8AF388; palettes: 0x8B06D8

Source/provenance: Azul Agua / Water Blue Beta 1.4 ML by gameboy_cl. Keep donor credit in final release documentation.

### Exact donor tile graphics
The HnS wrapper now compiles the exact indexed 16-colour tile PNGs extracted from Azul Agua rather than the repository's vanilla FireRed tile PNGs. FireRed metatile structures are retained only for index/behaviour compatibility.
