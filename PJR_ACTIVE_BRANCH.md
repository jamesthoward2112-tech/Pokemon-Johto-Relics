# Pokémon Johto Relics — active development branch

The repository default branch is inherited from the upstream project and is **not** the active PJR game branch.

## Source of truth

- **Active/canonical PJR branch:** `pjr-rebuild`
- **Authoritative playable build:** latest successful **PJR Alpha build** GitHub Actions run on `pjr-rebuild`
- **Temporary feature branches:** merge back into `pjr-rebuild` after validation; do not treat them as independent baselines.
- Chat/session state is never authoritative for current code or build status.

Historical branches such as `pjr-alpha1-intro-cleanup`, `pjr-infinity-evolutions`, `pjr-moveset-audit`, and `pjr-moveset-merge` are retained for history only unless explicitly reactivated.

This marker exists because the upstream default branch name can otherwise make automated tooling pick the wrong codebase.
