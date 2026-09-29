# AGENTS.md — Pokémon Johto Relics

This file defines the default working rules for AI-assisted development of **Pokémon Johto Relics (PJR)**.

## Repository / branch

- Repository: `jamesthoward2112-tech/Pokemon-Johto-Relics`
- Active development branch: `pjr-rebuild`
- Do not silently switch to `master`, `1.3-shop-ui`, an old checkout, an old ROM, or an earlier rescue state.
- Always read the live `pjr-rebuild` HEAD before editing. GitHub HEAD and GitHub Actions are the source of truth, not chat/session state.

## Crash-resistant execution rule

The priority is to make useful work survive an interrupted ChatGPT/agent session.

For every implementation task:

1. Inspect only what is needed to locate the requested change.
2. Make a **small real implementation batch** as soon as practical.
3. As soon as that batch is internally coherent, **commit and push it to `pjr-rebuild` immediately**.
4. Verify the pushed commit SHA.
5. Build/check the real GitHub Actions run for that SHA.
6. If it fails, inspect the actual error, fix that error, commit/push the fix, and rebuild.
7. Repeat **FIX → COMMIT/PUSH → BUILD → INSPECT** until the requested batch is successful.
8. Do not hold a large amount of completed work only inside a chat or temporary workspace waiting for the whole job to finish.

A session crash must never require rediscovering or recreating already completed work if that work could have been committed.

## Keep passes short

- Prefer one to three closely related implementation jobs per batch.
- Do not perform a broad project audit unless the user explicitly asks for one.
- Do not repeatedly re-check completed systems merely because a new run has started.
- Preserve working features unless the current task explicitly changes them.
- When a task is large, checkpoint working subsets to GitHub before continuing.

## Asset / Library discipline

Repeated broad Library searches are a known source of wasted time and fragile sessions.

- Search for an external asset only when the repository does not already contain the required asset.
- Reuse exact asset locations discovered earlier in the same task.
- Do not repeatedly list the same Library folders with slightly different queries.
- Once an asset has been imported into the repository, treat the repository copy as canonical for future builds.
- When a reusable external asset location is discovered, record it in the repository documentation or the commit message so a later session does not have to rediscover it.
- Prefer targeted filename/folder searches over recursive exploratory searches.
- Never redo an asset search just to “double check” if the asset has already been positively identified.

## PJR project invariants

- PJR is a sequel to Project Kanto Relics and Project Hoenn Relics.
- Core PJR work must not regress already working QoL or completed fixes.
- Followers are intentionally removed.
- Starter line is Scarabub → Heracross → Heracurion, Skarmet → Skarmory → Skarmadon, and Mootiny → Miltank → Miltitan.
- Silver receives the mapped unchosen baby starter, not a vanilla Johto starter.
- Jessie and James are recurring Team Rocket agents; their late-game Pikachu must remain Pikachu because Noxichu is reserved for Red.
- Red's exclusive PKR team is Edensaur, Charaxis, Fortotoise, Khang, Nolax, and Noxichu.
- RELICS/postgame content and custom species/assets already implemented must be preserved unless the user explicitly requests a change.
- Avoid frustrating puzzle redesigns; this project intentionally favors streamlined progression.

## Build

The upstream project documentation specifies:

```sh
make hns
```

and the resulting base build ROM is `pokehns.gba`. When GitHub Actions has a project-specific build/package workflow, use that workflow as the authoritative build result and artifact source.

## Reporting a run

A status report must distinguish between:

- edits only present in the current workspace,
- committed/pushed changes,
- a GitHub Actions run that is queued or running,
- a failed build,
- a successful build,
- and an artifact that actually exists.

Never describe work as continuing in the background unless GitHub/automation state actually shows that it is running.

For implementation requests, do not stop at an audit or plan when the requested code change can be made. The normal terminal result is a pushed implementation plus a verified build/artifact, or a clearly identified external blocker.
