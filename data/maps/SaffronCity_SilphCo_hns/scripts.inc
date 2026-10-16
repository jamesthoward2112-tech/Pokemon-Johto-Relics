SaffronCity_SilphCo_hns_MapScripts::
	.byte 0

SaffronCity_SilphCo_EventScript_Steven::
	lock
	msgbox SaffronCity_SilphCo_Text_Steven1, MSGBOX_DEFAULT
	closemessage
	delay 20
	faceplayer
	delay 20
	playse SE_PIN
	applymovement LOCALID_SILPHCO_STEVEN, Common_Movement_ExclamationMark
	delay 55
	waitmovement LOCALID_SILPHCO_STEVEN
	msgbox SaffronCity_SilphCo_Text_Steven2, MSGBOX_DEFAULT
	closemessage
	call_if_eq VAR_FACING, DIR_NORTH, SaffronCity_SilphCo_EventScript_PlayerMove
	applymovement LOCALID_SILPHCO_STEVEN, SaffronCity_SilphCo_Movement_StevenLeave
	waitmovement 0
	playse SE_EXIT
	@ PRU: legacy FLAG_GOT_HOENN_STARTER hides this one-time Steven scene.
	@ It now records a research meeting, never a free starter gift.
	setflag FLAG_GOT_HOENN_STARTER
	removeobject LOCALID_SILPHCO_STEVEN
	release
	end

SaffronCity_SilphCo_EventScript_PlayerMove:
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_WalkRight1
	waitmovement 0
	turnobject OBJ_EVENT_ID_PLAYER, DIR_WEST
	return

SaffronCity_SilphCo_Movement_StevenLeave:
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end


SaffronCity_SilphCo_Text_Steven1:
	.string "STEVEN: ELM? It's STEVEN.\p"
	.string "Those strange ALPH readings\n"
	.string "match traces found in HOENN.\p"
	.string "I'll send my notes to OAK.$"

SaffronCity_SilphCo_Text_Steven2:
	.string "STEVEN: Oh! You're {PLAYER}!\p"
	.string "ELM told me about your work\n"
	.string "with ancient RESONANCE.\p"
	.string "Some unusual partners can be\n"
	.string "found quite early in JOHTO.\p"
	.string "TREECKO live on ROUTE 30.\n"
	.string "TORCHIC roam ROUTE 33.\p"
	.string "MUDKIP can be found deep\n"
	.string "inside UNION CAVE.\p"
	.string "Study how they grow. Their\n"
	.string "evolutions may surprise us!$"

SaffronCity_SilphCo_EventScript_Receptionist::
	msgbox SilphCo_Text_Receptionist, MSGBOX_NPC
	end
SaffronCity_SilphCo_EventScript_Officer::
	goto_if_set FLAG_GOT_UP_GRADE, SaffronCity_SilphCo_EventScript_OfficerAfter
	msgbox SilphCo_Text_Officer, MSGBOX_NPC
	giveitem ITEM_UP_GRADE
	setflag FLAG_GOT_UP_GRADE
SaffronCity_SilphCo_EventScript_OfficerAfter::
	msgbox SilphCo_Text_Officer_GotUpGrade, MSGBOX_NPC
	end

SaffronCity_SilphCo_EventScript_Sign1::
	msgbox SilphCo_Text_Sign1, MSGBOX_SIGN
	end

SaffronCity_SilphCo_EventScript_Sign2::
	msgbox SilphCo_Text_Sign2, MSGBOX_SIGN
	end

SilphCo_Text_Sign1:
	.string "SILPH CO.\n"
	.string "1F RECEPTION.$"

SilphCo_Text_Sign2:
	.string "SILPH CO.\n"
	.string "ELEVATOR OUT OF SERVICE$"

SilphCo_Text_Receptionist:
	.string "Welcome. This is SILPH CO.'s HEAD\n"
	.string "OFFICE BUILDING.$"

SilphCo_Text_Officer:
	.string "Only employees are permitted to\n"
	.string "go upstairs.\p"
	.string "But since you came such a long\n"
	.string "way,\p"
	.string "have this neat little souvenir.$"

SilphCo_Text_Officer_GotUpGrade:
	.string "It's SILPH CO.'s latest product.\p"
	.string "It's not for sale anywhere yet.$"
