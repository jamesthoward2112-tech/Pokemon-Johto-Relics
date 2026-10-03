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
	msgbox MtSilver_SummitDay_Text_Red, MSGBOX_DEFAULT
	closemessage
	goto_if_unset FLAG_PJR_RELIC_SIX_RESONANCE, MtSilver_SummitDay_EventScript_RedNotReady
	goto_if_unset FLAG_PJR_RELIC_ALPHORACLE, MtSilver_SummitDay_EventScript_RedNotReady
	goto_if_ge VAR_SINJOH_STORYLINE, 13, MtSilver_SummitDay_EventScript_RedPostOBC
	goto MtSilver_SummitDay_EventScript_RedStandard

MtSilver_SummitDay_EventScript_RedNotReady::
	releaseall
	end

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
	setflag FLAG_DEFEATED_RED
	setflag FLAG_PJR_RED_DEFEATED
	goto_if_set FLAG_PJR_GOT_RAINBOW_CREST, MtSilver_SummitDay_EventScript_AfterCrest
	giveitem ITEM_ANCIENT_RAINBOW_CREST
	setflag FLAG_PJR_GOT_RAINBOW_CREST
	goto_if_set FLAG_PJR_RELIC_ALPHORACLE, MtSilver_SummitDay_EventScript_CrestReady
	msgbox MtSilver_SummitDay_Text_CrestNeedsFirstVoice, MSGBOX_DEFAULT
	goto MtSilver_SummitDay_EventScript_AfterCrest
MtSilver_SummitDay_EventScript_CrestReady:
	msgbox MtSilver_SummitDay_Text_CrestReady, MSGBOX_DEFAULT
MtSilver_SummitDay_EventScript_AfterCrest:
	call PJR_RelicQuest_TryUnlockHoOh
	setflag FLAG_END_NUZLOCKE
	clearflag FLAG_HIDE_MTSILVER_RED
	releaseall
	end

MtSilver_SummitDay_Text_Red:
	.string ".........................\n"
	.string ".........................$"

MtSilver_SummitDay_Text_RedBeaten:
	.string "...!$"

MtSilver_SummitDay_Text_CrestNeedsFirstVoice:
	.string "ANCIENT RAINBOW CREST: OBTAINED\p"
	.string "CURRENT OBJECTIVE:\nFind the FIRST VOICE.\p"
	.string "NEXT DESTINATION:\nRUINS OF ALPH\lDEEPEST CHAMBER.$"

MtSilver_SummitDay_Text_CrestReady:
	.string "ANCIENT RAINBOW CREST: RESONATING\p"
	.string "FIRST VOICE: ANSWERED\p"
	.string "NEXT DESTINATION:\nBELL TOWER ROOF\lECRUTEAK CITY.\p"
	.string "Use the glowing beam on BELL TOWER\n1F for a direct ascent.$"


