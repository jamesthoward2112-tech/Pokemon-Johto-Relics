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

The Ecruteak Rock Shop feature was developed on `pjr-rock-shop-ecruteak`. Once its final validation build succeeds, that branch is folded into `pjr-rebuild`, the Rock Shop PR is closed, and the dedicated Alpha workflow returns to building only `pjr-rebuild`.
