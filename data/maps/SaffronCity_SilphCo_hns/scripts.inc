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
SaffronCity_SilphCo_EventScript_StevenChooseStone::
	message SaffronCity_SilphCo_Text_Steven2
	waitmessage
	multichoice 20, 0, MULTI_HOENN_STARTERS, FALSE
	switch VAR_RESULT
	case 0, SaffronCity_SilphCo_EventScript_TreeckoChosen
	case 1, SaffronCity_SilphCo_EventScript_TorchicChosen
	case 2, SaffronCity_SilphCo_EventScript_MudkipChosen
	case MULTI_B_PRESSED, SaffronCity_SilphCo_EventScript_Refused

SaffronCity_SilphCo_EventScript_Refused::
	msgbox SaffronCity_SilphCo_Text_Refused, MSGBOX_DEFAULT
	turnobject LOCALID_SILPHCO_STEVEN, DIR_NORTH
	closemessage
	release
	end

SaffronCity_SilphCo_Text_Refused:
	.string "Oh...$"

SaffronCity_SilphCo_EventScript_TreeckoChosen::
	closemessage
	setvar VAR_TEMP_TRANSFERRED_SPECIES, SPECIES_TREECKO
	bufferspeciesname STR_VAR_1, SPECIES_TREECKO
	msgbox SaffronCity_SilphCo_Text_Steven3, MSGBOX_DEFAULT
	givemon SPECIES_TREECKO, 10
	goto SaffronCity_SilphCo_EventScript_CheckGiftSuccess
SaffronCity_SilphCo_EventScript_TorchicChosen::
	closemessage
	setvar VAR_TEMP_TRANSFERRED_SPECIES, SPECIES_BELDUM
	bufferspeciesname STR_VAR_1, SPECIES_BELDUM
	msgbox SaffronCity_SilphCo_Text_Steven3, MSGBOX_DEFAULT
	givemon SPECIES_BELDUM, 10
	goto SaffronCity_SilphCo_EventScript_CheckGiftSuccess
SaffronCity_SilphCo_EventScript_MudkipChosen::
	closemessage
	setvar VAR_TEMP_TRANSFERRED_SPECIES, SPECIES_BAGON
	bufferspeciesname STR_VAR_1, SPECIES_BAGON
	msgbox SaffronCity_SilphCo_Text_Steven3, MSGBOX_DEFAULT
	givemon SPECIES_BAGON, 10
	goto SaffronCity_SilphCo_EventScript_CheckGiftSuccess

@ Do not remove Steven or consume the one-time flag when the gift could not
@ enter either the party or Pokemon Storage. All choices share this check.
SaffronCity_SilphCo_EventScript_CheckGiftSuccess::
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PARTY, SaffronCity_SilphCo_EventScript_GiftSucceeded
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PC, SaffronCity_SilphCo_EventScript_GiftSucceeded
	msgbox SaffronCity_SilphCo_Text_StorageFull, MSGBOX_DEFAULT
	closemessage
	release
	end

SaffronCity_SilphCo_EventScript_GiftSucceeded::
	call Common_EventScript_GiftMon
	goto SaffronCity_SilphCo_EventScript_AfterStarterGiven

SaffronCity_SilphCo_EventScript_AfterStarterGiven::
	msgbox SaffronCity_SilphCo_Text_Steven4, MSGBOX_DEFAULT
	closemessage
	call_if_eq VAR_FACING, DIR_NORTH, SaffronCity_SilphCo_EventScript_PlayerMove
	applymovement LOCALID_SILPHCO_STEVEN, SaffronCity_SilphCo_Movement_StevenLeave
	waitmovement 0
	playse SE_EXIT
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
	.string "Hello...\n"
	.string "You're breaking up...\l"
	.string "I think it depends on my dad.\l"
	.string "I see...\n"
	.string "I'll be on my way. See you soon.$"
SaffronCity_SilphCo_Text_Steven2:
	.string "STEVEN: I spent years studying\n"
	.string "rare POKéMON and ancient stone.\p"
	.string "You have the eyes of a TRAINER\n"
	.string "who can raise something special.\p"
	.string "I have three unusual partners.\n"
	.string "Which would you choose?$"
SaffronCity_SilphCo_Text_Steven3:
	.string "You chose correctly! I'll give you\n"
	.string "{STR_VAR_1}!$"
SaffronCity_SilphCo_Text_StorageFull:
	.string "Your party and PC are full.\n"
	.string "Return when there's room.\p"
	.string "I'll keep the POKéMON safe.$"

SaffronCity_SilphCo_Text_Steven4:
	.string "Take good care of it. Your caring\n"
	.string "for it will make me very happy.$"

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
