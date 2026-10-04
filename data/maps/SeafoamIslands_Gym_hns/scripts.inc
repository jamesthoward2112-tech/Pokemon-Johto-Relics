SeafoamIslands_Gym_hns_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SeafoamIslands_Gym_OnTransition
	.byte 0

SeafoamIslands_Gym_OnTransition:
	setflag FLAG_TEMP_1
	clearflag FLAG_HIDE_SEAFOAM_GYMGUY
	goto_if_set FLAG_DEFEATED_CINNABAR_ISLAND_GYM, SeafoamIslands_Gym_OnTransition_Defeated
	setflag FLAG_HIDE_SEAFOAM_BLAINE
	end

SeafoamIslands_Gym_OnTransition_Defeated:
	clearflag FLAG_HIDE_SEAFOAM_BLAINE
	end

SeafoamIslands_Gym_EventScript_Blaine::
	lock
	faceplayer
	goto_if_set FLAG_DEFEATED_CINNABAR_ISLAND_GYM, SeafoamIslands_Gym_EventScript_Blaine_Defeated
	msgbox SeafoamIslands_Gym_Text_BlaineIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_BLAINE_HNS, SeafoamIslands_Gym_Text_BlaineWinLoss
	message SeafoamIslands_Gym_Text_ReceivedVolcanoBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox SeafoamIslands_Gym_Text_Blaine_GiveTM, MSGBOX_DEFAULT
	giveitem ITEM_TM_OVERHEAT
	msgbox SeafoamIslands_Gym_Text_Blaine_ExplainTM, MSGBOX_DEFAULT
	setflag FLAG_BADGE15_GET
	setflag FLAG_DEFEATED_CINNABAR_ISLAND_GYM
	addvar VAR_NUM_BADGES, 1
	setvar VAR_0x8008, 15
	clearflag FLAG_HIDE_SEAFOAM_BLAINE
	clearflag FLAG_HIDE_SEAFOAM_GYMGUY
	call Common_EventScript_SetGymTrainers_hns
	msgbox SeafoamIslands_Gym_Text_BlaineOpenPassage, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_SEAFOAM_BLAINE, SeafoamIslands_Gym_Movement_BlaineStepAside
	waitmovement 0
	release
	end

SeafoamIslands_Gym_Movement_BlaineStepAside:
	walk_left
	face_down
	step_end

SeafoamIslands_Gym_EventScript_Blaine_Defeated::
	msgbox SeafoamIslands_Gym_Text_BlaineAfterBattle, MSGBOX_DEFAULT
	closemessage
	release
	end

SeafomIslands2_EventScript_GymGuide::
	goto_if_unset FLAG_DEFEATED_CINNABAR_ISLAND_GYM, SeafomIslands2_EventScript_GymGuideBefore
	goto_if_set FLAG_TEMP_2, SeafomIslands2_EventScript_GymGuide2
	msgbox SeafoamIslands_Gym_Text_GymGuideWin, MSGBOX_NPC
	setflag FLAG_TEMP_2
	end

SeafomIslands2_EventScript_GymGuideBefore::
	msgbox SeafoamIslands_Gym_Text_GymGuideBefore, MSGBOX_NPC
	end

SeafomIslands2_EventScript_GymGuide2::
	msgbox SeafoamIslands_Gym_Text_GymGuideWin2, MSGBOX_NPC
	end

SeafoamIslands_Gym_EventScript_GymStatue::
	lockall
	goto_if_set FLAG_BADGE15_GET, SeafoamIslands_Gym_EventScript_GymStatuePostVictory
	msgbox SeafoamIslands_Gym_Text_GymStatue
	releaseall
	end

SeafoamIslands_Gym_EventScript_GymStatuePostVictory::
	msgbox SeafoamIslands_Gym_Text_GymStatuePlayerWon
	releaseall
	end

SeafoamIslands_Gym_Text_GymStatue::
    .string "CINNABAR POKéMON GYM\n"
    .string "LEADER: BLAINE\p"
	.string "WINNING TRAINERS:\n"
	.string "BLUE, RED$"

SeafoamIslands_Gym_Text_GymStatuePlayerWon::
    .string "CINNABAR POKéMON GYM\n"
    .string "LEADER: BLAINE\p"
    .string "WINNING TRAINERS:\n"
	.string "BLUE, RED, {PLAYER}$"

SeafoamIslands_Gym_Text_Blaine_GiveTM:
	.string "Take this too!$"

SeafoamIslands_Gym_Text_Blaine_ExplainTM:
	.string "This TM contains\n"
	.string "the awesome OVERHEAT!\p"
	.string "The overwhelming heat scorches your\n"
	.string "opponents, but then drops your power.\p"
	.string "I hope your next opponent has an\n"
	.string "extra BURN HEAL! Waaah!$"

SeafoamIslands_Gym_Text_BlaineIntro:
	.string "BLAINE: Waaah!\p"
	.string "My GYM in CINNABAR burned down.\p"
	.string "My fire-breathing POKéMON and I are\n"
	.string "homeless because of the volcano.\p"
	.string "Waaah!\p"
	.string "But I'm back in business as a GYM\n"
	.string "LEADER here in this cave.\p"
	.string "If you can beat me, I'll give you\n"
	.string "a BADGE.\p"
	.string "Ha! You'd better have BURN HEAL!$"

SeafoamIslands_Gym_Text_BlaineWinLoss:
	.string "BLAINE: Awesome. I've burned out…\p"
	.string "You've earned VOLCANOBADGE!$"

SeafoamIslands_Gym_Text_ReceivedVolcanoBadge:
	.string "{PLAYER} received VOLCANOBADGE.$"

SeafoamIslands_Gym_Text_BlaineOpenPassage:
	.string "BLAINE: You've earned more than a\n"
	.string "BADGE today.\p"
	.string "There's a strange heat coming from\n"
	.string "the passage behind me.\p"
	.string "It isn't from my POKéMON.\p"
	.string "Go on--take a look for yourself!$"

SeafoamIslands_Gym_Text_BlaineAfterBattle:
	.string "BLAINE: That passage behind the\n"
	.string "platform is open to you now.\p"
	.string "Whatever is creating that heat,\n"
	.string "you've earned the right to face it.$"

SeafoamIslands_Gym_Text_BlaineFightDone:
	.string "BLAINE: My fire POKéMON will be\n"
	.string "even stronger.\p"
	.string "Just you watch!$"

SeafoamIslands_Gym_Text_BlaineRematch:
	.string "BLAINE: Whoa!\p"
	.string "I see you've become the KANTO\n"
	.string "CHAMPION!\p"
	.string "That's blazing!\p"
	.string "Your skills are top-notch.\p"
	.string "I'm always up for a battle.\p"
	.string "Want to have a rematch with me?$"

SeafoamIslands_Gym_Text_BlaineRematchDefeat:
	.string "BLAINE: Your skills are truly fiery!\p"
	.string "You've burned right through my\n"
	.string "defenses.$"

SeafoamIslands_Gym_Text_GymGuideBefore:
	.string "Yo, CHAMP in making!\p"
	.string "BLAINE lost his old CINNABAR GYM,\n"
	.string "so he's set up here in SEAFOAM.\p"
	.string "He's waiting on the platform ahead.\n"
	.string "Bring something that can take HEAT!$"

SeafoamIslands_Gym_Text_GymGuideWin:
	.string "Yo, CHAMP! Now THAT was a battle!\p"
	.string "BLAINE's stepped aside, and the\n"
	.string "passage behind him is open.\p"
	.string "Something powerful is stirring deeper\n"
	.string "in the cave. I'd go take a look!$"

SeafoamIslands_Gym_Text_GymGuideWin2:
	.string "BLAINE may not have a building, but\n"
	.string "SEAFOAM is his GYM now.\p"
	.string "And you definitely earned that\n"
	.string "VOLCANOBADGE.$"
