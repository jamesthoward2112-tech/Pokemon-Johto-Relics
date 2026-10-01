# PJR Branch Policy

## Canonical development branch

**`pjr-rebuild` is the single source of truth for the active Pokémon Johto Relics Alpha.**

Use GitHub HEAD on `pjr-rebuild` plus the latest successful **PJR Alpha build** workflow as the authoritative state. Chat/session state is never authoritative.

## Feature branches

Feature branches such as `pjr-rock-shop-ecruteak`, `pjr-alpha1-intro-cleanup`, `pjr-infinity-evolutions`, `pjr-moveset-audit`, and `pjr-moveset-merge` are historical or temporary work branches. Do not treat them as current unless they are explicitly being merged into `pjr-rebuild`.

After a feature is validated, fast-forward or merge it into `pjr-rebuild`, close its PR, and continue from `pjr-rebuild`.

## Build authority

The dedicated workflow `.github/workflows/pjr-rebuild.yml` builds the real HnS/PJR Alpha and packages:

- `PJR-Alpha.gba`
- `PJR-Alpha.sym`
- `PJR-Alpha-SHA256.txt`
- `PJR-Alpha-Commit.txt`

A feature is not considered test-ready until this workflow succeeds on the canonical branch.

## 2026-10-01 housekeeping

The Ecruteak Rock Shop feature was validated by **PJR Alpha build Run 143** at commit `85393e8f` and folded into `pjr-rebuild`.

`pjr-rock-shop-ecruteak` is now historical only. New PJR feature work should branch from `pjr-rebuild` and open a PR back to `pjr-rebuild`. The PJR Alpha workflow runs on both those PRs and pushes to the canonical branch.

The generic Emerald/FireRed/LeafGreen CI is intentionally restricted to `master` and `upcoming`; it is not the authority for the HnS/PJR build.

Exact Azul Agua donor tile sources used by the Ecruteak Rock Shop are stored under `assets/pjr_azul_agua/` and are hash-checked before every PJR Alpha build:
- building tiles SHA-256: `19d1988dc7426e0be5957918de876e7a500ae327cc99bf53ef55d172d6a0f240`
- rock-shop tiles SHA-256: `5dac0833356b45617e3321e3686a15460a4f88d3f631cd1697071802f21bcc6a`
