MtMortar_2F_hns_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtMortar_2F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, SetTimeEncounters
	.byte 0

MtMortar_2F_OnTransition: 
	callnative SetTimeBasedEncounters
	end

MtMortar_2F_EventScript_RelicEntei::
	lock
	goto_if_unset FLAG_PJR_GOT_RELIC_JOURNAL, MtMortar_2F_EventScript_RelicStoneSilent
	goto_if_unset FLAG_PJR_RELIC_RAIKOU, MtMortar_2F_EventScript_RelicStoneSilent
	goto_if_set FLAG_PJR_RELIC_ENTEI, MtMortar_2F_EventScript_RelicStoneResolved
	setflag FLAG_PJR_RELIC_FOUND_ENTEI
	msgbox MtMortar_2F_Text_RelicEntei, MSGBOX_DEFAULT
	playmoncry SPECIES_ENTEI, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ENTEI, 66
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtMortar_2F_EventScript_RelicEnteiCaught
	msgbox MtMortar_2F_Text_RelicRetry, MSGBOX_DEFAULT
	release
	end

MtMortar_2F_EventScript_RelicEnteiCaught::
	setflag FLAG_PJR_RELIC_ENTEI
	msgbox MtMortar_2F_Text_RelicEnteiCaught, MSGBOX_DEFAULT
	release
	end

MtMortar_2F_EventScript_RelicStoneSilent::
	msgbox MtMortar_2F_Text_RelicStoneSilent, MSGBOX_DEFAULT
	release
	end

MtMortar_2F_EventScript_RelicStoneResolved::
	msgbox MtMortar_2F_Text_RelicStoneResolved, MSGBOX_DEFAULT
	release
	end

MtMortar_2F_Text_RelicEntei:
	.string "The RELIC JOURNAL flashes E.\p"
	.string "Heat surges through the mountain.\n"
	.string "ENTEI answers the Resonance!$"

MtMortar_2F_Text_RelicEnteiCaught:
	.string "The E mark burns into the Journal.\p"
	.string "The next inscription speaks of\n"
	.string "the deepest tide below four islands.$"

MtMortar_2F_Text_RelicRetry:
	.string "The volcanic Resonance remains.\p"
	.string "ENTEI will return until it is captured.$"

MtMortar_2F_Text_RelicStoneSilent:
	.string "The stone is warm, but quiet.$"

MtMortar_2F_Text_RelicStoneResolved:
	.string "The Resonance here has gone still.$"


MtMortar_2F_EventScript_Item_Iron::
    finditem ITEM_IRON
    end

MtMortar_2F_EventScript_Item_MaxRevive::
    finditem ITEM_MAX_REVIVE
    end

MtMortar_2F_EventScript_Item_Ether::
    finditem ITEM_ETHER
    end

MtMortar_2F_EventScript_Item_RareCandy::
    finditem ITEM_RARE_CANDY
    end

MtMortar_2F_EventScript_Item_DragonScale::
    finditem ITEM_DRAGON_SCALE
    end

MtMortar_2F_EventScript_Item_Elixir::
    finditem ITEM_ELIXIR
    end

MtMortar_2F_EventScript_Nerd::
	trainerbattle_single TRAINER_HUGH_HNS, MtMortar_2F_Text_SupernerdHughSeen, MtMortar_2F_Text_SupernerdHughBeaten
	msgbox MtMortar_2F_Text_SupernerdHughAfter, MSGBOX_AUTOCLOSE
	end

MtMortar_2F_Text_SupernerdHughSeen::
	.string "Yo! MARKUS!$"

MtMortar_2F_Text_SupernerdHughBeaten:
	.string "Sorry, my mistake.\n"
	.string "I misjudged you.$"

MtMortar_2F_Text_SupernerdHughAfter:
	.string "I'm investigating MT.MORTAR,\n"
	.string "but my pal's gone AWOL.\p"
	.string "Have you seen a trainer who\n"
	.string "has a SLOWPOKE that can use\l"
	.string "STRENGTH?$"
