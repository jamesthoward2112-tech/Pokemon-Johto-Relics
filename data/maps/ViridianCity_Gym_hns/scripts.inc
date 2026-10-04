ViridianCity_Gym_hns_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, ViridianCity_Gym_OnTransition
	.byte 0

@ Repair old saves where the Dojo invitation left a second Blue in the gym.
ViridianCity_Gym_OnTransition::
	goto_if_unset FLAG_DEFEATED_VIRIDIAN_GYM, ViridianCity_Gym_BlueNotDefeated
	setflag FLAG_HIDE_CINNABAR_BLUE
	goto_if_set FLAG_HIDE_DOJO_BLUE, ViridianCity_Gym_OnTransition_End
	setflag FLAG_HIDE_VIRIDIAN_BLUE
ViridianCity_Gym_OnTransition_End::
	end

ViridianCity_Gym_BlueNotDefeated::
	setflag FLAG_HIDE_DOJO_BLUE
	end

ViridianCity_Gym_EventScript_Blue::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_VIRIDIAN_GYM, ViridianCity_Gym_EventScript_BlueGotoDojo
	msgbox ViridianCity_Gym_Text_LeaderBlue_Before, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_BLUE_HNS, ViridianCity_Gym_Text_LeaderBlue_Win
	message ViridianCity_Gym_Text_ReceivedEarthBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox ViridianCity_Gym_Text_LeaderBlue_After, MSGBOX_DEFAULT
	msgbox ViridianCity_Gym_Text_LeaderBlue_GiveTM, MSGBOX_DEFAULT
	giveitem ITEM_TM_TRICK_ROOM
	msgbox ViridianCity_Gym_Text_LeaderBlue_ExplainTM, MSGBOX_DEFAULT
	setflag FLAG_BADGE16_GET
	setflag FLAG_DEFEATED_VIRIDIAN_GYM
	setflag FLAG_HIDE_CINNABAR_BLUE
	addvar VAR_NUM_BADGES, 1
	setvar VAR_0x8008, 16
	call Common_EventScript_SetGymTrainers_hns
	closemessage
	setflag FLAG_HIDE_LEAGUE_BLACKBELT
	clearflag FLAG_HIDE_CINNABAR_BLAINE
	setvar VAR_OAK_MT_SILVER_CALL, 1
	release
	end

ViridianCity_Gym_EventScript_BlueGotoDojo::
	msgbox ViridianCity_Gym_Text_BlueGotoDojo, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	setflag FLAG_HIDE_VIRIDIAN_BLUE
	setflag FLAG_HIDE_CINNABAR_BLUE
	clearflag FLAG_HIDE_DOJO_BLUE
	removeobject LOCALID_VIRIDIAN_BLUE
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

ViridianCity_Gym_Text_BlueGotoDojo:
	.string "BLUE: Ready for a rematch?\p"
	.string "Meet me at the FIGHTING DOJO\n"
	.string "in SAFFRON CITY!$"

ViridianCity_Gym_Text_LeaderBlue_Before:
	.string "BLUE: Yo! Finally got here, huh?\p"
	.string "I wasn't in the mood at CINNABAR,\p"
	.string "but now I'm ready to battle you.\p"
	.string "…\p"
	.string "You're telling me you conquered all\n"
	.string "the GYMS in JOHTO?\p"
	.string "Heh! JOHTO's GYMS must be pretty\n"
	.string "pathetic then.\p"
	.string "Hey, don't worry about it.\p"
	.string "I'll know if you are good or not by\n"
	.string "battling you right now.\p"
	.string "Ready, JOHTO CHAMP?$"

ViridianCity_Gym_Text_LeaderBlue_Win:
	.string "BLUE: What?\p"
	.string "How the heck did I lose to you?\p"
	.string "…\p"
	.string "Tch, all right… Here, take this--it's\n"
	.string "EARTHBADGE.$"

ViridianCity_Gym_Text_ReceivedEarthBadge:
	.string "{PLAYER} received EARTHBADGE.$"

ViridianCity_Gym_Text_LeaderBlue_After:
	.string "BLUE: …\p"
	.string "All right, I was wrong. You're the\n"
	.string "real deal. You are a good trainer.\p"
	.string "But I'm going to beat you someday.\p"
	.string "Don't you forget it!$"

ViridianCity_Gym_Text_LeaderBlue_GiveTM:
	.string "Take this with you.$"

ViridianCity_Gym_Text_LeaderBlue_ExplainTM:
	.string "That's TRICK ROOM.\p"
	.string "All POKEMON in battle will change speed.\n"
	.string "Slow goes first. Fast goes last.\p"
	.string "Use it to turn a battle on its head.$"

ViridianCity_Gym_Text_LeaderBlue_Epilogue:
	.string "BLUE: Listen, you.\p"
	.string "You'd better not lose until I beat\n"
	.string "you. Got it?$"


ViridianCity_Gym_EventScript_GymGuy::
	goto_if_set FLAG_DEFEATED_VIRIDIAN_GYM, ViridianCity_Gym_EventScript_GymGuyAfter
	msgbox ViridianCity_Gym_Text_Guide, MSGBOX_NPC
	end

ViridianCity_Gym_EventScript_GymGuyAfter::
	msgbox ViridianCity_Gym_Text_Guide_Win, MSGBOX_NPC
	end

ViridianCity_Gym_Text_Guide:
	.string "Yo, CHAMP in making!\p"
	.string "How's it going? Looks like you're on\n"
	.string "a roll.\p"
	.string "The GYM LEADER is a guy who battled\n"
	.string "the CHAMPION three years ago.\p"
	.string "He's no pushover.\p"
	.string "Give it everything you've got!$"

ViridianCity_Gym_Text_Guide_Win:
	.string "Man, you are truly tough…\p"
	.string "That was a heck of an inspirational\n"
	.string "battle. It brought tears to my eyes.$"


ViridianCity_Gym_EventScript_GymStatue::
	lockall
	goto_if_set FLAG_BADGE16_GET, ViridianCity_Gym_EventScript_GymStatuePostVictory
	msgbox ViridianCity_Gym_Text_GymStatue
	releaseall
	end

ViridianCity_Gym_EventScript_GymStatuePostVictory::
	msgbox ViridianCity_Gym_Text_GymStatuePlayerWon
	releaseall
	end

ViridianCity_Gym_Text_GymStatue::
    .string "VIRIDIAN POKéMON GYM\n"
    .string "LEADER: BLUE\p"
	.string "WINNING TRAINERS:\n"
	.string "BLUE, RED$"

ViridianCity_Gym_Text_GymStatuePlayerWon::
    .string "VIRIDIAN POKéMON GYM\n"
    .string "LEADER: BLUE\p"
    .string "WINNING TRAINERS:\n"
	.string "BLUE, RED, {PLAYER}$"

