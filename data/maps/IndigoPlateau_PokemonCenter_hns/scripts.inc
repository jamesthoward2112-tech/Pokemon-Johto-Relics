IndigoPlateau_PokemonCenter_hns_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, IndigoPlateau_PokemonCenter_OnFrame 
	map_script MAP_SCRIPT_ON_TRANSITION, IndigoPlateau_Pokecenter_OnTransition
	.byte 0

IndigoPlateau_PokemonCenter_OnFrame::
	map_script_2 VAR_LEAGUE_STATE, 0, IndigoPlateau_PokemonCenter_Enter
	map_script_2 VAR_LEAGUE_STATE, 2, IndigoPlateau_PokemonCenter_Enter
	map_script_2 VAR_LEAGUE_STATE, 3, IndigoPlateau_PokemonCenter_Enter
	map_script_2 VAR_LEAGUE_STATE, 4, IndigoPlateau_PokemonCenter_Enter
	map_script_2 VAR_LEAGUE_STATE, 5, IndigoPlateau_PokemonCenter_Enter
	map_script_2 VAR_LEAGUE_STATE, 6, IndigoPlateau_PokemonCenter_Enter
	.2byte 0

IndigoPlateau_PokemonCenter_Enter::
	setflag FLAG_VISITED_INDIGO_PLATEAU
	setvar VAR_LEAGUE_STATE, 1
	end

IndigoPlateau_Pokecenter_OnTransition::
	setrespawn HEAL_LOCATION_INDIGO_PLATEAU_HNS
	end


IndigoPlateau_EventScript_Cooltrainer::
	goto IndigoPlateau_EventScript_HazardTutor
	end

IndigoPlateau_EventScript_BlackBelt::
	msgbox IndigoPlateau_Text_Blackbelt, MSGBOX_NPC
	end

IndigoPlateau_EventScript_ShigyNinja::
	goto IndigoPlateau_EventScript_CleanupTutor
	end

IndigoPlateau_Text_ShigyNinja:
	.string "Congrats on making it here!\p"
	.string "I've seen tons of trainers come\n"
	.string "through here over the years, and\l"
	.string "all of them are wonderfully unique.\p"
	.string "You should be proud of yourself\n"
	.string "for getting this far!\p"
	.string "Now, go get 'em!$"

IndigoPlateau_Text_Blackbelt:
	.string "The POKéMON LEAGUE is not taking\n"
	.string "new challengers at the moment.\p"
	.string "Please check back later.$"

IndigoPlateau_Text_CooltrainerM:
    .string "At the POKéMON LEAGUE, you'll get\n"
    .string "tested by the ELITE FOUR.\p"
    .string "You have to beat them all. If you\n"
    .string "lose, you have to start all over!$"

IndigoPlateau_EventScript_Silver::
	lock
	faceplayer 
	goto_if_set FLAG_DAILY_BEAT_SILVER, IndigoPlateau_EventScript_SilverBeat
	msgbox IndigoPlateau_Text_RivalEntrance1, MSGBOX_DEFAULT
	call_if_eq VAR_STARTER_MON, 0, IndigoPlateau_Silver_Battle_Cyndaquil
	call_if_eq VAR_STARTER_MON, 1, IndigoPlateau_Silver_Battle_Totodile
	call_if_eq VAR_STARTER_MON, 2, IndigoPlateau_Silver_Battle_Chikorita
	msgbox IndigoPlateau_Text_RivalAfter, MSGBOX_DEFAULT
	setflag FLAG_DAILY_BEAT_SILVER
	release
	end

IndigoPlateau_EventScript_SilverBeat::
	msgbox IndigoPlateau_Text_RivalAfter, MSGBOX_DEFAULT
	closemessage
	release
	end

IndigoPlateau_Silver_Battle_Cyndaquil::
	trainerbattle_no_intro TRAINER_RIVAL_CYNDAQUIL_7_HNS, IndigoPlateau_Text_RivalWin
	return

IndigoPlateau_Silver_Battle_Totodile::
	trainerbattle_no_intro TRAINER_RIVAL_TOTODILE_7_HNS, IndigoPlateau_Text_RivalWin
	return

IndigoPlateau_Silver_Battle_Chikorita::
	trainerbattle_no_intro TRAINER_RIVAL_CHIKORITA_7_HNS, IndigoPlateau_Text_RivalWin
	return

IndigoPlateau_Text_RivalEntrance1:
    .string "Hold it.\p"
    .string "You're going to take the POKéMON\n"
    .string "LEAGUE challenge now?\p"
    .string "That's not going to happen.\p"
    .string "My super-well-trained POKéMON\n"
    .string "are going to pound you.\p"
    .string "{PLAYER}!\n"
    .string "I challenge you!$"

IndigoPlateau_Text_RivalWin:
    .string "…\p"
    .string "OK--I lost…$"

IndigoPlateau_Text_RivalAfter:
    .string "…Darn… I still can't win…\p"
    .string "I… I have to think more about my\n"
    .string "POKéMON…\p"
    .string "Humph! Try not to lose!$"

IndigoPlateau_EventScript_Psychic::
	lock
	faceplayer
	msgbox IndigoPlateau_Text_TeleportGuy1, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, TRUE, IndigoPlateau_EventScript_PsychicTeleport
	msgbox IndigoPlateau_Text_TeleportGuyNo, MSGBOX_DEFAULT
	closemessage
	release
	end

IndigoPlateau_EventScript_PsychicTeleport::
	msgbox IndigoPlateau_Text_TeleportGuyYes, MSGBOX_DEFAULT
	closemessage
	turnobject OBJ_EVENT_ID_PLAYER, DIR_SOUTH
	playbgm MUS_HG_NEW_BARK, FALSE
	delay 60
	playmoncry SPECIES_ABRA, CRY_MODE_NORMAL
	applymovement2 LOCALID_INDIGOPLATEAU_ABRA, IndigoPLateau_Movement_Abra
	waitmovement 0
	fadescreen FADE_TO_WHITE
	warpteleport MAP_NEW_BARK_TOWN_HNS, 20, 12
	waitstate
	release
	end
	
IndigoPLateau_Movement_Abra:
	jump_in_place_right
	jump_in_place_right
	step_end

IndigoPlateau_EventScript_Abra::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_ABRA, CRY_MODE_NORMAL
	msgbox IndigoPlateau_Text_Abra, MSGBOX_DEFAULT
	waitmoncry
	release
	end

IndigoPlateau_Text_TeleportGuy1:
    .string "Ah! You're challenging the ELITE\n"
    .string "FOUR? Are you sure you're ready?\p"
    .string "If you need to train some more,\n"
    .string "my ABRA can help you.\p"
    .string "It can TELEPORT you home.\p"
    .string "Would you like to go home now?$"

IndigoPlateau_Text_TeleportGuyYes:
    .string "OK, OK. Picture your house in your\n"
    .string "mind…$"

IndigoPlateau_Text_TeleportGuyNo:
    .string "OK, OK. The best of luck to you!$"

IndigoPlateau_Text_Abra:
    .string "ABRA: Aabra…$"


@ PJR tactical move tutors: free, repeatable, and deliberately placed in Indigo Plateau.
IndigoPlateau_EventScript_HazardTutor::
	lock
	faceplayer
	message IndigoPlateau_Text_HazardTutorIntro
	waitmessage
	dynmultichoice 0, 0, FALSE, 6, 0, DYN_MULTICHOICE_CB_NONE, IndigoPlateau_Text_TutorMove_StealthRock, IndigoPlateau_Text_TutorMove_Spikes, IndigoPlateau_Text_TutorMove_ToxicSpikes, IndigoPlateau_Text_TutorMove_StickyWeb, IndigoPlateau_Text_TutorMove_StoneAxe, IndigoPlateau_Text_TutorMove_CeaselessEdge, IndigoPlateau_Text_TutorMove_SaltCure, IndigoPlateau_Text_TutorMove_LeechSeed, IndigoPlateau_Text_TutorMove_Toxic, IndigoPlateau_Text_TutorMove_WillOWisp, IndigoPlateau_Text_TutorMove_ThunderWave, IndigoPlateau_Text_TutorMove_Taunt, IndigoPlateau_Text_TutorMove_Encore, IndigoPlateau_Text_TutorMove_KnockOff, IndigoPlateau_Text_TutorMove_Roar, IndigoPlateau_Text_TutorMove_Whirlwind, IndigoPlateau_Text_TutorMove_DragonTail, IndigoPlateau_Text_TutorMove_Infestation, IndigoPlateau_Text_TutorMove_Cancel
	switch VAR_RESULT
	case 0, IndigoPlateau_EventScript_TutorTeach_StealthRock
	case 1, IndigoPlateau_EventScript_TutorTeach_Spikes
	case 2, IndigoPlateau_EventScript_TutorTeach_ToxicSpikes
	case 3, IndigoPlateau_EventScript_TutorTeach_StickyWeb
	case 4, IndigoPlateau_EventScript_TutorTeach_StoneAxe
	case 5, IndigoPlateau_EventScript_TutorTeach_CeaselessEdge
	case 6, IndigoPlateau_EventScript_TutorTeach_SaltCure
	case 7, IndigoPlateau_EventScript_TutorTeach_LeechSeed
	case 8, IndigoPlateau_EventScript_TutorTeach_Toxic
	case 9, IndigoPlateau_EventScript_TutorTeach_WillOWisp
	case 10, IndigoPlateau_EventScript_TutorTeach_ThunderWave
	case 11, IndigoPlateau_EventScript_TutorTeach_Taunt
	case 12, IndigoPlateau_EventScript_TutorTeach_Encore
	case 13, IndigoPlateau_EventScript_TutorTeach_KnockOff
	case 14, IndigoPlateau_EventScript_TutorTeach_Roar
	case 15, IndigoPlateau_EventScript_TutorTeach_Whirlwind
	case 16, IndigoPlateau_EventScript_TutorTeach_DragonTail
	case 17, IndigoPlateau_EventScript_TutorTeach_Infestation
	case 18, IndigoPlateau_EventScript_TutorDecline
	case MULTI_B_PRESSED, IndigoPlateau_EventScript_TutorDecline
	end

IndigoPlateau_EventScript_CleanupTutor::
	lock
	faceplayer
	message IndigoPlateau_Text_CleanupTutorIntro
	waitmessage
	dynmultichoice 0, 0, FALSE, 6, 0, DYN_MULTICHOICE_CB_NONE, IndigoPlateau_Text_TutorMove_RapidSpin, IndigoPlateau_Text_TutorMove_Defog, IndigoPlateau_Text_TutorMove_MortalSpin, IndigoPlateau_Text_TutorMove_TidyUp, IndigoPlateau_Text_TutorMove_CourtChange, IndigoPlateau_Text_TutorMove_Haze, IndigoPlateau_Text_TutorMove_ClearSmog, IndigoPlateau_Text_TutorMove_BrickBreak, IndigoPlateau_Text_TutorMove_PsychicFangs, IndigoPlateau_Text_TutorMove_IceSpinner, IndigoPlateau_Text_TutorMove_HealBell, IndigoPlateau_Text_TutorMove_Aromatherapy, IndigoPlateau_Text_TutorMove_UTurn, IndigoPlateau_Text_TutorMove_VoltSwitch, IndigoPlateau_Text_TutorMove_FlipTurn, IndigoPlateau_Text_TutorMove_PartingShot, IndigoPlateau_Text_TutorMove_Snarl, IndigoPlateau_Text_TutorMove_IcyWind, IndigoPlateau_Text_TutorMove_BreakingSwipe, IndigoPlateau_Text_TutorMove_ChillingWater, IndigoPlateau_Text_TutorMove_AcidSpray, IndigoPlateau_Text_TutorMove_Nuzzle, IndigoPlateau_Text_TutorMove_Cancel
	switch VAR_RESULT
	case 0, IndigoPlateau_EventScript_TutorTeach_RapidSpin
	case 1, IndigoPlateau_EventScript_TutorTeach_Defog
	case 2, IndigoPlateau_EventScript_TutorTeach_MortalSpin
	case 3, IndigoPlateau_EventScript_TutorTeach_TidyUp
	case 4, IndigoPlateau_EventScript_TutorTeach_CourtChange
	case 5, IndigoPlateau_EventScript_TutorTeach_Haze
	case 6, IndigoPlateau_EventScript_TutorTeach_ClearSmog
	case 7, IndigoPlateau_EventScript_TutorTeach_BrickBreak
	case 8, IndigoPlateau_EventScript_TutorTeach_PsychicFangs
	case 9, IndigoPlateau_EventScript_TutorTeach_IceSpinner
	case 10, IndigoPlateau_EventScript_TutorTeach_HealBell
	case 11, IndigoPlateau_EventScript_TutorTeach_Aromatherapy
	case 12, IndigoPlateau_EventScript_TutorTeach_UTurn
	case 13, IndigoPlateau_EventScript_TutorTeach_VoltSwitch
	case 14, IndigoPlateau_EventScript_TutorTeach_FlipTurn
	case 15, IndigoPlateau_EventScript_TutorTeach_PartingShot
	case 16, IndigoPlateau_EventScript_TutorTeach_Snarl
	case 17, IndigoPlateau_EventScript_TutorTeach_IcyWind
	case 18, IndigoPlateau_EventScript_TutorTeach_BreakingSwipe
	case 19, IndigoPlateau_EventScript_TutorTeach_ChillingWater
	case 20, IndigoPlateau_EventScript_TutorTeach_AcidSpray
	case 21, IndigoPlateau_EventScript_TutorTeach_Nuzzle
	case 22, IndigoPlateau_EventScript_TutorDecline
	case MULTI_B_PRESSED, IndigoPlateau_EventScript_TutorDecline
	end

IndigoPlateau_EventScript_TutorTeach_StealthRock::
	setvar VAR_0x8005, MOVE_STEALTH_ROCK
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_Spikes::
	setvar VAR_0x8005, MOVE_SPIKES
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_ToxicSpikes::
	setvar VAR_0x8005, MOVE_TOXIC_SPIKES
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_StickyWeb::
	setvar VAR_0x8005, MOVE_STICKY_WEB
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_StoneAxe::
	setvar VAR_0x8005, MOVE_STONE_AXE
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_CeaselessEdge::
	setvar VAR_0x8005, MOVE_CEASELESS_EDGE
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_SaltCure::
	setvar VAR_0x8005, MOVE_SALT_CURE
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_LeechSeed::
	setvar VAR_0x8005, MOVE_LEECH_SEED
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_Toxic::
	setvar VAR_0x8005, MOVE_TOXIC
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_WillOWisp::
	setvar VAR_0x8005, MOVE_WILL_O_WISP
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_ThunderWave::
	setvar VAR_0x8005, MOVE_THUNDER_WAVE
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_Taunt::
	setvar VAR_0x8005, MOVE_TAUNT
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_Encore::
	setvar VAR_0x8005, MOVE_ENCORE
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_KnockOff::
	setvar VAR_0x8005, MOVE_KNOCK_OFF
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_Roar::
	setvar VAR_0x8005, MOVE_ROAR
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_Whirlwind::
	setvar VAR_0x8005, MOVE_WHIRLWIND
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_DragonTail::
	setvar VAR_0x8005, MOVE_DRAGON_TAIL
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_Infestation::
	setvar VAR_0x8005, MOVE_INFESTATION
	goto IndigoPlateau_EventScript_TutorTeachMove
	end

IndigoPlateau_EventScript_TutorTeach_RapidSpin::
	setvar VAR_0x8005, MOVE_RAPID_SPIN
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_Defog::
	setvar VAR_0x8005, MOVE_DEFOG
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_MortalSpin::
	setvar VAR_0x8005, MOVE_MORTAL_SPIN
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_TidyUp::
	setvar VAR_0x8005, MOVE_TIDY_UP
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_CourtChange::
	setvar VAR_0x8005, MOVE_COURT_CHANGE
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_Haze::
	setvar VAR_0x8005, MOVE_HAZE
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_ClearSmog::
	setvar VAR_0x8005, MOVE_CLEAR_SMOG
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_BrickBreak::
	setvar VAR_0x8005, MOVE_BRICK_BREAK
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_PsychicFangs::
	setvar VAR_0x8005, MOVE_PSYCHIC_FANGS
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_IceSpinner::
	setvar VAR_0x8005, MOVE_ICE_SPINNER
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_HealBell::
	setvar VAR_0x8005, MOVE_HEAL_BELL
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_Aromatherapy::
	setvar VAR_0x8005, MOVE_AROMATHERAPY
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_UTurn::
	setvar VAR_0x8005, MOVE_U_TURN
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_VoltSwitch::
	setvar VAR_0x8005, MOVE_VOLT_SWITCH
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_FlipTurn::
	setvar VAR_0x8005, MOVE_FLIP_TURN
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_PartingShot::
	setvar VAR_0x8005, MOVE_PARTING_SHOT
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_Snarl::
	setvar VAR_0x8005, MOVE_SNARL
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_IcyWind::
	setvar VAR_0x8005, MOVE_ICY_WIND
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_BreakingSwipe::
	setvar VAR_0x8005, MOVE_BREAKING_SWIPE
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_ChillingWater::
	setvar VAR_0x8005, MOVE_CHILLING_WATER
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_AcidSpray::
	setvar VAR_0x8005, MOVE_ACID_SPRAY
	goto IndigoPlateau_EventScript_TutorTeachMove
	end
IndigoPlateau_EventScript_TutorTeach_Nuzzle::
	setvar VAR_0x8005, MOVE_NUZZLE
	goto IndigoPlateau_EventScript_TutorTeachMove
	end

IndigoPlateau_EventScript_TutorTeachMove::
	buffermovename STR_VAR_1, VAR_0x8005
	msgbox IndigoPlateau_Text_TutorConfirm, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, IndigoPlateau_EventScript_TutorDecline
	msgbox IndigoPlateau_Text_TutorWhichMon, MSGBOX_DEFAULT
	fadescreen FADE_TO_BLACK
	chooseboxmon SELECT_PC_MON_MOVE_TUTOR
	waitstate
	goto_if_eq VAR_RESULT, FALSE, IndigoPlateau_EventScript_TutorCancelled
	msgbox IndigoPlateau_Text_TutorDone, MSGBOX_DEFAULT
	release
	end

IndigoPlateau_EventScript_TutorCancelled::
	msgbox IndigoPlateau_Text_TutorComeBack, MSGBOX_DEFAULT
	release
	end

IndigoPlateau_EventScript_TutorDecline::
	msgbox IndigoPlateau_Text_TutorComeBack, MSGBOX_DEFAULT
	release
	end

IndigoPlateau_Text_HazardTutorIntro:
	.string "I teach battlefield control.\p"
	.string "Hazards, traps, status and phazing.\n"
	.string "No fee. Which move do you want?$"

IndigoPlateau_Text_CleanupTutorIntro:
	.string "I teach cleanup and utility.\p"
	.string "Clear hazards, screens and status,\n"
	.string "then seize momentum. Pick a move.$"

IndigoPlateau_Text_TutorConfirm:
	.string "Teach {STR_VAR_1}?$"

IndigoPlateau_Text_TutorWhichMon:
	.string "Which POKEMON should learn it?$"

IndigoPlateau_Text_TutorDone:
	.string "Done. Use it well.$"

IndigoPlateau_Text_TutorComeBack:
	.string "No problem. Come back anytime.$"

IndigoPlateau_Text_TutorMove_StealthRock:
	.string "STEALTH ROCK$"
IndigoPlateau_Text_TutorMove_Spikes:
	.string "SPIKES$"
IndigoPlateau_Text_TutorMove_ToxicSpikes:
	.string "TOXIC SPIKES$"
IndigoPlateau_Text_TutorMove_StickyWeb:
	.string "STICKY WEB$"
IndigoPlateau_Text_TutorMove_StoneAxe:
	.string "STONE AXE$"
IndigoPlateau_Text_TutorMove_CeaselessEdge:
	.string "CEASELESS EDGE$"
IndigoPlateau_Text_TutorMove_SaltCure:
	.string "SALT CURE$"
IndigoPlateau_Text_TutorMove_LeechSeed:
	.string "LEECH SEED$"
IndigoPlateau_Text_TutorMove_Toxic:
	.string "TOXIC$"
IndigoPlateau_Text_TutorMove_WillOWisp:
	.string "WILL-O-WISP$"
IndigoPlateau_Text_TutorMove_ThunderWave:
	.string "THUNDER WAVE$"
IndigoPlateau_Text_TutorMove_Taunt:
	.string "TAUNT$"
IndigoPlateau_Text_TutorMove_Encore:
	.string "ENCORE$"
IndigoPlateau_Text_TutorMove_KnockOff:
	.string "KNOCK OFF$"
IndigoPlateau_Text_TutorMove_Roar:
	.string "ROAR$"
IndigoPlateau_Text_TutorMove_Whirlwind:
	.string "WHIRLWIND$"
IndigoPlateau_Text_TutorMove_DragonTail:
	.string "DRAGON TAIL$"
IndigoPlateau_Text_TutorMove_Infestation:
	.string "INFESTATION$"
IndigoPlateau_Text_TutorMove_RapidSpin:
	.string "RAPID SPIN$"
IndigoPlateau_Text_TutorMove_Defog:
	.string "DEFOG$"
IndigoPlateau_Text_TutorMove_MortalSpin:
	.string "MORTAL SPIN$"
IndigoPlateau_Text_TutorMove_TidyUp:
	.string "TIDY UP$"
IndigoPlateau_Text_TutorMove_CourtChange:
	.string "COURT CHANGE$"
IndigoPlateau_Text_TutorMove_Haze:
	.string "HAZE$"
IndigoPlateau_Text_TutorMove_ClearSmog:
	.string "CLEAR SMOG$"
IndigoPlateau_Text_TutorMove_BrickBreak:
	.string "BRICK BREAK$"
IndigoPlateau_Text_TutorMove_PsychicFangs:
	.string "PSYCHIC FANGS$"
IndigoPlateau_Text_TutorMove_IceSpinner:
	.string "ICE SPINNER$"
IndigoPlateau_Text_TutorMove_HealBell:
	.string "HEAL BELL$"
IndigoPlateau_Text_TutorMove_Aromatherapy:
	.string "AROMATHERAPY$"
IndigoPlateau_Text_TutorMove_UTurn:
	.string "U-TURN$"
IndigoPlateau_Text_TutorMove_VoltSwitch:
	.string "VOLT SWITCH$"
IndigoPlateau_Text_TutorMove_FlipTurn:
	.string "FLIP TURN$"
IndigoPlateau_Text_TutorMove_PartingShot:
	.string "PARTING SHOT$"
IndigoPlateau_Text_TutorMove_Snarl:
	.string "SNARL$"
IndigoPlateau_Text_TutorMove_IcyWind:
	.string "ICY WIND$"
IndigoPlateau_Text_TutorMove_BreakingSwipe:
	.string "BREAKING SWIPE$"
IndigoPlateau_Text_TutorMove_ChillingWater:
	.string "CHILLING WATER$"
IndigoPlateau_Text_TutorMove_AcidSpray:
	.string "ACID SPRAY$"
IndigoPlateau_Text_TutorMove_Nuzzle:
	.string "NUZZLE$"
IndigoPlateau_Text_TutorMove_Cancel:
	.string "CANCEL$"
