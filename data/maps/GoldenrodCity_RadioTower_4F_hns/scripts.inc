GoldenrodCity_RadioTower_4F_hns_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesTransition
	map_script MAP_SCRIPT_ON_LOAD, GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesLoad
	.byte 0

// Reset the coordinate-trigger gate on every visit without clearing wins.
GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesTransition::
	// The trio exists only during their staircase ambush; never idle in view.
	setflag FLAG_TEMP_1
	setvar VAR_TEMP_3, 1
	call_if_unset FLAG_PJR_JESSIE_JAMES_3_DEFEATED, GoldenrodCity_RadioTower_4F4_EventScript_ArmJessieJames
	end

GoldenrodCity_RadioTower_4F4_EventScript_ArmJessieJames::
	setvar VAR_TEMP_3, 0
	return

GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesLoad::
	call_if_unset FLAG_PJR_JESSIE_JAMES_3_DEFEATED, GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesLoad_ResetTrainer
	end

GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesLoad_ResetTrainer::
	cleartrainerflag TRAINER_GRUNT_9_HNS
	return

GoldenrodCity_RadioTower_4F4_EventScript_Sign1::
	lock
	msgbox GoldenrodCity_RadioTower_4F4_Text_Studio2Sign, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodCity_RadioTower_4F4_EventScript_Sign2::
	lock
	msgbox GoldenrodCity_RadioTower_4F4_Text_ProductionSign, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodCity_RadioTower_4F4_EventScript_FaceJessieJames::
	applymovement 2, Common_Movement_FacePlayer
	applymovement 5, Common_Movement_FacePlayer
	applymovement 7, Common_Movement_FacePlayer
	waitmovementall
	return

// The three Rocket actors are hidden at (14,11), (15,11), (16,11)
// outside the left stair camera on entry.  Stepping off the 3F stair
// at (9,5) into the 4F triggers this scene automatically.  No A press
// or trainer vision is required, and player movement is locked throughout.
// Route: run north through the open central aisle, then fan out across
// the hallway to block the exit.  None of the destinations is a trigger tile.
GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesTrigger::
	goto_if_set FLAG_PJR_JESSIE_JAMES_3_DEFEATED, GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesAlreadyDefeated
	lockall
	setvar VAR_TEMP_3, 1
	clearflag FLAG_TEMP_1
	addobject 5
	addobject 2
	addobject 7
	applymovement 5, GoldenrodCity_RadioTower_4F4_Movement_RushNorth
	applymovement 2, GoldenrodCity_RadioTower_4F4_Movement_RushNorth
	applymovement 7, GoldenrodCity_RadioTower_4F4_Movement_RushNorth
	waitmovementall
	// Crossing actors are ordered from left to right to avoid collision.
	applymovement 5, GoldenrodCity_RadioTower_4F4_Movement_RushWest
	waitmovement 5
	applymovement 2, GoldenrodCity_RadioTower_4F4_Movement_RushWest
	waitmovement 2
	applymovement 7, GoldenrodCity_RadioTower_4F4_Movement_RushWest
	waitmovement 7
	call GoldenrodCity_RadioTower_4F4_EventScript_FaceJessieJames
	releaseall
	setvar VAR_LAST_TALKED, 2
	goto GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesBattle

// Both Jessie and James must share one battle/cleanup path.
GoldenrodRaidoTower4_EventScript_Grunt28::
	setvar VAR_TEMP_3, 1
	setvar VAR_LAST_TALKED, 2
	goto GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesBattle

GoldenrodRaidoTower4_EventScript_Grunt9::
	setvar VAR_TEMP_3, 1
	setvar VAR_LAST_TALKED, 2
	goto GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesBattle

GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesBattle::
	call GoldenrodCity_RadioTower_4F4_EventScript_FaceJessieJames
	trainerbattle_double TRAINER_GRUNT_9_HNS, GoldenrodCity_RadioTower_4F4_Text_JessieJamesSeen, GoldenrodCity_RadioTower_4F4_Text_JessieJamesBeaten, GoldenrodCity_RadioTower_4F4_Text_JessieJamesNeedTwo, GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesAfterBattle
	goto GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesAfterBattle

GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesAfterBattle::
	lockall
	msgbox GoldenrodCity_RadioTower_4F4_Text_JessieJamesAfter, MSGBOX_DEFAULT
	closemessage
	// Actual on-screen retreat: clear the centre aisle in the opposite
	// order of the ambush, sprint away and vanish only once out of view.
	// No fade to black, backward shuffle or teleport from the player.
	applymovement 7, GoldenrodCity_RadioTower_4F4_Movement_EscapeEast
	waitmovement 7
	applymovement 2, GoldenrodCity_RadioTower_4F4_Movement_EscapeEast
	waitmovement 2
	applymovement 5, GoldenrodCity_RadioTower_4F4_Movement_EscapeEast
	waitmovement 5
	applymovement 7, GoldenrodCity_RadioTower_4F4_Movement_EscapeSouth
	applymovement 2, GoldenrodCity_RadioTower_4F4_Movement_EscapeSouth
	applymovement 5, GoldenrodCity_RadioTower_4F4_Movement_EscapeSouth
	waitmovementall
	setflag FLAG_PJR_JESSIE_JAMES_3_DEFEATED
	setflag FLAG_TEMP_1
	removeobject 2
	removeobject 5
	removeobject 7
	setvar VAR_TEMP_3, 1
	releaseall
	end

GoldenrodCity_RadioTower_4F4_EventScript_JessieJamesAlreadyDefeated::
	setvar VAR_TEMP_3, 1
	end

GoldenrodCity_RadioTower_4F4_Movement_RushNorth:
	walk_faster_up
	walk_faster_up
	walk_faster_up
	walk_faster_up
	step_end

GoldenrodCity_RadioTower_4F4_Movement_RushWest:
	walk_faster_left
	walk_faster_left
	walk_faster_left
	step_end

GoldenrodCity_RadioTower_4F4_Movement_EscapeEast:
	walk_faster_right
	walk_faster_right
	walk_faster_right
	step_end

GoldenrodCity_RadioTower_4F4_Movement_EscapeSouth:
	walk_faster_down
	walk_faster_down
	walk_faster_down
	walk_faster_down
	step_end

GoldenrodRaidoTower4_EventScript_Proton::
	trainerbattle_single TRAINER_PROTON_2_HNS, GoldenrodCity_RadioTower_4F4_Text_Proton_Seen, GoldenrodCity_RadioTower_4F4_Text_Proton_Beaten
	msgbox GoldenrodCity_RadioTower_4F4_Text_Proton_After, MSGBOX_AUTOCLOSE
	end


GoldenrodCity_RadioTower_4F4_EventScript_Fisher::
	lock
	faceplayer
	msgbox GoldenrodCity_RadioTower_4F4_Text_Fisher, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_RadioTower_4F4_EventScript_Scientist::
	trainerbattle_single TRAINER_RICH_HNS, GoldenrodCity_RadioTower_4F4_Text_ScientistRichSeen, GoldenrodCity_RadioTower_4F4_Text_ScientistRichBeaten
	msgbox GoldenrodCity_RadioTower_4F4_Text_ScientistRichAfter, MSGBOX_AUTOCLOSE
	end


GoldenrodCity_RadioTower_4F4_EventScript_Mary::
	lock
	faceplayer
	goto_if_eq VAR_GOLDENROD_CITY_STATE, 6, GoldenrodCity_RadioTower_4F4_EventScript_Mary2
	goto_if_eq VAR_GOLDENROD_CITY_STATE, 7, GoldenrodCity_RadioTower_4F4_EventScript_Mary2
	goto_if_eq VAR_GOLDENROD_CITY_STATE, 8, GoldenrodCity_RadioTower_4F4_EventScript_Mary2
	goto_if_eq VAR_GOLDENROD_CITY_STATE, 9, GoldenrodCity_RadioTower_4F4_EventScript_Mary2
	goto_if_unset FLAG_GOT_MARY_BRIGHT_POWDER, GoldenrodCity_RadioTower_4F4_EventScript_Mary3
	msgbox GoldenrodCity_RadioTower_4F4_Text_DJMaryAfter, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_RadioTower_4F4_EventScript_Mary2::
	msgbox GoldenrodCity_RadioTower_4F4_Text_DJMary, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_RadioTower_4F4_EventScript_Mary3::
	msgbox GoldenrodCity_RadioTower_4F4_Text_DJMaryCleared, MSGBOX_DEFAULT
	closemessage
	giveitem ITEM_BRIGHT_POWDER
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_BagIsFull
	msgbox GoldenrodCity_RadioTower_4F4_Text_DJMaryPinkBow, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_GOT_MARY_BRIGHT_POWDER
	closemessage
	release
	end

GoldenrodCity_RadioTower_4F4_EventScript_Meowth::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MEOWTH, CRY_MODE_NORMAL
	msgbox GoldenrodCity_RadioTower_4F4_Text_Meowth, MSGBOX_DEFAULT
	waitmoncry
	release
	end


GoldenrodCity_RadioTower_4F4_Text_Proton_Seen:
	.string "PROTON: Now wait just one second!\p"
	.string "Aren't you the one who got in our\n"
	.string "way at SLOWPOKE WELL?\p"
	.string "I see... You're doing all this\n"
	.string "because you want to make me angry.\l"
	.string "Be careful!\p"
	.string "But since you seem to wish it, I'll\n"
	.string "show you the full extent of a TEAM\l"
	.string "ROCKET EXECUTIVE's wrath!$"

GoldenrodCity_RadioTower_4F4_Text_Proton_Beaten:
	.string "Phew...$"

GoldenrodCity_RadioTower_4F4_Text_Proton_After:
	.string "PROTON: You may have won this\n"
	.string "time... But all you did was make\p"
	.string "TEAM ROCKET's wrath grow.$"

GoldenrodCity_RadioTower_4F4_Text_Fisher:
	.string "I listened to the radio while I was\n"
	.string "at the RUINS.\p"
	.string "I heard a strange broadcast there.$"

GoldenrodCity_RadioTower_4F4_Text_DJMary:
	.string "MARY: Why? Why do I have to suffer\n"
	.string "through this?\p"
	.string "MEOWTH, help me!$"

GoldenrodCity_RadioTower_4F4_Text_DJMaryCleared:
	.string "MARY: Oh! You're my little savior!\p"
	.string "Will you take this as my thanks?$"

GoldenrodCity_RadioTower_4F4_Text_DJMaryPinkBow:
	.string "MARY: It's good for dodging the\n"
	.string "enemy's attacks.$"

GoldenrodCity_RadioTower_4F4_Text_DJMaryAfter:
	.string "MARY: Please tune into me on PROF.\n"
	.string "OAK'S POKéMON TALK show!$"

GoldenrodCity_RadioTower_4F4_Text_Meowth:
	.string "MEOWTH: Meowth…$"

GoldenrodCity_RadioTower_4F4_Text_GruntM10Seen:
	.string "You plan to rescue the DIRECTOR?\p"
	.string "That won't be possible because I'm\n"
	.string "going to beat you!$"

GoldenrodCity_RadioTower_4F4_Text_GruntM10Beaten:
	.string "No! Unbelievable!$"

GoldenrodCity_RadioTower_4F4_Text_GruntM10After:
	.string "I don't believe it! I was beaten!$"

GoldenrodCity_RadioTower_4F4_Text_ExecutiveM2Seen:
	.string "Stop! I'm known as the TEAM ROCKET\n"
	.string "fortress!\p"
	.string "You're not taking another step!$"

GoldenrodCity_RadioTower_4F4_Text_ExecutiveM2Beaten:
	.string "The fortress came down!$"

GoldenrodCity_RadioTower_4F4_Text_ExecutiveM2After:
	.string "You've earned my respect, so here's\n"
	.string "some advice.\p"
	.string "It's not too late. You can still turn\n"
	.string "back.$"

GoldenrodCity_RadioTower_4F4_Text_GruntF4Seen:
	.string "Don't I think POKéMON are cute?\p"
	.string "I'll think my POKéMON are cute--\p"
	.string "after they beat yours!$"

GoldenrodCity_RadioTower_4F4_Text_GruntF4Beaten:
	.string "Oh, no! They're so useless!$"

GoldenrodCity_RadioTower_4F4_Text_GruntF4After:
	.string "I love my beautiful self!\p"
	.string "Who cares about POKéMON?$"

GoldenrodCity_RadioTower_4F4_Text_ScientistRichSeen:
	.string "Most excellent.\p"
	.string "This RADIO TOWER will fulfill our\n"
	.string "grand design.$"

GoldenrodCity_RadioTower_4F4_Text_ScientistRichBeaten:
	.string "Hmmm…\p"
	.string "All grand plans come with snags.$"

GoldenrodCity_RadioTower_4F4_Text_ScientistRichAfter:
	.string "Do you honestly believe you can stop\n"
	.string "TEAM ROCKET?$"

GoldenrodCity_RadioTower_4F4_Text_ProductionSign:
	.string "4F PRODUCTION$"

GoldenrodCity_RadioTower_4F4_Text_Studio2Sign:
	.string "4F STUDIO 2$"

GoldenrodCity_RadioTower_4F4_Text_JessieJamesSeen:
	.string "JESSIE: This tower belongs to\n"
	.string "TEAM ROCKET!\p"
	.string "JAMES: And we're guarding it\n"
	.string "together!$"

GoldenrodCity_RadioTower_4F4_Text_JessieJamesBeaten:
	.string "JESSIE & JAMES: Not again!$"

GoldenrodCity_RadioTower_4F4_Text_JessieJamesAfter:
	.string "JESSIE: Keep moving, twerp.\p"
	.string "JAMES: We'll meet again!$"

GoldenrodCity_RadioTower_4F4_Text_JessieJamesNeedTwo:
	.string "Bring at least two {PKMN} if you\n"
	.string "want to face both of us!$"
