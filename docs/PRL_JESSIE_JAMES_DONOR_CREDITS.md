# Jessie and James sprite donor credits

The Jessie and James battle portraits and walking frames were imported from the user-approved `PRL_Jessie_James_Meowth_Donor_and_ROM_Audit.zip`, folder `/Pokémon Relic Legacy/Sprite Resources/Team Rocket Jessie James/`. The selected battle fronts use the classic white uniforms. The overworld assets are the original nine-frame 16×32 GBA 4bpp walking sets with their donor RGB555 palettes; front portraits are converted to PRL's indexed GBA PNG format without changing their opaque colors.

The archive identifies the donor ROM as **Pokémon Team Rocket Jessie & James** (FireRed, BPRE), by **MrNightology**, source ROM SHA-256 `03b53a3594d7f67afe3c4b6de7127027d8ae4ac64961b59a51fe1cbd0578fe53`. The archive audit notes that individual graphical credits and reuse terms should be verified before public distribution. These are donor graphics only; no donor story, maps, code, balloon artwork, or alternative outfits are imported.

## Battle-introduction artwork

The Jessie & James and Steevee & Neevee BG0 introduction assets are preserved byte-for-byte from the approved PRL asset pack on branch `prl/approved-duo-intros-jj-finale-20261011` (pack blob `8e13a0133d2abe1687c9eb74d2cba7366ac8dc93`). PRU's importer verifies the packed payload checksum, exact output paths, byte lengths, tile bounds and palette bank before compilation.
