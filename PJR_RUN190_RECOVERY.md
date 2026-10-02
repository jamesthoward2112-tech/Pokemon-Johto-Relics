# PJR Run190 recovery baseline

Recovery source: Run182 / commit cb4518d2acb46f16ef831131d0823e648b8ba0d7.

Run189 is rejected for gameplay regression. This recovery restores the full Run182 tree, then adds only the selective first-clear Elite Four visual pass and the save-compatible Relic / Resonance dialogue pass.

Run182's custom source sprites and battle mechanics are preserved. Tailspin remains the Run182 implementation: Rollout-style 30→60→120→180→240 progression, Defense Curl synergy, and +1 Speed.

Relic Ho-Oh remains SPECIES_RELIC_HO_OH at 1609. Trainer-only E4 visual forms are appended after it.

The world-spanning RELICS encounter relocation remains deferred for the fresh-save structural pass.
