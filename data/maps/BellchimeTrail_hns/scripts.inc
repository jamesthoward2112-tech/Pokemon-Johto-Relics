BellchimeTrail_hns_MapScripts::
	.byte 0


BellchimeTrail_EventScript_Morty::
	lock
	faceplayer
	msgbox BellchimeTrail_Text_Morty, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	setflag FLAG_HIDE_BELLCHIME_MORTY
	removeobject LOCALID_BELLCHIME_MORTY
	fadescreenswapbuffers FADE_FROM_BLACK
	clearflag FLAG_HIDE_DOJO_MORTY
	release
	end

BellchimeTrail_Text_Morty:
	.string "MORTY: The legendary POKéMON\n"
	.string "did not choose me...\p"
	.string "But that does not mean that I\n"
	.string "have lost out on my future.\p"
	.string "I will continue my training until I\n"
	.string "I discover a new future for me.\p"
	.string "If you seek another battle, find\n"
	.string "me at the FIGHTING DOJO.$"

EcruteakBellchimeTrail_EventScript_Item_BigMushroom::
	finditem ITEM_BIG_MUSHROOM
	end

EcruteakBellchimeTrail_EventScript_DoorTrigger::
	lock
	opendoor 28, 12
	waitdooranim
	addobject OBJ_EVENT_ID_CAMERA
	removeobject OBJ_EVENT_ID_PLAYER
	closedoor 28, 12
	applymovement OBJ_EVENT_ID_CAMERA, EcruteakBellchimeTrail_Movement_CameraPanUp
	waitmovement 0
	warp MAP_TIN_TOWER_1F_HNS, 1
	release
	end

EcruteakBellchimeTrail_Movement_CameraPanUp::
	slide_up
	slide_up
	slide_up
	slide_up
	slide_up
	slide_up
	slide_up
	step_end


EcruteakBellchimeTrail_EventScript_RelicShortcut::
	goto_if_unset FLAG_PJR_GOT_RAINBOW_CREST, EcruteakBellchimeTrail_Text_RelicShortcutDormant
	goto_if_unset FLAG_PJR_RELIC_ALPHORACLE, EcruteakBellchimeTrail_Text_RelicShortcutDormant
	msgbox EcruteakBellchimeTrail_Text_RelicShortcutReady, MSGBOX_DEFAULT
	warp MAP_TIN_TOWER_8F_HNS, 6, 12
	waitstate
	end

EcruteakBellchimeTrail_Text_RelicShortcutDormant:
	msgbox EcruteakBellchimeTrail_Text_RelicShortcutDormantMsg, MSGBOX_DEFAULT
	end

EcruteakBellchimeTrail_Text_RelicShortcutReady:
	.string "The ANCIENT RAINBOW CREST glows.\p"
	.string "A hidden passage opens toward the\n"
	.string "highest floor of TIN TOWER.$"

EcruteakBellchimeTrail_Text_RelicShortcutDormantMsg:
	.string "TIN TOWER\n"
	.string "A sacred tower watched by HO-OH.$"
