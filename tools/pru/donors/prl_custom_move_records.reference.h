// Reference-only; exact PRL moves_info.h records, NOT included in a compiled PRU build.
// Includes all 37 Step10/PRL custom source records, including some already available in PJR.
// For missing IDs: port effects/animations and integrate in src/data/moves_info.h, preserving working PJR IDs.
// Source: prl/pr108-regional-trainer-namespaces-save-architecture-20261015.

// PRL STEP10 MOVE DATA BEGIN
[MOVE_AMBER_BLADE] =
{
    .name = COMPOUND_STRING("AMBER BLADE"),
    .description = COMPOUND_STRING("PRL signature move."),
    .effect = EFFECT_HIT,
    .power = 95,
    .type = TYPE_GRASS,
    .accuracy = 100,
    .pp = 10,
    .target = TARGET_SELECTED,
    .priority = 0,
    .category = DAMAGE_CATEGORY_PHYSICAL,
    .criticalHitStage = 1,
    .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_STAT_MINUS, .defense = 1, .chance = 20, }),
    .battleAnimScript = gBattleAnimMove_LeafBlade,
},

[MOVE_SUN_RITE] =
{
    .name = COMPOUND_STRING("SUN RITE"),
    .description = COMPOUND_STRING("PRL signature move."),
    .effect = EFFECT_HIT,
    .power = 95,
    .type = TYPE_FIRE,
    .accuracy = 100,
    .pp = 10,
    .target = TARGET_SELECTED,
    .priority = 0,
    .category = DAMAGE_CATEGORY_PHYSICAL,
    .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_STAT_PLUS, .speed = 1, .self = TRUE, .chance = 30, }),
    .battleAnimScript = gBattleAnimMove_BlazeKick,
},

[MOVE_TECTONIC_TIDE] =
{
    .name = COMPOUND_STRING("TECTONIC TIDE"),
    .description = COMPOUND_STRING("PRL signature move."),
    .effect = EFFECT_HIT,
    .power = 95,
    .type = TYPE_WATER,
    .accuracy = 100,
    .pp = 10,
    .target = TARGET_SELECTED,
    .priority = 0,
    .category = DAMAGE_CATEGORY_PHYSICAL,
    .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_STAT_MINUS, .defense = 1, .chance = 30, }),
    .battleAnimScript = gBattleAnimMove_AquaTail,
},

[MOVE_EPOCH_CRASH] =
{
    .name = COMPOUND_STRING("EPOCH CRASH"),
    .description = COMPOUND_STRING("PRL signature move."),
    .effect = EFFECT_HIT,
    .power = 120,
    .type = TYPE_ROCK,
    .accuracy = 100,
    .pp = 5,
    .target = TARGET_SELECTED,
    .priority = 0,
    .category = DAMAGE_CATEGORY_PHYSICAL,
    .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_STAT_MINUS, .defense = 1, .chance = 20, }),
    .battleAnimScript = gBattleAnimMove_StoneEdge,
},

[MOVE_RELIC_WISH] =
{
    .name = COMPOUND_STRING("RELIC WISH"),
    .description = COMPOUND_STRING("PRL signature move."),
    .effect = EFFECT_HIT,
    .power = 100,
    .type = TYPE_FAIRY,
    .accuracy = 100,
    .pp = 10,
    .target = TARGET_SELECTED,
    .priority = 0,
    .category = DAMAGE_CATEGORY_SPECIAL,
    .battleAnimScript = gBattleAnimMove_Moonblast,
},

[MOVE_STAG_STAB] =
    {
        .name = COMPOUND_STRING("STAG STAB"),
        .description = COMPOUND_STRING("A brutal horn thrust that may\nmake the target flinch."),
        .effect = EFFECT_HIT,
        .power = 85,
        .type = TYPE_FIGHTING,
        .accuracy = 100,
        .pp = 10,
        .target = TARGET_SELECTED,
        .category = DAMAGE_CATEGORY_PHYSICAL,
        .makesContact = TRUE,
        .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_FLINCH, .chance = 20, }),
        .battleAnimScript = gBattleAnimMove_Megahorn,
    },

[MOVE_IRON_TEMPEST] =
    {
        .name = COMPOUND_STRING("IRON TEMPEST"),
        .description = COMPOUND_STRING("Metal wings carve the foe. It\nmay lower the target's Speed."),
        .effect = EFFECT_HIT,
        .power = 85,
        .type = TYPE_STEEL,
        .accuracy = 100,
        .pp = 10,
        .target = TARGET_SELECTED,
        .category = DAMAGE_CATEGORY_PHYSICAL,
        .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_STAT_MINUS, .speed = 1, .chance = 20, }),
        .battleAnimScript = gBattleAnimMove_SteelWing,
    },

[MOVE_TAILSPIN] =
    {
        .name = COMPOUND_STRING("TAILSPIN"),
        .description = COMPOUND_STRING("A spinning tail strike that\ngets stronger and raises Speed."),
        .effect = EFFECT_ROLLOUT,
        .power = 30,
        .type = TYPE_NORMAL,
        .accuracy = 95,
        .pp = 10,
        .target = TARGET_SELECTED,
        .category = DAMAGE_CATEGORY_PHYSICAL,
        .makesContact = TRUE,
        .instructBanned = TRUE,
        .parentalBondBanned = TRUE,
        .additionalEffects = ADDITIONAL_EFFECTS({
            .moveEffect = MOVE_EFFECT_STAT_PLUS,
            .speed = 1,
            .self = TRUE,
            .chance = 100,
        }),
        .battleAnimScript = gBattleAnimMove_Rollout,
    },

[MOVE_FORTRESS_CRUSH] =
    {
        .name = COMPOUND_STRING("FORTRESS CRUSH"),
        .description = COMPOUND_STRING(
            "Crushes with hardened armor.\n"
            "Uses the user's Defense."),
        .effect = EFFECT_BODY_PRESS,
        .power = 90,
        .type = TYPE_ROCK,
        .accuracy = 100,
        .pp = 10,
        .target = TARGET_SELECTED,
        .priority = 0,
        .category = DAMAGE_CATEGORY_PHYSICAL,
        .battleAnimScript = gBattleAnimMove_BodyPress,
    },

[MOVE_BRAIN_FREEZE] =
    {
        .name = COMPOUND_STRING("BRAIN FREEZE"),
        .description = COMPOUND_STRING(
            "Cryokinesis strikes the foe.\n"
            "It may freeze the target."),
        .effect = EFFECT_HIT,
        .power = 85,
        .type = TYPE_PSYCHIC,
        .accuracy = 100,
        .pp = 10,
        .target = TARGET_SELECTED,
        .priority = 0,
        .category = DAMAGE_CATEGORY_SPECIAL,
        .additionalEffects = ADDITIONAL_EFFECTS({
            .moveEffect = MOVE_EFFECT_FREEZE,
            .chance = 10,
        }),
        .battleAnimScript = gBattleAnimMove_Psybeam,
    },

[MOVE_ETERNAL_BLOOM] =
    {
        .name = COMPOUND_STRING("ETERNAL BLOOM"),
        .description = COMPOUND_STRING(
            "Drains life with ancient light.\n"
            "Heals half the damage dealt."),
        .effect = EFFECT_HIT,
        .power = 90,
        .type = TYPE_FAIRY,
        .accuracy = 100,
        .pp = 10,
        .target = TARGET_SELECTED,
        .priority = 0,
        .category = DAMAGE_CATEGORY_SPECIAL,
        .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_ABSORB, .argument.absorbPercentage = 50, }),
        .healingMove = B_HEAL_BLOCKING >= GEN_6,
        .battleAnimScript = gBattleAnimMove_Moonblast,
    },

[MOVE_MAGMA_RIFT] =
    {
        .name = COMPOUND_STRING("MAGMA RIFT"),
        .description = COMPOUND_STRING(
            "Rips open a burning fissure.\n"
            "It may burn the target."),
        .effect = EFFECT_HIT,
        .power = 100,
        .type = TYPE_GROUND,
        .accuracy = 100,
        .pp = 10,
        .target = TARGET_SELECTED,
        .priority = 0,
        .category = DAMAGE_CATEGORY_SPECIAL,
        .additionalEffects = ADDITIONAL_EFFECTS({
            .moveEffect = MOVE_EFFECT_BURN,
            .chance = 20,
        }),
        .battleAnimScript = gBattleAnimMove_EarthPower,
    },

[MOVE_DEATH_ROLL] =
    {
        .name = COMPOUND_STRING("DEATH ROLL"),
        .description = COMPOUND_STRING(
            "A savage rolling bite that\n"
            "may make the target flinch."),
        .effect = EFFECT_HIT,
        .power = 95,
        .type = TYPE_WATER,
        .accuracy = 100,
        .pp = 10,
        .target = TARGET_SELECTED,
        .priority = 0,
        .category = DAMAGE_CATEGORY_PHYSICAL,
        .makesContact = TRUE,
        .bitingMove = TRUE,
        .additionalEffects = ADDITIONAL_EFFECTS({
            .moveEffect = MOVE_EFFECT_FLINCH,
            .chance = 20,
        }),
        .battleAnimScript = gBattleAnimMove_AquaTail,
    },

[MOVE_PRESSURIZE] =
    {
        .name = COMPOUND_STRING("PRESSURIZE"),
        .description = COMPOUND_STRING(
            "Compresses its rocky body to\n"
            "sharply raise Sp. Def."),
        .effect = EFFECT_STAT_CHANGE,
        .power = 0,
        .type = TYPE_ROCK,
        .accuracy = 0,
        .pp = 20,
        .target = TARGET_USER,
        .priority = 0,
        .category = DAMAGE_CATEGORY_STATUS,
        .additionalEffects = ADDITIONAL_EFFECTS({
            .moveEffect = STAT_CHANGE_EFFECT_PLUS,
            .spDef = 2,
        }),
        .snatchAffected = TRUE,
        .ignoresProtect = TRUE,
        .mirrorMoveBanned = TRUE,
        .battleAnimScript = gBattleAnimMove_Amnesia,
    },

[MOVE_VENOM_SWIPE] =
    {
        .name = COMPOUND_STRING("VENOM SWIPE"),
        .description = COMPOUND_STRING(
            "Slashes the target with a\n"
            "venom-coated strike."),
        .effect = EFFECT_HIT,
        .power = 100,
        .type = TYPE_POISON,
        .accuracy = 90,
        .pp = 10,
        .target = TARGET_SELECTED,
        .priority = 0,
        .category = DAMAGE_CATEGORY_PHYSICAL,
        .makesContact = TRUE,
        .additionalEffects = ADDITIONAL_EFFECTS({
            .moveEffect = MOVE_EFFECT_POISON,
            .chance = 30,
        }),
        .battleAnimScript = gBattleAnimMove_PoisonJab,
    },

[MOVE_VANISH] =
    {
        .name = COMPOUND_STRING("VANISH"),
        .description = COMPOUND_STRING(
            "Becomes nearly invisible to\n"
            "sharply raise evasiveness."),
        .effect = EFFECT_STAT_CHANGE,
        .power = 0,
        .type = TYPE_GHOST,
        .accuracy = 0,
        .pp = 5,
        .target = TARGET_USER,
        .priority = 0,
        .category = DAMAGE_CATEGORY_STATUS,
        .additionalEffects = ADDITIONAL_EFFECTS({
            .moveEffect = STAT_CHANGE_EFFECT_PLUS,
            .evasion = 2,
        }),
        .snatchAffected = TRUE,
        .ignoresProtect = TRUE,
        .mirrorMoveBanned = TRUE,
        .battleAnimScript = gBattleAnimMove_DoubleTeam,
    },

[MOVE_KABLOW] =
    {
        .name = COMPOUND_STRING("KABLOW!"),
        .description = COMPOUND_STRING(
            "The user detonates violently,\n"
            "scattering hazardous shrapnel."),
        .effect = EFFECT_CEASELESS_EDGE,
        .power = 170,
        .type = TYPE_STEEL,
        .accuracy = 100,
        .pp = 5,
        .target = TARGET_FOES_AND_ALLY,
        .priority = 0,
        .category = DAMAGE_CATEGORY_PHYSICAL,
        .explosion = TRUE,
        .parentalBondBanned = TRUE,
        .dampBanned = TRUE,
        .battleAnimScript = gBattleAnimMove_Explosion,
    },

[MOVE_GLYPHIC_CHORUS] =
    {
        .name = COMPOUND_STRING("GLYPHIC CHORUS"),
        .description = COMPOUND_STRING("An ancient chorus clears\nweakness before striking."),
        .effect = EFFECT_HIT,
        .power = 100,
        .type = TYPE_PSYCHIC,
        .accuracy = 100,
        .pp = 5,
        .target = TARGET_SELECTED,
        .category = DAMAGE_CATEGORY_SPECIAL,
        .soundMove = TRUE,
        .battleAnimScript = gBattleAnimMove_Psychic,
    },

[MOVE_COSMIC_RAY] =
    {
        .name = COMPOUND_STRING("COSMIC RAY"),
        .description = COMPOUND_STRING(
            "A concentrated astral beam.\n"
            "It may make the foe flinch."),
        .effect = EFFECT_HIT,
        .power = 95,
        .type = TYPE_FAIRY,
        .accuracy = 100,
        .pp = 10,
        .target = TARGET_SELECTED,
        .priority = 0,
        .category = DAMAGE_CATEGORY_SPECIAL,
        .pulseMove = TRUE,
        .additionalEffects = ADDITIONAL_EFFECTS({
            .moveEffect = MOVE_EFFECT_FLINCH,
            .chance = 15,
        }),
        .battleAnimScript = gBattleAnimMove_Moonblast,
    },

[MOVE_DEJA_VU] =
    {
        .name = COMPOUND_STRING("DÉJÀ-VU"),
        .description = COMPOUND_STRING(
            "A psychic echo strikes with\n"
            "an attack that never misses."),
        .effect = EFFECT_HIT,
        .power = 105,
        .type = TYPE_PSYCHIC,
        .accuracy = 0,
        .pp = 10,
        .target = TARGET_SELECTED,
        .priority = 0,
        .category = DAMAGE_CATEGORY_SPECIAL,
        .battleAnimScript = gBattleAnimMove_FutureSight,
    },

[MOVE_PHOENIX_HYMN] =
    {
        .name = COMPOUND_STRING("PHOENIX HYMN"),
        .description = COMPOUND_STRING("A sacred flame-song that\nrestores one quarter max HP."),
        .effect = EFFECT_HIT,
        .power = 105,
        .type = TYPE_FIRE,
        .accuracy = 100,
        .pp = 5,
        .target = TARGET_SELECTED,
        .category = DAMAGE_CATEGORY_SPECIAL,
        .soundMove = TRUE,
        .battleAnimScript = gBattleAnimMove_SacredFire,
    },

[MOVE_EDEN_BLOOM] =
{
    .name = COMPOUND_STRING("Eden Bloom"),
    .description = COMPOUND_STRING("A sacred bloom strikes the\nfoe. May cause poisoning."),
    .effect = EFFECT_HIT,
    .power = 95,
    .type = TYPE_GRASS,
    .accuracy = 100,
    .pp = 10,
    .target = TARGET_SELECTED,
    .priority = 0,
    .category = DAMAGE_CATEGORY_SPECIAL,
    .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_POISON, .chance = 30, }),
    .battleAnimScript = gBattleAnimMove_EnergyBall,
},

[MOVE_SCORCHWING] =
{
    .name = COMPOUND_STRING("Scorch Wings"),
    .description = COMPOUND_STRING("Scorching wings strike the\nfoe. May cause a burn."),
    .effect = EFFECT_HIT,
    .power = 95,
    .type = TYPE_FLYING,
    .accuracy = 100,
    .pp = 10,
    .target = TARGET_SELECTED,
    .priority = 0,
    .category = DAMAGE_CATEGORY_PHYSICAL,
    .makesContact = TRUE,
    .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_BURN, .chance = 20, }),
    .battleAnimScript = gBattleAnimMove_BraveBird,
},

[MOVE_BASTION_CANNON] =
{
    .name = COMPOUND_STRING("Bastion Cannon"),
    .description = COMPOUND_STRING("A mighty steel blast that\nmay boost user's Defense."),
    .effect = EFFECT_HIT,
    .power = 95,
    .type = TYPE_STEEL,
    .accuracy = 100,
    .pp = 10,
    .target = TARGET_SELECTED,
    .priority = 0,
    .category = DAMAGE_CATEGORY_SPECIAL,
    .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_STAT_PLUS, .defense = 1, .self = TRUE, .chance = 30, }),
    .battleAnimScript = gBattleAnimMove_FlashCannon,
},

[MOVE_LOVELY_BITE] =
{
    .name = COMPOUND_STRING("Lovely Bite"),
    .description = COMPOUND_STRING("A charming bite that may infatuate the target."),
    .effect = EFFECT_HIT, .power = 85, .type = TYPE_FAIRY, .accuracy = 100,
    .pp = 15, .target = TARGET_SELECTED, .priority = 0,
    .category = DAMAGE_CATEGORY_PHYSICAL, .makesContact = TRUE, .bitingMove = TRUE,
    .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_INFATUATION, .chance = 10, },
            { .moveEffect = MOVE_EFFECT_BLEED, .chance = 10, }),
    .battleAnimScript = gBattleAnimMove_Bite,
},

[MOVE_SHADOW_FANGS] =
{
    .name = COMPOUND_STRING("Shadow Fangs"),
    .description = COMPOUND_STRING("A shadowy bite that may curse the target."),
    .effect = EFFECT_HIT, .power = 80, .type = TYPE_GHOST, .accuracy = 100,
    .pp = 15, .target = TARGET_SELECTED, .priority = 0,
    .category = DAMAGE_CATEGORY_PHYSICAL, .makesContact = TRUE, .bitingMove = TRUE,
    .additionalEffects = ADDITIONAL_EFFECTS({ .moveEffect = MOVE_EFFECT_CURSE, .chance = 10, },
            { .moveEffect = MOVE_EFFECT_BLEED, .chance = 10, }),
    .battleAnimScript = gBattleAnimMove_Bite,
},

[MOVE_RIP_AND_TEAR] =
{
    .name = COMPOUND_STRING("Rip and Tear"),
    .description = COMPOUND_STRING("Rips the target, lowering its Speed and possibly causing bleeding."),
    .effect = EFFECT_HIT, .power = 110, .type = TYPE_DARK, .accuracy = 90,
    .pp = 5, .target = TARGET_SELECTED, .priority = 0,
    .category = DAMAGE_CATEGORY_PHYSICAL, .makesContact = TRUE, .bitingMove = TRUE,
    .cantUseTwice = TRUE,
    .additionalEffects = (const struct AdditionalEffect[]) {
        {
            .moveEffect = MOVE_EFFECT_STAT_MINUS,
            .speed = 1,
            .chance = 100,
        },
        {
            .moveEffect = MOVE_EFFECT_BLEED,
            .chance = 50,
        }
    },
    .numAdditionalEffects = 2,
    .battleAnimScript = gBattleAnimMove_Crunch,
},

[MOVE_EERIE_FOG] =
{
    .name = COMPOUND_STRING("Eerie Fog"),
    .description = COMPOUND_STRING("Summons an eerie fog for eight turns."),
    .effect = EFFECT_WEATHER,
    .power = 0,
    .type = TYPE_GHOST,
    .accuracy = 0,
    .pp = 5,
    .target = TARGET_FIELD,
    .priority = 0,
    .category = DAMAGE_CATEGORY_STATUS,
    .ignoresProtect = TRUE,
    .mirrorMoveBanned = TRUE,
    .argument = { .weatherType = BATTLE_WEATHER_FOG },
    .battleAnimScript = gBattleAnimMove_Mist,
},

[MOVE_SEISMIC_SLAM] =
{
    .name = COMPOUND_STRING("Seismic Slam"),
    .description = COMPOUND_STRING("Shatters the earth.\nThe user takes recoil."),
    .effect = EFFECT_RECOIL,
    .power = 120,
    .type = TYPE_GROUND,
    .accuracy = 100,
    .pp = 10,
    .target = TARGET_SELECTED,
    .priority = 0,
    .category = DAMAGE_CATEGORY_PHYSICAL,
    .makesContact = TRUE,
    .argument = { .recoilPercentage = 33 },
    .battleAnimScript = gBattleAnimMove_DoubleEdge,
},

[MOVE_SOIL_DRAIN] =
{
    .name = COMPOUND_STRING("Soil Drain"),
    .description = COMPOUND_STRING("Drains power through soil.\nHeals half damage dealt."),
    .effect = EFFECT_HIT,
    .power = 75,
    .type = TYPE_GROUND,
    .accuracy = 100,
    .pp = 10,
    .target = TARGET_SELECTED,
    .priority = 0,
    .category = DAMAGE_CATEGORY_SPECIAL,
    .additionalEffects = ADDITIONAL_EFFECTS({
        .moveEffect = MOVE_EFFECT_ABSORB,
        .argument.absorbPercentage = 50,
    }),
    .battleAnimScript = gBattleAnimMove_GigaDrain,
},

[MOVE_BRAVADO] =
{
    .name = COMPOUND_STRING("Bravado"),
    .description = COMPOUND_STRING("Boosted if burned,\npoisoned or paralyzed."),
    .effect = EFFECT_FACADE,
    .power = 70,
    .type = TYPE_NORMAL,
    .accuracy = 100,
    .pp = 20,
    .target = TARGET_SELECTED,
    .priority = 0,
    .category = DAMAGE_CATEGORY_SPECIAL,
    .makesContact = TRUE,
    .battleAnimScript = gBattleAnimMove_Facade,
},

[MOVE_RAGING_SOULS] =
{
    .name = COMPOUND_STRING("Raging Souls"),
    .description = COMPOUND_STRING("Ghostly surge that\nsharply drops Sp. Atk."),
    .effect = EFFECT_HIT,
    .power = 130,
    .type = TYPE_GHOST,
    .accuracy = 100,
    .pp = 5,
    .target = TARGET_SELECTED,
    .priority = 0,
    .category = DAMAGE_CATEGORY_SPECIAL,
    .additionalEffects = ADDITIONAL_EFFECTS({
        .moveEffect = MOVE_EFFECT_STAT_MINUS,
        .spAtk = 2,
        .self = TRUE,
    }),
    .battleAnimScript = gBattleAnimMove_WillOWisp,
},

[MOVE_IRON_FANGS] =
{
    .name = COMPOUND_STRING("Iron Fangs"),
    .description = COMPOUND_STRING("Steel fangs smash\nthrough barriers."),
    .effect = EFFECT_HIT,
    .power = 85,
    .type = TYPE_STEEL,
    .accuracy = 100,
    .pp = 15,
    .target = TARGET_SELECTED,
    .priority = 0,
    .category = DAMAGE_CATEGORY_PHYSICAL,
    .makesContact = TRUE,
    .bitingMove = TRUE,
    .additionalEffects = ADDITIONAL_EFFECTS({
        .moveEffect = MOVE_EFFECT_BREAK_SCREEN,
        .preAttackEffect = TRUE,
    },
            { .moveEffect = MOVE_EFFECT_BLEED, .chance = 10, }),
    .battleAnimScript = gBattleAnimMove_BrickBreak,
},

[MOVE_BEATDOWN] =
{
    .name = COMPOUND_STRING("Beatdown"),
    .description = COMPOUND_STRING("A dark flurry that\nhits two to five times."),
    .effect = EFFECT_HIT,
    .power = 25,
    .type = TYPE_DARK,
    .accuracy = 100,
    .pp = 20,
    .target = TARGET_SELECTED,
    .priority = 0,
    .category = DAMAGE_CATEGORY_PHYSICAL,
    .makesContact = TRUE,
    .multiHit = TRUE,
    .battleAnimScript = gBattleAnimMove_BeatUp,
},

[MOVE_TAKE_FLIGHT] =
{
    .name = COMPOUND_STRING("Take Flight"),
    .description = COMPOUND_STRING("Strikes with wind,\nthen switches user out."),
    .effect = EFFECT_HIT_ESCAPE,
    .power = 60,
    .type = TYPE_FLYING,
    .accuracy = 100,
    .pp = 20,
    .target = TARGET_SELECTED,
    .priority = 0,
    .category = DAMAGE_CATEGORY_SPECIAL,
    .windMove = TRUE,
    .battleAnimScript = gBattleAnimMove_UTurn,
},

[MOVE_INSECT_IMPACT] =
{
    .name = COMPOUND_STRING("Insect Impact"),
    .description = COMPOUND_STRING("A hard bug punch that\nmay lower Defense."),
    .effect = EFFECT_HIT,
    .power = 80,
    .type = TYPE_BUG,
    .accuracy = 100,
    .pp = 15,
    .target = TARGET_SELECTED,
    .priority = 0,
    .category = DAMAGE_CATEGORY_PHYSICAL,
    .makesContact = TRUE,
    .punchingMove = TRUE,
    .additionalEffects = ADDITIONAL_EFFECTS({
        .moveEffect = MOVE_EFFECT_STAT_MINUS,
        .defense = 1,
        .chance = 30,
    }),
    .battleAnimScript = gBattleAnimMove_DoubleEdge,
},
// PRL STEP10 MOVE DATA END

[MOVE_EEVOBOOST] =
    {
        .name = COMPOUND_STRING("Eevoboost"),
        .description = COMPOUND_STRING(
            "Gathers inner potential\n"
            "to raise all five stats."),
        .effect = EFFECT_EXTREME_EVOBOOST,
        .power = 0,
        .type = TYPE_NORMAL,
        .accuracy = 0,
        .pp = 5,
        .target = TARGET_USER,
        .priority = -2,
        .category = DAMAGE_CATEGORY_STATUS,
        .ignoresProtect = TRUE,
        .mirrorMoveBanned = TRUE,
        .snatchAffected = TRUE,
        .additionalEffects = ADDITIONAL_EFFECTS({
            .moveEffect = STAT_CHANGE_EFFECT_PLUS,
            .attack = 1,
            .defense = 1,
            .speed = 1,
            .spAtk = 1,
            .spDef = 1,
        }),
        .battleAnimScript = gBattleAnimMove_ExtremeEvoboost,
    },
