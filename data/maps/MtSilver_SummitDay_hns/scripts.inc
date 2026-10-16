MtSilver_SummitDay_hns_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtSilver_SummitDay_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, MtSilver_SummitDay_OnFrame
	.byte 0

MtSilver_SummitDay_OnFrame::
	map_script_2 VAR_TEMP_MTSILVER_RESUME_BLIZZARD_SE, 0, MtSilver_SummitDay_Blizzard
	.2byte 0

MtSilver_SummitDay_Blizzard::
	playse SE_M_BLIZZARD
	setvar VAR_TEMP_MTSILVER_RESUME_BLIZZARD_SE, 1
	end

MtSilver_SummitDay_OnTransition:
	setescapewarp MAP_MT_SILVER_OUTSIDE_HNS, 17, 8
	call_if_set FLAG_DAY_POKEMON, MtSilver_SummitDay_EventScript_SetNight
	call_if_unset FLAG_DAY_POKEMON, MtSilver_SummitDay_EventScript_SetDay
	end

MtSilver_SummitDay_EventScript_SetNight::
	setmaplayoutindex LAYOUT_MT_SILVER_SUMMIT_NIGHT_HNS
	return

MtSilver_SummitDay_EventScript_SetDay::
	setmaplayoutindex LAYOUT_MT_SILVER_SUMMIT_DAY_HNS
	return

MtSilver_SummitDay_EventScript_Red::
	lock
	faceplayer
	@ A full-bag Crest can be collected on a later conversation, without
	@ preventing ordinary Red rematches once the Crest is received.
	goto_if_unset FLAG_DEFEATED_RED, MtSilver_SummitDay_EventScript_RedBattleNormal
	goto_if_unset FLAG_PJR_GOT_RAINBOW_CREST, MtSilver_SummitDay_EventScript_CheckPendingCrest
MtSilver_SummitDay_EventScript_RedBattleNormal::
	msgbox MtSilver_SummitDay_Text_Red, MSGBOX_DEFAULT
	closemessage
	goto_if_unset FLAG_IS_KANTO_CHAMPION, MtSilver_SummitDay_EventScript_RedStandard
	goto_if_ge VAR_SINJOH_STORYLINE, 13, MtSilver_SummitDay_EventScript_RedPostOBC

MtSilver_SummitDay_EventScript_RedStandard::
	trainerbattle_no_intro TRAINER_RED_HNS, MtSilver_SummitDay_Text_RedBeaten
	goto MtSilver_SummitDay_EventScript_RedOnDefeat

MtSilver_SummitDay_EventScript_RedPostOBC::
	trainerbattle_no_intro TRAINER_RED_POSTOBC_HNS, MtSilver_SummitDay_Text_RedBeaten
	goto MtSilver_SummitDay_EventScript_RedOnDefeat

MtSilver_SummitDay_EventScript_RedOnDefeat::
	playse SE_M_BLIZZARD
	setrespawn HEAL_LOCATION_NEW_BARK_TOWN_HNS
	msgbox MtSilver_SummitDay_Text_Red, MSGBOX_DEFAULT
	special GivePartyMonLandRibbon
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	setflag FLAG_HIDE_MTSILVER_RED
	removeobject LOCALID_MTSILVER_RED
	fadescreenswapbuffers FADE_FROM_BLACK
	delay 180
	fadescreenspeed FADE_TO_BLACK, 24
	setflag FLAG_DEFEATED_RED
	setflag FLAG_PJR_RED_DEFEATED
	goto_if_set FLAG_PJR_GOT_RAINBOW_CREST, MtSilver_SummitDay_EventScript_AfterCrest
	call MtSilver_SummitDay_EventScript_AwardCrest
MtSilver_SummitDay_EventScript_AfterCrest:
	@ Keep the original Hall of Fame and Red progression after this scene.
	call_if_set FLAG_PJR_RELIC_ALPHORACLE, MtSilver_SummitDay_EventScript_UnlockRelicHoOh
	setflag FLAG_END_NUZLOCKE
	clearflag FLAG_HIDE_MTSILVER_RED
	special GameClear
	waitstate
	releaseall
	end

@ Both initial reward and a subsequent safe retry use the same one-time
@ Crest handoff.  A full bag MUST NOT mark the Crest as received.
MtSilver_SummitDay_EventScript_AwardCrest::
	giveitem ITEM_ANCIENT_RAINBOW_CREST
	goto_if_eq VAR_RESULT, FALSE, MtSilver_SummitDay_EventScript_CrestFullBag
	setflag FLAG_PJR_GOT_RAINBOW_CREST
	msgbox MtSilver_SummitDay_Text_Crest, MSGBOX_DEFAULT
	return

MtSilver_SummitDay_EventScript_CrestFullBag::
	msgbox MtSilver_SummitDay_Text_CrestFullBag, MSGBOX_DEFAULT
	return

MtSilver_SummitDay_EventScript_CheckPendingCrest::
	goto_if_set FLAG_PJR_GOT_RAINBOW_CREST, MtSilver_SummitDay_EventScript_RedAlreadyRewarded
	msgbox MtSilver_SummitDay_Text_CrestPending, MSGBOX_DEFAULT
	call MtSilver_SummitDay_EventScript_AwardCrest
	call_if_set FLAG_PJR_GOT_RAINBOW_CREST, MtSilver_SummitDay_EventScript_UnlockRelicHoOh
	release
	end

MtSilver_SummitDay_Text_CrestPending:
	.string "RED left something behind.\p"
	.string "Make room for the CREST\n"
	.string "if your bag is full.$"

MtSilver_SummitDay_Text_CrestFullBag:
	.string "There is no room for the\n"
	.string "ANCIENT RAINBOW CREST!\p"
	.string "Return with bag space.\n"
	.string "The CREST is still here.$"

MtSilver_SummitDay_Text_Red:
	.string ".........................\n"
	.string ".........................$"

MtSilver_SummitDay_EventScript_UnlockRelicHoOh::
	setvar VAR_COMPLETED_HO_OH, 4
	clearflag FLAG_HIDE_HO_OH
	return

MtSilver_SummitDay_Text_RedBeaten:
	.string "...!$"

MtSilver_SummitDay_Text_Crest:
	.string "RED leaves behind the ANCIENT\n"
	.string "RAINBOW CREST.\p"
	.string "Its light points toward TIN TOWER.\p"
	.string "RED: The ULTIMATE RELIC has been\n"
	.string "spotted at the top of TIN TOWER.\p"
	.string "The CREST is reacting. Go.$"


