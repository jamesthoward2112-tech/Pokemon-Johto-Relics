# Pokémon Insurgence front-sprite donors

These are the original published Pokémon Insurgence Mega battler images used as
the source for the PJR forms below.  They are retained here so future builds do
not repeat the old mistake of shrinking the entire donor canvas.

- Miltitan <- Mega Miltank: https://wiki.p-insurgence.com/images/d/da/241_1.png
- Sudowarden <- Mega Sudowoodo: https://wiki.p-insurgence.com/images/4/42/185_1.png
- Donphalanx <- Mega Donphan: https://wiki.p-insurgence.com/images/b/b1/232_1.png
- Faeranium <- Mega Meganium: https://wiki.p-insurgence.com/images/8/8c/154_1.png
- Pyroclast <- Mega Typhlosion: https://wiki.p-insurgence.com/images/a/a2/157_1.png

Conversion rule: crop transparent padding first, reduce the published 2x render
back to its native pixel grid, uniformly fit into a 64x64 GBA front-sprite frame,
then map to the existing locked PJR 16-colour palette.  No non-uniform scaling,
redrawing, or changes to backs/icons are allowed.

Feralodon is intentionally excluded: its current locked visual is the later
Mega-Y choice, not the Insurgence Mega Feraligatr donor.  Heracurion also remains
on the existing Mega Heracross asset.
