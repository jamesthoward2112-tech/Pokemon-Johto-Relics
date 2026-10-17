CherrygroveCity_PokemonCenter_hns_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CherryGrove_Pokecenter_OnTransition
	.byte 0

CherryGrove_Pokecenter_OnTransition::
	setrespawn HEAL_LOCATION_CHERRYGROVE_CITY_HNS
	end

CherryGrove_Pokecenter_EventScript_Fisher::
	lock
	faceplayer
	msgbox CherryGrove_Pokecenter_Text_Fisher, MSGBOX_DEFAULT
	closemessage
	release
	end

CherryGrove_Pokecenter_EventScript_Gentleman::
	lock
	faceplayer
	msgbox CherryGrove_Pokecenter_Text_Gentleman, MSGBOX_DEFAULT
	closemessage
	release
	end

CherryGrove_Pokecenter_EventScript_Lass::
	lock
	faceplayer
	msgbox CherryGrove_Pokecenter_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

@ PRU repeatable experience trainer: interact with the existing Chansey
@ beside Nurse Joy. Every Pokemon Center assigns its own level tier via map.json.
@ Every battle has two Chansey, never a separate human overworld trainer.
CherryGrove_Pokecenter_Chansey::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_07_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv12::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_12_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv15::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_15_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv20::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_20_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv26::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_26_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv31::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_31_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv37::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_37_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv40::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_40_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv44::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_44_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv50::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_50_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv60::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_60_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv64::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_64_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv68::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_68_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv71::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_71_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv75::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_75_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv78::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_78_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv82::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_82_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv85::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_85_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv90::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_90_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv95::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_95_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Lv100::
	lock
	faceplayer
	call PRU_ChanseyTrainer_Offer
	goto_if_eq VAR_RESULT, FALSE, PRU_ChanseyTrainer_End
	trainerbattle_no_intro TRAINER_PRU_CHANSEY_100_HNS, PRU_ChanseyTrainer_Text_Victory
	goto PRU_ChanseyTrainer_Won

PRU_ChanseyTrainer_Offer::
	playmoncry SPECIES_CHANSEY, CRY_MODE_NORMAL
	waitmoncry
	msgbox PRU_ChanseyTrainer_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, PRU_ChanseyTrainer_OfferDeclined
	@ A double battle needs two usable party members; no softlock on first Pikachu.
	specialvar VAR_RESULT, CalculatePlayerPartyCount
	goto_if_lt VAR_RESULT, 2, PRU_ChanseyTrainer_NeedTwo
	setvar VAR_RESULT, TRUE
	return
PRU_ChanseyTrainer_OfferDeclined::
	setvar VAR_RESULT, FALSE
	return
PRU_ChanseyTrainer_NeedTwo::
	msgbox PRU_ChanseyTrainer_Text_NeedTwo, MSGBOX_DEFAULT
	setvar VAR_RESULT, FALSE
	return

PRU_ChanseyTrainer_Won::
	msgbox PRU_ChanseyTrainer_Text_After, MSGBOX_DEFAULT
PRU_ChanseyTrainer_End::
	closemessage
	release
	end

PRU_ChanseyTrainer_Text_Offer:
	.string "CHANSEY: Chan, chan!\p"
	.string "Train against a pair of\n"
	.string "CHANSEY? (DOUBLE BATTLE)$"

PRU_ChanseyTrainer_Text_NeedTwo:
	.string "Bring at least two POKéMON\n"
	.string "for a DOUBLE BATTLE.$"

PRU_ChanseyTrainer_Text_Victory:
	.string "CHANSEY: Chan-chaa!$"

PRU_ChanseyTrainer_Text_After:
	.string "CHANSEY looks ready to\n"
	.string "train again whenever you are.$"


CherryGrove_Pokecenter_Text_Fisher:
	.string "It's great. I can store any number\n"
	.string "of POKéMON, and it's all free.$"

CherryGrove_Pokecenter_Text_Gentleman:
	.string "That PC is free for any\n"
	.string "trainer to use.$"

CherryGrove_Pokecenter_Text_Lass:
	.string "They say a watched pot never\n"
	.string "boils. But watching the clock\l"
	.string "in the POKéCENTER makes time fly!$"

CherryGrove_Pokecenter_Text_Chansey:
	.string "CHANSEY: Chaan! Sii!$"
