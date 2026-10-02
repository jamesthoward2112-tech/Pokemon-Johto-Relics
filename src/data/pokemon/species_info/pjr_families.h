// Pokémon Johto Relics custom species.
// Rebuild stage 2: all three baby starters. No overworld follower data by design.

[SPECIES_SCARABUB] =
{
    .baseHP        = 45,
    .baseAttack    = 55,
    .baseDefense   = 45,
    .baseSpeed     = 50,
    .baseSpAttack  = 30,
    .baseSpDefense = 40,
    .types = MON_TYPES(TYPE_BUG),
    .catchRate = 45,
    .expYield = 65,
    .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 5,
    .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_MEDIUM_FAST,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_BUG),
    .abilities = { ABILITY_SWARM, ABILITY_GUTS, ABILITY_BATTLE_ARMOR },
    .bodyColor = BODY_COLOR_BLUE,
    .speciesName = _("SCARABUB"),
    .cryId = CRY_HERACROSS,
    .natDexNum = NATIONAL_DEX_HERACROSS,
    .categoryName = _("Scarab"),
    .height = 6,
    .weight = 120,
    .description = COMPOUND_STRING(
        "A young scarab POKéMON whose horn\n"
        "hardens as its strength grows. It\n"
        "never gives up when challenged."),
    .pokemonScale = 256,
    .pokemonOffset = 0,
    .trainerScale = 256,
    .trainerOffset = 0,
    .frontPic = gMonFrontPic_Scarabub,
    .frontPicSize = MON_COORDS_SIZE(64, 64),
    .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder,
    .frontAnimId = ANIM_V_SQUISH_AND_BOUNCE,
    .backPic = gMonBackPic_Scarabub,
    .backPicSize = MON_COORDS_SIZE(64, 64),
    .backPicYOffset = 8,
    .backAnimId = BACK_ANIM_JOLT_RIGHT,
    .palette = gMonPalette_Scarabub,
    .shinyPalette = gMonShinyPalette_Scarabub,
    .iconSprite = gMonIcon_Scarabub,
    .iconPalIndex = 3,
    .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sScarabubLevelUpLearnset,
    .teachableLearnset = sHeracrossTeachableLearnset,
    .evolutions = EVOLUTION({EVO_LEVEL, 18, SPECIES_HERACROSS}),
},

/*
 * IDs 1574 and 1576 are deliberately reserved for the locked Relic
 * evolutions Heracurion and Skarmadon. Keep them non-randomizable until
 * their full species data is installed in a later rebuild stage.
 */
[SPECIES_HERACURION] =
{
    .baseHP = 95, .baseAttack = 140, .baseDefense = 110,
    .baseSpeed = 75, .baseSpAttack = 45, .baseSpDefense = 85,
    .types = MON_TYPES(TYPE_BUG, TYPE_FIGHTING),
    .catchRate = 45, .expYield = 220, .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 25, .friendship = STANDARD_FRIENDSHIP, .growthRate = GROWTH_SLOW,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_BUG),
    .abilities = { ABILITY_MOXIE, ABILITY_GUTS, ABILITY_BATTLE_ARMOR }, .bodyColor = BODY_COLOR_BLUE,
    .speciesName = _("HERACURION"),
    .cryId = CRY_HERACROSS,
    .natDexNum = NATIONAL_DEX_HERACROSS,
    .categoryName = _("Relic Horn"), .height = 18, .weight = 625,
    .description = COMPOUND_STRING("Its ancient horn can pierce stone.\nIt stands firm while protecting\nweaker Pokémon."),
    .pokemonScale = 256, .trainerScale = 256,
    .frontPic = gMonFrontPic_Heracurion, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 3,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder,
    .frontAnimId = ANIM_V_SQUISH_AND_BOUNCE,
    .backPic = gMonBackPic_Heracurion, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 6,
    .backAnimId = BACK_ANIM_V_SHAKE_LOW,
    .palette = gMonPalette_Heracurion, .shinyPalette = gMonShinyPalette_Heracurion,
    .iconSprite = gMonIcon_Heracurion, .iconPalIndex = 3,
    .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sHeracurionLevelUpLearnset, .teachableLearnset = sHeracrossTeachableLearnset,
},

[SPECIES_SKARMET] =
{
    .baseHP        = 45,
    .baseAttack    = 45,
    .baseDefense   = 65,
    .baseSpeed     = 50,
    .baseSpAttack  = 30,
    .baseSpDefense = 35,
    .types = MON_TYPES(TYPE_STEEL, TYPE_FLYING),
    .catchRate = 45,
    .expYield = 65,
    .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 5,
    .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_SLOW,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_FLYING),
    .abilities = { ABILITY_KEEN_EYE, ABILITY_STURDY, ABILITY_WEAK_ARMOR },
    .bodyColor = BODY_COLOR_GRAY,
    .speciesName = _("SKARMET"),
    .cryId = CRY_SKARMORY,
    .natDexNum = NATIONAL_DEX_SKARMORY,
    .categoryName = _("Armor Chick"),
    .height = 5,
    .weight = 180,
    .description = COMPOUND_STRING(
        "Its light metal feathers harden as it\n"
        "grows. It practices short flights while\n"
        "testing its sharp wings on stone."),
    .pokemonScale = 256,
    .pokemonOffset = 0,
    .trainerScale = 256,
    .trainerOffset = 0,
    .frontPic = gMonFrontPic_Skarmet,
    .frontPicSize = MON_COORDS_SIZE(64, 64),
    .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder,
    .frontAnimId = ANIM_V_STRETCH,
    .backPic = gMonBackPic_Skarmet,
    .backPicSize = MON_COORDS_SIZE(64, 64),
    .backPicYOffset = 8,
    .backAnimId = BACK_ANIM_JOLT_RIGHT,
    .palette = gMonPalette_Skarmet,
    .shinyPalette = gMonShinyPalette_Skarmet,
    .iconSprite = gMonIcon_Skarmet,
    .iconPalIndex = 3,
    .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sSkarmetLevelUpLearnset,
    .teachableLearnset = sSkarmoryTeachableLearnset,
    .evolutions = EVOLUTION({EVO_LEVEL, 18, SPECIES_SKARMORY}),
},

[SPECIES_SKARMADON] =
{
    .baseHP = 80, .baseAttack = 125, .baseDefense = 140,
    .baseSpeed = 85, .baseSpAttack = 45, .baseSpDefense = 80,
    .types = MON_TYPES(TYPE_STEEL, TYPE_FLYING),
    .catchRate = 45, .expYield = 220, .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 25, .friendship = STANDARD_FRIENDSHIP, .growthRate = GROWTH_SLOW,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_FLYING),
    .abilities = { ABILITY_STURDY, ABILITY_KEEN_EYE, ABILITY_BATTLE_ARMOR }, .bodyColor = BODY_COLOR_GRAY,
    .speciesName = _("SKARMADON"),
    .cryId = CRY_SKARMORY,
    .natDexNum = NATIONAL_DEX_SKARMORY,
    .categoryName = _("Relic Armor"), .height = 20, .weight = 610,
    .description = COMPOUND_STRING("Its relic-plated wings ring like\nforged steel. It rides violent winds\nwithout yielding."),
    .pokemonScale = 256, .trainerScale = 256,
    .frontPic = gMonFrontPic_Skarmadon, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 2,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder,
    .frontAnimId = ANIM_V_STRETCH,
    .backPic = gMonBackPic_Skarmadon, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 6,
    .backAnimId = BACK_ANIM_H_SHAKE,
    .palette = gMonPalette_Skarmadon, .shinyPalette = gMonShinyPalette_Skarmadon,
    .iconSprite = gMonIcon_Skarmadon,
    .iconPalIndex = 2,
    .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sSkarmadonLevelUpLearnset, .teachableLearnset = sSkarmoryTeachableLearnset,
},

[SPECIES_MOOTINY] =
{
    .baseHP        = 50,
    .baseAttack    = 45,
    .baseDefense   = 55,
    .baseSpeed     = 45,
    .baseSpAttack  = 30,
    .baseSpDefense = 45,
    .types = MON_TYPES(TYPE_NORMAL),
    .catchRate = 45,
    .expYield = 65,
    .genderRatio = MON_FEMALE,
    .eggCycles = 5,
    .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_SLOW,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_FIELD),
    .abilities = { ABILITY_THICK_FAT, ABILITY_SCRAPPY, ABILITY_SAP_SIPPER },
    .bodyColor = BODY_COLOR_PINK,
    .speciesName = _("MOOTINY"),
    .cryId = CRY_MILTANK,
    .natDexNum = NATIONAL_DEX_MILTANK,
    .categoryName = _("Calf"),
    .height = 5,
    .weight = 280,
    .description = COMPOUND_STRING(
        "This cheerful calf builds strong legs by\n"
        "running in circles. It is surprisingly\n"
        "stubborn when protecting its friends."),
    .pokemonScale = 256,
    .pokemonOffset = 0,
    .trainerScale = 256,
    .trainerOffset = 0,
    .frontPic = gMonFrontPic_Mootiny,
    .frontPicSize = MON_COORDS_SIZE(64, 64),
    .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder,
    .frontAnimId = ANIM_V_SQUISH_AND_BOUNCE_SLOW,
    .backPic = gMonBackPic_Mootiny,
    .backPicSize = MON_COORDS_SIZE(64, 64),
    .backPicYOffset = 8,
    .backAnimId = BACK_ANIM_H_SLIDE,
    .palette = gMonPalette_Mootiny,
    .shinyPalette = gMonShinyPalette_Mootiny,
    .iconSprite = gMonIcon_Mootiny,
    .iconPalIndex = 2,
    .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sMootinyLevelUpLearnset,
    .teachableLearnset = sMiltankTeachableLearnset,
    .evolutions = EVOLUTION({EVO_LEVEL, 18, SPECIES_MILTANK}),
},

// Pokémon Infinity donor additions approved for PJR.

[SPECIES_CHAMPEON] =
{
    .baseHP = 65, .baseAttack = 110, .baseDefense = 65,
    .baseSpeed = 130, .baseSpAttack = 95, .baseSpDefense = 60,
    .types = MON_TYPES(TYPE_FIGHTING),
    .catchRate = 45, .expYield = 184,
    .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 20, .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_MEDIUM_FAST,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_FIELD),
    .abilities = { ABILITY_SCRAPPY, ABILITY_NONE, ABILITY_COMPETITIVE }, .bodyColor = BODY_COLOR_RED,
    .speciesName = _("CHAMPEON"), .cryId = CRY_EEVEE, .natDexNum = NATIONAL_DEX_EEVEE,
    .categoryName = _("Champion"), .height = 10, .weight = 230,
    .description = COMPOUND_STRING("A rare evolution awakened by unusual\n" "conditions in JOHTO. Its altered form\n" "draws out a new kind of strength."),
    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 256, .trainerOffset = 0,
    .frontPic = gMonFrontPic_Champeon, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_STRETCH,
    .backPic = gMonBackPic_Champeon, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 0, .backAnimId = BACK_ANIM_NONE,
    .palette = gMonPalette_Champeon, .shinyPalette = gMonPalette_Champeon,
    .iconSprite = gMonIcon_Champeon, .iconPalIndex = 3, .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sChampeonLevelUpLearnset, .teachableLearnset = sChampeonInfinityTeachableLearnset,
},

[SPECIES_LEPIDEON] =
{
    .baseHP = 80, .baseAttack = 65, .baseDefense = 72,
    .baseSpeed = 103, .baseSpAttack = 115, .baseSpDefense = 90,
    .types = MON_TYPES(TYPE_BUG),
    .catchRate = 45, .expYield = 184,
    .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 20, .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_MEDIUM_FAST,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_FIELD),
    .abilities = { ABILITY_RATTLED, ABILITY_NONE, ABILITY_TINTED_LENS }, .bodyColor = BODY_COLOR_YELLOW,
    .speciesName = _("LEPIDEON"), .cryId = CRY_EEVEE, .natDexNum = NATIONAL_DEX_EEVEE,
    .categoryName = _("Moth"), .height = 14, .weight = 220,
    .description = COMPOUND_STRING("A rare evolution awakened by unusual\n" "conditions in JOHTO. Its altered form\n" "draws out a new kind of strength."),
    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 256, .trainerOffset = 0,
    .frontPic = gMonFrontPic_Lepideon, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_STRETCH,
    .backPic = gMonBackPic_Lepideon, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 0, .backAnimId = BACK_ANIM_NONE,
    .palette = gMonPalette_Lepideon, .shinyPalette = gMonPalette_Lepideon,
    .iconSprite = gMonIcon_Lepideon, .iconPalIndex = 2, .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sLepideonLevelUpLearnset, .teachableLearnset = sLepideonInfinityTeachableLearnset,
},

[SPECIES_GUARDEON] =
{
    .baseHP = 65, .baseAttack = 60, .baseDefense = 130,
    .baseSpeed = 65, .baseSpAttack = 110, .baseSpDefense = 95,
    .types = MON_TYPES(TYPE_STEEL),
    .catchRate = 45, .expYield = 184,
    .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 20, .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_MEDIUM_FAST,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_FIELD),
    .abilities = { ABILITY_BULLETPROOF, ABILITY_NONE, ABILITY_HEATPROOF }, .bodyColor = BODY_COLOR_GRAY,
    .speciesName = _("GUARDEON"), .cryId = CRY_EEVEE, .natDexNum = NATIONAL_DEX_EEVEE,
    .categoryName = _("Knight"), .height = 12, .weight = 585,
    .description = COMPOUND_STRING("A rare evolution awakened by unusual\n" "conditions in JOHTO. Its altered form\n" "draws out a new kind of strength."),
    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 256, .trainerOffset = 0,
    .frontPic = gMonFrontPic_Guardeon, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_STRETCH,
    .backPic = gMonBackPic_Guardeon, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 0, .backAnimId = BACK_ANIM_NONE,
    .palette = gMonPalette_Guardeon, .shinyPalette = gMonPalette_Guardeon,
    .iconSprite = gMonIcon_Guardeon, .iconPalIndex = 3, .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sGuardeonLevelUpLearnset, .teachableLearnset = sGuardeonInfinityTeachableLearnset,
},

[SPECIES_OBSIDEON] =
{
    .baseHP = 75, .baseAttack = 120, .baseDefense = 75,
    .baseSpeed = 80, .baseSpAttack = 60, .baseSpDefense = 115,
    .types = MON_TYPES(TYPE_ROCK),
    .catchRate = 45, .expYield = 184,
    .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 20, .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_MEDIUM_FAST,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_FIELD),
    .abilities = { ABILITY_ROCK_HEAD, ABILITY_NONE, ABILITY_SAND_RUSH }, .bodyColor = BODY_COLOR_BLACK,
    .speciesName = _("OBSIDEON"), .cryId = CRY_EEVEE, .natDexNum = NATIONAL_DEX_EEVEE,
    .categoryName = _("Obsidian"), .height = 13, .weight = 330,
    .description = COMPOUND_STRING("A rare evolution awakened by unusual\n" "conditions in JOHTO. Its altered form\n" "draws out a new kind of strength."),
    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 256, .trainerOffset = 0,
    .frontPic = gMonFrontPic_Obsideon, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_STRETCH,
    .backPic = gMonBackPic_Obsideon, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 0, .backAnimId = BACK_ANIM_NONE,
    .palette = gMonPalette_Obsideon, .shinyPalette = gMonPalette_Obsideon,
    .iconSprite = gMonIcon_Obsideon, .iconPalIndex = 3, .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sObsideonLevelUpLearnset, .teachableLearnset = sObsideonInfinityTeachableLearnset,
},

[SPECIES_TOXEON] =
{
    .baseHP = 65, .baseAttack = 111, .baseDefense = 105,
    .baseSpeed = 110, .baseSpAttack = 84, .baseSpDefense = 50,
    .types = MON_TYPES(TYPE_POISON),
    .catchRate = 45, .expYield = 184,
    .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 20, .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_MEDIUM_FAST,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_FIELD),
    .abilities = { ABILITY_POISON_TOUCH, ABILITY_NONE, ABILITY_LIGHTNING_ROD }, .bodyColor = BODY_COLOR_PURPLE,
    .speciesName = _("TOXEON"), .cryId = CRY_EEVEE, .natDexNum = NATIONAL_DEX_EEVEE,
    .categoryName = _("Chimera"), .height = 11, .weight = 230,
    .description = COMPOUND_STRING("A rare evolution awakened by unusual\n" "conditions in JOHTO. Its altered form\n" "draws out a new kind of strength."),
    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 256, .trainerOffset = 0,
    .frontPic = gMonFrontPic_Toxeon, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_STRETCH,
    .backPic = gMonBackPic_Toxeon, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 0, .backAnimId = BACK_ANIM_NONE,
    .palette = gMonPalette_Toxeon, .shinyPalette = gMonPalette_Toxeon,
    .iconSprite = gMonIcon_Toxeon, .iconPalIndex = 2, .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sToxeonLevelUpLearnset, .teachableLearnset = sToxeonInfinityTeachableLearnset,
},

[SPECIES_SPHYNXEON] =
{
    .baseHP = 120, .baseAttack = 88, .baseDefense = 106,
    .baseSpeed = 61, .baseSpAttack = 70, .baseSpDefense = 80,
    .types = MON_TYPES(TYPE_GROUND),
    .catchRate = 45, .expYield = 184,
    .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 20, .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_MEDIUM_FAST,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_FIELD),
    .abilities = { ABILITY_SYNCHRONIZE, ABILITY_NONE, ABILITY_TECHNICIAN }, .bodyColor = BODY_COLOR_BROWN,
    .speciesName = _("SPHYNXEON"), .cryId = CRY_EEVEE, .natDexNum = NATIONAL_DEX_EEVEE,
    .categoryName = _("Desert"), .height = 9, .weight = 240,
    .description = COMPOUND_STRING("A rare evolution awakened by unusual\n" "conditions in JOHTO. Its altered form\n" "draws out a new kind of strength."),
    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 256, .trainerOffset = 0,
    .frontPic = gMonFrontPic_Sphynxeon, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_STRETCH,
    .backPic = gMonBackPic_Sphynxeon, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 0, .backAnimId = BACK_ANIM_NONE,
    .palette = gMonPalette_Sphynxeon, .shinyPalette = gMonPalette_Sphynxeon,
    .iconSprite = gMonIcon_Sphynxeon, .iconPalIndex = 0, .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sSphynxeonLevelUpLearnset, .teachableLearnset = sSphynxeonInfinityTeachableLearnset,
},

[SPECIES_OMEON] =
{
    .baseHP = 70, .baseAttack = 124, .baseDefense = 85,
    .baseSpeed = 116, .baseSpAttack = 65, .baseSpDefense = 65,
    .types = MON_TYPES(TYPE_GHOST),
    .catchRate = 45, .expYield = 184,
    .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 20, .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_MEDIUM_FAST,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_FIELD),
    .abilities = { ABILITY_SUPER_LUCK, ABILITY_NONE, ABILITY_MOXIE }, .bodyColor = BODY_COLOR_BLACK,
    .speciesName = _("OMEON"), .cryId = CRY_EEVEE, .natDexNum = NATIONAL_DEX_EEVEE,
    .categoryName = _("Omen"), .height = 11, .weight = 180,
    .description = COMPOUND_STRING("A rare evolution awakened by unusual\n" "conditions in JOHTO. Its altered form\n" "draws out a new kind of strength."),
    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 256, .trainerOffset = 0,
    .frontPic = gMonFrontPic_Omeon, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_STRETCH,
    .backPic = gMonBackPic_Omeon, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 0, .backAnimId = BACK_ANIM_NONE,
    .palette = gMonPalette_Omeon, .shinyPalette = gMonPalette_Omeon,
    .iconSprite = gMonIcon_Omeon, .iconPalIndex = 2, .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sOmeonLevelUpLearnset, .teachableLearnset = sOmeonInfinityTeachableLearnset,
},

[SPECIES_JOLLIBIRD] =
{
    .baseHP = 80, .baseAttack = 50, .baseDefense = 105,
    .baseSpeed = 75, .baseSpAttack = 120, .baseSpDefense = 115,
    .types = MON_TYPES(TYPE_ICE, TYPE_FAIRY),
    .catchRate = 45, .expYield = 184,
    .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 20, .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_MEDIUM_FAST,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_WATER_1, EGG_GROUP_FAIRY),
    .abilities = { ABILITY_THICK_FAT, ABILITY_NONE, ABILITY_SNOW_WARNING }, .bodyColor = BODY_COLOR_RED,
    .speciesName = _("JOLLIBIRD"), .cryId = CRY_DELIBIRD, .natDexNum = NATIONAL_DEX_DELIBIRD,
    .categoryName = _("Present"), .height = 14, .weight = 980,
    .description = COMPOUND_STRING("A rare evolution awakened by unusual\n" "conditions in JOHTO. Its altered form\n" "draws out a new kind of strength."),
    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 256, .trainerOffset = 0,
    .frontPic = gMonFrontPic_Jollibird, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_STRETCH,
    .backPic = gMonBackPic_Jollibird, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 0, .backAnimId = BACK_ANIM_NONE,
    .palette = gMonPalette_Jollibird, .shinyPalette = gMonPalette_Jollibird,
    .iconSprite = gMonIcon_Jollibird, .iconPalIndex = 5, .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sJollibirdLevelUpLearnset, .teachableLearnset = sJollibirdInfinityTeachableLearnset,
},

[SPECIES_GRIMFOWL] =
{
    .baseHP = 112, .baseAttack = 63, .baseDefense = 80,
    .baseSpeed = 78, .baseSpAttack = 130, .baseSpDefense = 77,
    .types = MON_TYPES(TYPE_DARK, TYPE_FLYING),
    .catchRate = 45, .expYield = 184,
    .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 20, .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_MEDIUM_FAST,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_FLYING),
    .abilities = { ABILITY_UNNERVE, ABILITY_NONE, ABILITY_NO_GUARD }, .bodyColor = BODY_COLOR_BLACK,
    .speciesName = _("GRIMFOWL"), .cryId = CRY_NOCTOWL, .natDexNum = NATIONAL_DEX_NOCTOWL,
    .categoryName = _("Harbinger"), .height = 24, .weight = 700,
    .description = COMPOUND_STRING("A rare evolution awakened by unusual\n" "conditions in JOHTO. Its altered form\n" "draws out a new kind of strength."),
    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 256, .trainerOffset = 0,
    .frontPic = gMonFrontPic_Grimfowl, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_STRETCH,
    .backPic = gMonBackPic_Grimfowl, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 0, .backAnimId = BACK_ANIM_NONE,
    .palette = gMonPalette_Grimfowl, .shinyPalette = gMonPalette_Grimfowl,
    .iconSprite = gMonIcon_Grimfowl, .iconPalIndex = 0, .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sGrimfowlLevelUpLearnset, .teachableLearnset = sGrimfowlInfinityTeachableLearnset,
},

[SPECIES_KABLOWFISH] =
{
    .baseHP = 85, .baseAttack = 100, .baseDefense = 125,
    .baseSpeed = 75, .baseSpAttack = 65, .baseSpDefense = 85,
    .types = MON_TYPES(TYPE_WATER, TYPE_STEEL),
    .catchRate = 45, .expYield = 184,
    .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 20, .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_MEDIUM_FAST,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_WATER_2),
    .abilities = { ABILITY_POISON_POINT, ABILITY_SWIFT_SWIM, ABILITY_INTIMIDATE }, .bodyColor = BODY_COLOR_GRAY,
    .speciesName = _("KABLOWFISH"), .cryId = CRY_QWILFISH, .natDexNum = NATIONAL_DEX_QWILFISH,
    .categoryName = _("Naval Mine"), .height = 17, .weight = 600,
    .description = COMPOUND_STRING("A rare evolution awakened by unusual\n" "conditions in JOHTO. Its altered form\n" "draws out a new kind of strength."),
    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 256, .trainerOffset = 0,
    .frontPic = gMonFrontPic_Kablowfish, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_STRETCH,
    .backPic = gMonBackPic_Kablowfish, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 0, .backAnimId = BACK_ANIM_NONE,
    .palette = gMonPalette_Kablowfish, .shinyPalette = gMonPalette_Kablowfish,
    .iconSprite = gMonIcon_Kablowfish, .iconPalIndex = 0, .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sKablowfishLevelUpLearnset, .teachableLearnset = sKablowfishInfinityTeachableLearnset,
},

[SPECIES_MYSTYNX] =
{
    .baseHP = 75, .baseAttack = 60, .baseDefense = 40,
    .baseSpeed = 125, .baseSpAttack = 130, .baseSpDefense = 105,
    .types = MON_TYPES(TYPE_ICE, TYPE_FAIRY),
    .catchRate = 45, .expYield = 184,
    .genderRatio = MON_FEMALE,
    .eggCycles = 20, .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_MEDIUM_FAST,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_HUMAN_LIKE),
    .abilities = { ABILITY_COMPETITIVE, ABILITY_OBLIVIOUS, ABILITY_SNOW_WARNING }, .bodyColor = BODY_COLOR_PURPLE,
    .speciesName = _("MYSTYNX"), .cryId = CRY_JYNX, .natDexNum = NATIONAL_DEX_JYNX,
    .categoryName = _("Mystic"), .height = 17, .weight = 450,
    .description = COMPOUND_STRING("A rare evolution awakened by unusual\n" "conditions in JOHTO. Its altered form\n" "draws out a new kind of strength."),
    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 256, .trainerOffset = 0,
    .frontPic = gMonFrontPic_Mystynx, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_STRETCH,
    .backPic = gMonBackPic_Mystynx, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 0, .backAnimId = BACK_ANIM_NONE,
    .palette = gMonPalette_Mystynx, .shinyPalette = gMonShinyPalette_Mystynx,
    .iconSprite = gMonIcon_Mystynx, .iconPalIndex = 2, .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sMystynxLevelUpLearnset, .teachableLearnset = sMystynxInfinityTeachableLearnset,
},

[SPECIES_SUNFLORID] =
{
    .baseHP = 110, .baseAttack = 90, .baseDefense = 75,
    .baseSpeed = 65, .baseSpAttack = 115, .baseSpDefense = 80,
    .types = MON_TYPES(TYPE_GRASS, TYPE_FIRE),
    .catchRate = 45, .expYield = 184,
    .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 20, .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_MEDIUM_FAST,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_GRASS),
    .abilities = { ABILITY_CHLOROPHYLL, ABILITY_SOLAR_POWER, ABILITY_DROUGHT }, .bodyColor = BODY_COLOR_YELLOW,
    .speciesName = _("SUNFLORID"), .cryId = CRY_SUNFLORA, .natDexNum = NATIONAL_DEX_SUNFLORA,
    .categoryName = _("Sunfire"), .height = 10, .weight = 340,
    .description = COMPOUND_STRING("A rare evolution awakened by unusual\n" "conditions in JOHTO. Its altered form\n" "draws out a new kind of strength."),
    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 256, .trainerOffset = 0,
    .frontPic = gMonFrontPic_Sunflorid, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_STRETCH,
    .backPic = gMonBackPic_Sunflorid, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 0, .backAnimId = BACK_ANIM_NONE,
    .palette = gMonPalette_Sunflorid, .shinyPalette = gMonPalette_Sunflorid,
    .iconSprite = gMonIcon_Sunflorid, .iconPalIndex = 1, .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sSunfloridLevelUpLearnset, .teachableLearnset = sSunfloridInfinityTeachableLearnset,
},

[SPECIES_OSTEODIAN] =
{
    .baseHP = 105, .baseAttack = 95, .baseDefense = 145,
    .baseSpeed = 60, .baseSpAttack = 60, .baseSpDefense = 95,
    .types = MON_TYPES(TYPE_GROUND),
    .catchRate = 45, .expYield = 220,
    .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 20, .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_MEDIUM_FAST,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_MONSTER),
    .abilities = { ABILITY_ROCK_HEAD, ABILITY_SCRAPPY, ABILITY_BATTLE_ARMOR },
    .bodyColor = BODY_COLOR_BROWN,
    .speciesName = _("OSTEODIAN"), .cryId = CRY_MAROWAK, .natDexNum = NATIONAL_DEX_MAROWAK,
    .categoryName = _("Guardian"), .height = 20, .weight = 860,
    .description = COMPOUND_STRING(
        "Its ancient skeleton has hardened into\n"
        "natural armor. It stands guard over\n"
        "weaker Pokémon without retreating."),
    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 256, .trainerOffset = 0,
    .frontPic = gMonFrontPic_Osteodian, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_STRETCH,
    .backPic = gMonBackPic_Osteodian, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 0, .backAnimId = BACK_ANIM_NONE,
    .palette = gMonPalette_Osteodian, .shinyPalette = gMonShinyPalette_Osteodian,
    .iconSprite = gMonIcon_Osteodian, .iconPalIndex = 0, .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sMarowakLevelUpLearnset, .teachableLearnset = sMarowakTeachableLearnset,
},

[SPECIES_MAROGHOST] =
{
    .baseHP = 100, .baseAttack = 140, .baseDefense = 120,
    .baseSpeed = 70, .baseSpAttack = 50, .baseSpDefense = 90,
    .types = MON_TYPES(TYPE_GROUND, TYPE_GHOST),
    .catchRate = 45, .expYield = 220,
    .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 20, .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_MEDIUM_FAST,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_MONSTER),
    .abilities = { ABILITY_ROCK_HEAD, ABILITY_CURSED_BODY, ABILITY_BATTLE_ARMOR },
    .bodyColor = BODY_COLOR_PURPLE,
    .speciesName = _("MAROGHOST"), .cryId = CRY_MAROWAK, .natDexNum = NATIONAL_DEX_MAROWAK,
    .categoryName = _("Bone Wraith"), .height = 16, .weight = 600,
    .description = COMPOUND_STRING(
        "A spectral force clings to its bone club.\n"
        "It stalks the dark in silence and strikes\n"
        "with terrifying physical strength."),
    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 256, .trainerOffset = 0,
    .frontPic = gMonFrontPic_Maroghost, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_SQUISH_AND_BOUNCE,
    .backPic = gMonBackPic_Maroghost, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 0, .backAnimId = BACK_ANIM_NONE,
    .palette = gMonPalette_Maroghost, .shinyPalette = gMonShinyPalette_Maroghost,
    .iconSprite = gMonIcon_Maroghost, .iconPalIndex = 2, .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sMarowakLevelUpLearnset, .teachableLearnset = sMarowakTeachableLearnset,
},

[SPECIES_ALPHORACLE] =
{
    .baseHP = 100, .baseAttack = 70, .baseDefense = 110,
    .baseSpeed = 100, .baseSpAttack = 150, .baseSpDefense = 150,
    .types = MON_TYPES(TYPE_PSYCHIC, TYPE_FAIRY),
    .catchRate = 3, .expYield = 306,
    .genderRatio = MON_GENDERLESS,
    .eggCycles = 120, .friendship = 0,
    .growthRate = GROWTH_SLOW,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_NO_EGGS_DISCOVERED),
    .abilities = { ABILITY_FULL_METAL_BODY, ABILITY_NONE, ABILITY_NONE }, .bodyColor = BODY_COLOR_PURPLE,
    .speciesName = _("ALPHORACLE"), .cryId = CRY_UNOWN, .natDexNum = NATIONAL_DEX_UNOWN,
    .categoryName = _("First Voice"), .height = 25, .weight = 999,
    .description = COMPOUND_STRING("An ancient guardian that watches over\n" "the language of the RUINS. Its presence\n" "causes RELIC resonance to stir."),
    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 256, .trainerOffset = 0,
    .frontPic = gMonFrontPic_Alphoracle, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_STRETCH,
    .backPic = gMonBackPic_Alphoracle, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 0, .backAnimId = BACK_ANIM_NONE,
    .palette = gMonPalette_Alphoracle, .shinyPalette = gMonPalette_Alphoracle,
    .iconSprite = gMonIcon_Alphoracle, .iconPalIndex = 4, .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sAlphoracleLevelUpLearnset, .teachableLearnset = sAlphoracleInfinityTeachableLearnset,
},

[SPECIES_PINSIREX] =
{
    .baseHP = 80, .baseAttack = 135, .baseDefense = 100,
    .baseSpeed = 110, .baseSpAttack = 45, .baseSpDefense = 80,
    .types = MON_TYPES(TYPE_BUG, TYPE_FLYING),
    .catchRate = 45, .expYield = 210,
    .genderRatio = PERCENT_FEMALE(50),
    .eggCycles = 25, .friendship = STANDARD_FRIENDSHIP,
    .growthRate = GROWTH_SLOW,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_BUG),
    .abilities = { ABILITY_AERILATE, ABILITY_MOLD_BREAKER, ABILITY_HYPER_CUTTER },
    .bodyColor = BODY_COLOR_BROWN,
    .speciesName = _("PINSIREX"), .cryId = CRY_PINSIR, .natDexNum = NATIONAL_DEX_PINSIR,
    .categoryName = _("Relic Stag"), .height = 17, .weight = 590,
    .description = COMPOUND_STRING(
        "Ancient power has awakened its wings.\n"
        "It dives at high speed before locking\n"
        "its mighty horns around its foe."),
    .pokemonScale = 256, .pokemonOffset = 2, .trainerScale = 257, .trainerOffset = 0,
    .frontPic = gMonFrontPic_PinsirMega, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 5,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_SQUISH_AND_BOUNCE,
    .backPic = gMonBackPic_PinsirMega, .backPicSize = MON_COORDS_SIZE(64, 56), .backPicYOffset = 6,
    .backAnimId = BACK_ANIM_V_SHAKE_LOW,
    .palette = gMonPalette_PinsirMega, .shinyPalette = gMonShinyPalette_PinsirMega,
    .iconSprite = gMonIcon_PinsirMega, .iconPalIndex = 2,
    .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    .levelUpLearnset = sPinsirexLevelUpLearnset,
    .teachableLearnset = sPinsirTeachableLearnset,
},

#define PJR_FINAL_SPECIES(species, hp, atk, def, spa, spd, spe, type1, type2, ability1, ability2, hidden, name, cry, natdex, category, color, front, back, pal, shiny, icon, iconPal, levelMoves, teachMoves) \
[species] = { \
    .baseHP = hp, .baseAttack = atk, .baseDefense = def, .baseSpAttack = spa, .baseSpDefense = spd, .baseSpeed = spe, \
    .types = MON_TYPES(type1, type2), .catchRate = 45, .expYield = 220, .genderRatio = PERCENT_FEMALE(50), \
    .eggCycles = 25, .friendship = STANDARD_FRIENDSHIP, .growthRate = GROWTH_SLOW, \
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_FIELD), .abilities = { ability1, ability2, hidden }, .bodyColor = color, \
    .speciesName = _(name), .cryId = cry, .natDexNum = natdex, .categoryName = _(category), .height = 16, .weight = 600, \
    .description = COMPOUND_STRING("Relic energy awakened this final form.\nIts ancient strength protects JOHTO\nand all who travel beside it."), \
    .pokemonScale = 256, .trainerScale = 256, \
    .frontPic = front, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 2, \
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_STRETCH, \
    .backPic = back, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 6, .backAnimId = BACK_ANIM_NONE, \
    .palette = pal, .shinyPalette = shiny, .iconSprite = icon, .iconPalIndex = iconPal, \
    .pokemonJumpType = PKMN_JUMP_TYPE_NONE, .levelUpLearnset = levelMoves, .teachableLearnset = teachMoves, \
}

PJR_FINAL_SPECIES(SPECIES_MILTITAN, 110, 120, 105, 45, 100, 75, TYPE_NORMAL, TYPE_FAIRY,
    ABILITY_THICK_FAT, ABILITY_SCRAPPY, ABILITY_SAP_SIPPER, "MILTITAN", CRY_MILTANK,
    NATIONAL_DEX_MILTANK, "Relic Cow", BODY_COLOR_PINK, gMonFrontPic_Miltitan, gMonBackPic_Miltitan,
    gMonPalette_Miltitan, gMonShinyPalette_Miltitan, gMonIcon_Miltitan, 0, sMiltitanLevelUpLearnset, sMiltankTeachableLearnset),

PJR_FINAL_SPECIES(SPECIES_SHUCKOLOSSE, 40, 30, 230, 30, 230, 20, TYPE_BUG, TYPE_ROCK,
    ABILITY_ANCIENT_BASTION, ABILITY_NONE, ABILITY_NONE, "SHUCKOLOSSE", CRY_SHUCKLE,
    NATIONAL_DEX_SHUCKLE, "Bastion", BODY_COLOR_YELLOW, gMonFrontPic_Shuckolosse, gMonBackPic_Shuckolosse,
    gMonPalette_Shuckolosse, gMonShinyPalette_Shuckolosse, gMonIcon_Shuckolosse, 1, sShuckolosseLevelUpLearnset, sShuckleTeachableLearnset),

PJR_FINAL_SPECIES(SPECIES_SUDOWARDEN, 90, 125, 145, 40, 95, 40, TYPE_ROCK, TYPE_GRASS,
    ABILITY_STURDY, ABILITY_ROCK_HEAD, ABILITY_SAP_SIPPER, "SUDOWARDEN", CRY_SUDOWOODO,
    NATIONAL_DEX_SUDOWOODO, "Ancient Tree", BODY_COLOR_BROWN, gMonFrontPic_Sudowarden, gMonBackPic_Sudowarden,
    gMonPalette_Sudowarden, gMonShinyPalette_Sudowarden, gMonIcon_Sudowarden, 1, sSudowardenLevelUpLearnset, sSudowoodoTeachableLearnset),

PJR_FINAL_SPECIES(SPECIES_DONPHALANX, 110, 140, 135, 60, 85, 60, TYPE_GROUND, TYPE_DARK,
    ABILITY_STAMINA, ABILITY_INTIMIDATE, ABILITY_SAND_RUSH, "DONPHALANX", CRY_DONPHAN,
    NATIONAL_DEX_DONPHAN, "War Tusk", BODY_COLOR_GRAY, gMonFrontPic_Donphalanx, gMonBackPic_Donphalanx,
    gMonPalette_Donphalanx, gMonShinyPalette_Donphalanx, gMonIcon_Donphalanx, 2, sDonphalanxLevelUpLearnset, sDonphanTeachableLearnset),

PJR_FINAL_SPECIES(SPECIES_FAERANIUM, 100, 85, 115, 105, 120, 65, TYPE_GRASS, TYPE_FAIRY,
    ABILITY_ANCIENT_BLOOM, ABILITY_NONE, ABILITY_NONE, "FAERANIUM", CRY_MEGANIUM,
    NATIONAL_DEX_MEGANIUM, "Bloom Relic", BODY_COLOR_GREEN, gMonFrontPic_Faeranium, gMonBackPic_Faeranium,
    gMonPalette_Faeranium, gMonShinyPalette_Faeranium, gMonIcon_Faeranium, 1, sFaeraniumLevelUpLearnset, sMeganiumTeachableLearnset),

PJR_FINAL_SPECIES(SPECIES_PYROCLAST, 85, 95, 85, 130, 90, 105, TYPE_FIRE, TYPE_GHOST,
    ABILITY_CINDER_VEIL, ABILITY_NONE, ABILITY_NONE, "PYROCLAST", CRY_TYPHLOSION,
    NATIONAL_DEX_TYPHLOSION, "Cinder Relic", BODY_COLOR_RED, gMonFrontPic_Pyroclast, gMonBackPic_Pyroclast,
    gMonPalette_Pyroclast, gMonShinyPalette_Pyroclast, gMonIcon_Pyroclast, 1, sPyroclastLevelUpLearnset, sTyphlosionTeachableLearnset),

PJR_FINAL_SPECIES(SPECIES_FERALODON, 105, 135, 105, 70, 85, 80, TYPE_WATER, TYPE_DRAGON,
    ABILITY_TIDAL_ROAR, ABILITY_NONE, ABILITY_NONE, "FERALODON", CRY_FERALIGATR,
    NATIONAL_DEX_FERALIGATR, "Tidal Relic", BODY_COLOR_BLUE, gMonFrontPic_Feralodon, gMonBackPic_Feralodon,
    gMonPalette_Feralodon, gMonShinyPalette_Feralodon, gMonIcon_Feralodon, 3, sFeralodonLevelUpLearnset, sFeraligatrTeachableLearnset),

PJR_FINAL_SPECIES(SPECIES_DRAKEON, 75, 130, 85, 110, 65, 80, TYPE_DRAGON, TYPE_DRAGON,
    ABILITY_INTIMIDATE, ABILITY_NONE, ABILITY_MULTISCALE, "DRAKEON", CRY_EEVEE,
    NATIONAL_DEX_EEVEE, "Wyvern", BODY_COLOR_BLUE, gMonFrontPic_Drakeon, gMonBackPic_Drakeon,
    gMonPalette_Drakeon, gMonShinyPalette_Drakeon, gMonIcon_Drakeon, 0, sDrakeonLevelUpLearnset, sEeveeTeachableLearnset),

PJR_FINAL_SPECIES(SPECIES_GHOULBAT, 95, 110, 90, 80, 95, 130, TYPE_GHOST, TYPE_FLYING,
    ABILITY_INFILTRATOR, ABILITY_PRESSURE, ABILITY_CURSED_BODY, "GHOULBAT", CRY_CROBAT,
    NATIONAL_DEX_CROBAT, "Wraith", BODY_COLOR_PURPLE, gMonFrontPic_Ghoulbat, gMonBackPic_Ghoulbat,
    gMonPalette_Ghoulbat, gMonShinyPalette_Ghoulbat, gMonIcon_Ghoulbat, 0, sGhoulbatLevelUpLearnset, sCrobatTeachableLearnset),

[SPECIES_RELIC_HO_OH] =
{
    .baseHP = 106, .baseAttack = 100, .baseDefense = 100,
    .baseSpeed = 114, .baseSpAttack = 140, .baseSpDefense = 140,
    .types = MON_TYPES(TYPE_FIRE, TYPE_FAIRY),
    .catchRate = 3, .expYield = 340,
    .evYield_SpDefense = 3,
    .itemCommon = ITEM_SACRED_ASH, .itemRare = ITEM_SACRED_ASH,
    .genderRatio = MON_GENDERLESS, .eggCycles = 120, .friendship = 0,
    .growthRate = GROWTH_SLOW,
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_NO_EGGS_DISCOVERED),
    .abilities = { ABILITY_SACRED_REBIRTH, ABILITY_SACRED_REBIRTH, ABILITY_SACRED_REBIRTH },
    .bodyColor = BODY_COLOR_YELLOW,
    .speciesName = _("RELIC HO-OH"), .cryId = CRY_HO_OH, .natDexNum = NATIONAL_DEX_HO_OH,
    .categoryName = _("Rainbow Relic"), .height = 38, .weight = 1990,
    .description = COMPOUND_STRING("An ancient Ho-Oh awakened by Relic
Resonance. Its sacred flame refuses
to be extinguished."),
    .pokemonScale = 256, .pokemonOffset = 0, .trainerScale = 610, .trainerOffset = 17,
    .frontPic = gMonFrontPic_HoOhRelic, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 0,
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_GROW_VIBRATE,
    .enemyMonElevation = 6,
    .backPic = gMonBackPic_HoOhRelic, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 1,
    .backAnimId = BACK_ANIM_SHAKE_GLOW_RED,
    .palette = gMonPalette_HoOhRelic, .shinyPalette = gMonShinyPalette_HoOhRelic,
    .iconSprite = gMonIcon_HoOhRelic, .iconPalIndex = 1,
    .pokemonJumpType = PKMN_JUMP_TYPE_NONE,
    SHADOW(1, 17, SHADOW_SIZE_L)
    FOOTPRINT(HoOh)
    OVERWORLD(
        sPicTable_HoOh,
        SIZE_64x64,
        SHADOW_SIZE_M,
        TRACKS_NONE,
        sAnimTable_Following,
        gOverworldPalette_HoOh,
        gShinyOverworldPalette_HoOh
    )
    .isRestrictedLegendary = TRUE,
    .isFrontierBanned = TRUE,
    .perfectIVCount = LEGENDARY_PERFECT_IV_COUNT,
    .levelUpLearnset = sRelicHoOhLevelUpLearnset,
    .teachableLearnset = sHoOhTeachableLearnset,
},

#undef PJR_FINAL_SPECIES

#define PJR_RED_SPECIES(species, hp, atk, def, spa, spd, spe, type1, type2, ability, name, cry, natdex, color, front, back, pal, shiny, icon, levelMoves, teachMoves) \
[species] = { \
    .baseHP = hp, .baseAttack = atk, .baseDefense = def, .baseSpAttack = spa, .baseSpDefense = spd, .baseSpeed = spe, \
    .types = MON_TYPES(type1, type2), .catchRate = 45, .expYield = 250, .genderRatio = PERCENT_FEMALE(50), \
    .eggCycles = 25, .friendship = STANDARD_FRIENDSHIP, .growthRate = GROWTH_MEDIUM_SLOW, \
    .eggGroups = MON_EGG_GROUPS(EGG_GROUP_FIELD), .abilities = { ability, ABILITY_NONE, ABILITY_NONE }, .bodyColor = color, \
    .speciesName = _(name), .cryId = cry, .natDexNum = natdex, .categoryName = _("Relic"), .height = 16, .weight = 600, \
    .description = COMPOUND_STRING("A champion of KANTO's Relic age.\nIts Resonance has been refined through\ncountless battles beside RED."), \
    .pokemonScale = 256, .trainerScale = 256, \
    .frontPic = front, .frontPicSize = MON_COORDS_SIZE(64, 64), .frontPicYOffset = 2, \
    .frontAnimFrames = sAnims_SingleFramePlaceHolder, .frontAnimId = ANIM_V_STRETCH, \
    .backPic = back, .backPicSize = MON_COORDS_SIZE(64, 64), .backPicYOffset = 6, .backAnimId = BACK_ANIM_NONE, \
    .palette = pal, .shinyPalette = shiny, .iconSprite = icon, .iconPalIndex = 0, \
    .pokemonJumpType = PKMN_JUMP_TYPE_NONE, .levelUpLearnset = levelMoves, .teachableLearnset = teachMoves, \
}

PJR_RED_SPECIES(SPECIES_EDENSAUR, 95, 80, 110, 135, 105, 55, TYPE_GRASS, TYPE_POISON,
    ABILITY_GRASSY_SURGE, "EDENSAUR", CRY_VENUSAUR, NATIONAL_DEX_VENUSAUR, BODY_COLOR_GREEN,
    gMonFrontPic_Edensaur, gMonBackPic_Edensaur, gMonPalette_Edensaur, gMonShinyPalette_Edensaur, gMonIcon_Edensaur,
    sVenusaurLevelUpLearnset, sVenusaurTeachableLearnset),

PJR_RED_SPECIES(SPECIES_CHARAXIS, 80, 120, 85, 90, 80, 125, TYPE_FIRE, TYPE_FLYING,
    ABILITY_GALE_WINGS, "CHARAXIS", CRY_CHARIZARD, NATIONAL_DEX_CHARIZARD, BODY_COLOR_RED,
    gMonFrontPic_Charaxis, gMonBackPic_Charaxis, gMonPalette_Charaxis, gMonShinyPalette_Charaxis, gMonIcon_Charaxis,
    sCharizardLevelUpLearnset, sCharizardTeachableLearnset),

PJR_RED_SPECIES(SPECIES_FORTOTOISE, 95, 80, 155, 100, 105, 50, TYPE_WATER, TYPE_STEEL,
    ABILITY_STURDY, "FORTOTOISE", CRY_BLASTOISE, NATIONAL_DEX_BLASTOISE, BODY_COLOR_BLUE,
    gMonFrontPic_Fortotoise, gMonBackPic_Fortotoise, gMonPalette_Fortotoise, gMonShinyPalette_Fortotoise, gMonIcon_Fortotoise,
    sBlastoiseLevelUpLearnset, sBlastoiseTeachableLearnset),

PJR_RED_SPECIES(SPECIES_KHANG, 105, 105, 95, 50, 90, 110, TYPE_NORMAL, TYPE_NORMAL,
    ABILITY_PARENTAL_BOND, "KHANG", CRY_KANGASKHAN, NATIONAL_DEX_KANGASKHAN, BODY_COLOR_BROWN,
    gMonFrontPic_Khang, gMonBackPic_Khang, gMonPalette_Khang, gMonShinyPalette_Khang, gMonIcon_Kangaskhan,
    sKangaskhanLevelUpLearnset, sKangaskhanTeachableLearnset),

PJR_RED_SPECIES(SPECIES_NOLAX, 100, 130, 80, 45, 90, 130, TYPE_NORMAL, TYPE_NORMAL,
    ABILITY_INSOMNIA, "NOLAX", CRY_SNORLAX, NATIONAL_DEX_SNORLAX, BODY_COLOR_BLUE,
    gMonFrontPic_Nolax, gMonBackPic_Nolax, gMonPalette_Nolax, gMonShinyPalette_Nolax, gMonIcon_Snorlax,
    sSnorlaxLevelUpLearnset, sSnorlaxTeachableLearnset),

PJR_RED_SPECIES(SPECIES_NOXICHU, 70, 110, 70, 110, 80, 125, TYPE_ELECTRIC, TYPE_DARK,
    ABILITY_INFILTRATOR, "NOXICHU", CRY_PIKACHU, NATIONAL_DEX_PIKACHU, BODY_COLOR_YELLOW,
    gMonFrontPic_Noxichu, gMonBackPic_Noxichu, gMonPalette_Noxichu, gMonShinyPalette_Noxichu, gMonIcon_Pikachu,
    sPikachuLevelUpLearnset, sPikachuTeachableLearnset),

#undef PJR_RED_SPECIES
