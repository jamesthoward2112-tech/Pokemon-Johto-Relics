// Reference-only; exact PRL custom ability records, NOT included in a compiled PRU build.
// Includes reserved PRL placeholders. Preserve numeric PJR ability IDs and port all engine triggers.
// Source: prl/pr108-regional-trainer-namespaces-save-architecture-20261015.

[ABILITY_PIERCING_DRILL] =
    {
        .name = _("Piercing Drill"),
        .description = COMPOUND_STRING("Contact evades protection."),
    },

    [ABILITY_DRAGONIZE] =
    {
        .name = _("Dragonize"),
        .description = COMPOUND_STRING("Normal moves turn Dragon."),
    },

    [ABILITY_EELEVATE] =
    {
        .name = _("Eelevate"),
        .description = COMPOUND_STRING("Levitate and Beast Boost."),
    },

    [ABILITY_314] =
    {
        .name = _("-------"),
        .description = COMPOUND_STRING("No special ability."),
    },

    [ABILITY_MEGA_SOL] =
    {
        .name = _("Mega Sol"),
        .description = COMPOUND_STRING("Acts like under sun."),
    },

    [ABILITY_FIRE_MANE] =
    {
        .name = _("Fire Mane"),
        .description = COMPOUND_STRING("Ups Fire-type moves."),
    },

    [ABILITY_317] =
    {
        .name = _("-------"),
        .description = COMPOUND_STRING("No special ability."),
    },

    [ABILITY_SPICY_SPRAY] =
    {
        .name = _("Spicy Spray"),
        .description = COMPOUND_STRING("Burns the foe when damaged."),
    },

    [ABILITY_AURA_GUARD] =
    {
        .name = _("Aura Guard"),
        .description = COMPOUND_STRING("Unimplemented."),
    },

// PRL STEP10 ABILITY DATA BEGIN
[ABILITY_ANCIENT_GROVE] =
{
    .name = _("Ancient Grove"),
    .description = COMPOUND_STRING("On entry, 5-turn Ancient Grove effect; Sceptitan Defense +50% during it; no passive healing"),
    .aiRating = 3,
},

[ABILITY_SOLAR_DISCIPLINE] =
{
    .name = _("Solar Discipline"),
    .description = COMPOUND_STRING("On entry, 5 turns; Fire/Psychic moves +20%; Attack and Sp. Atk cannot be lowered; no weather"),
    .aiRating = 3,
},

[ABILITY_TIDAL_BASTION] =
{
    .name = _("Tidal Bastion"),
    .description = COMPOUND_STRING("On entry, 5 turns; super-effective damage against Swamplith reduced by 25%"),
    .aiRating = 3,
},

[ABILITY_ANCIENT_CORE] =
{
    .name = _("Ancient Core"),
    .description = COMPOUND_STRING("Super-effective damage -25%; Water/Rock moves +20%; Atk/SpA cannot be lowered; after receiving "),
    .aiRating = 3,
},

[ABILITY_WISHMAKER] =
{
    .name = _("Wishmaker"),
    .description = COMPOUND_STRING("On entry create 5-turn Wishlight; Psychic/Fairy +20%; heal 1/16 max HP each turn; opponent cann"),
    .aiRating = 3,
},

[ABILITY_ANCIENT_BASTION] =
    {
        .name = _("ANCIENT BASTION"),
        .description = COMPOUND_STRING("Physical hits scatter stones\nup to three times."),
        .aiRating = 9,
    },

[ABILITY_ANCIENT_BLOOM] =
    {
        .name = _("ANCIENT BLOOM"),
        .description = COMPOUND_STRING("Heals and grows Grassy Terrain."),
        .aiRating = 8,
    },

[ABILITY_CINDER_VEIL] =
    {
        .name = _("CINDER VEIL"),
        .description = COMPOUND_STRING("Softens first hit; burns contact."),
        .aiRating = 8,
    },

[ABILITY_TIDAL_ROAR] =
    {
        .name = _("TIDAL ROAR"),
        .description = COMPOUND_STRING("Lowers foes' Atk and Sp. Atk."),
        .aiRating = 8,
    },

[ABILITY_EDENS_CANOPY] =
{
    .name = _("Eden's Canopy"),
    .description = COMPOUND_STRING("Summons Grassy Terrain;\nblocks status in it."),
    .aiRating = 3,
},

[ABILITY_THERMAL_WINGS] =
{
    .name = _("Thermal Wings"),
    .description = COMPOUND_STRING("Boosts Fire/Flying moves\nby 20%; reduces recoil."),
    .aiRating = 3,
},

[ABILITY_CITADEL_SHELL] =
{
    .name = _("Citadel Shell"),
    .description = COMPOUND_STRING("Cuts super-effective hits\nby 20%; blocks Def drops."),
    .aiRating = 3,
},

[ABILITY_STYGIAN_RUSH] =
{
    .name = _("Stygian Rush"),
    .description = COMPOUND_STRING("Dark-type moves gain priority at full HP."),
    .aiRating = 7,
},
// PRL STEP10 ABILITY DATA END
