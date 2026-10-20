TinTower_8F_hns_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, TinTower_8F_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, TinTower_8F_OnFrame
	.byte 0

TinTower_8F_EventScript_SetWarp::
	lock
	goto_if_set FLAG_NIGHT_POKEMON, TinTower_8F_EventScript_SetWarpDay
	setdynamicwarp MAP_TIN_TOWER_ROOF_NIGHT_HNS, 10, 14
	release
	end

TinTower_8F_EventScript_SetWarpDay::
	setdynamicwarp MAP_TIN_TOWER_ROOF_DAY_HNS, 10, 14
	release
	end


TinTower_8F_OnTransition::
	call TinTower_8F_EventScript_SyncFinalRocketState
	call TinTower_OnTransition
	end

@ One-time mandatory Johto finale on 8F, in the statue gallery.
@ Keep the existing Ho-Oh roof scripts independent.
TinTower_8F_OnFrame::
	map_script_2 VAR_TEMP_0, 1, TinTower_8F_EventScript_JessieJamesBattle
	.2byte 0

TinTower_8F_EventScript_SyncFinalRocketState::
	setvar VAR_TEMP_0, 0
	goto_if_unset FLAG_PJR_GOT_RAINBOW_CREST, TinTower_8F_EventScript_HideFinalRocket
	goto_if_unset FLAG_PJR_RELIC_ALPHORACLE, TinTower_8F_EventScript_HideFinalRocket
	goto_if_set FLAG_PJR_JESSIE_JAMES_FINAL_DEFEATED, TinTower_8F_EventScript_HideFinalRocket
	setvar VAR_TEMP_0, 1
	return

TinTower_8F_EventScript_HideFinalRocket::
	removeobject LOCALID_TINTOWER8F_JESSIE
	removeobject LOCALID_TINTOWER8F_JAMES
	removeobject 5  @ Meowth: fifth local object on this map
	return

TinTower_8F_EventScript_JessieJamesTrigger::
	goto_if_unset FLAG_PJR_GOT_RAINBOW_CREST, TinTower_8F_EventScript_NoFinalRocket
	goto_if_unset FLAG_PJR_RELIC_ALPHORACLE, TinTower_8F_EventScript_NoFinalRocket
	goto_if_set FLAG_PJR_JESSIE_JAMES_FINAL_DEFEATED, TinTower_8F_EventScript_NoFinalRocket
	goto TinTower_8F_EventScript_JessieJamesBattle

TinTower_8F_EventScript_JessieJamesInteract::
	goto_if_set FLAG_PJR_JESSIE_JAMES_FINAL_DEFEATED, TinTower_8F_EventScript_NoFinalRocket
	goto TinTower_8F_EventScript_JessieJamesBattle

TinTower_8F_EventScript_JessieJamesBattle::
	lockall
	setvar VAR_TEMP_0, 0
	applymovement LOCALID_TINTOWER8F_JESSIE, Common_Movement_FacePlayer
	applymovement LOCALID_TINTOWER8F_JAMES, Common_Movement_FacePlayer
	waitmovement 0
	trainerbattle_double TRAINER_JESSIE_JAMES_TINTOWER_HNS, TinTower_8F_Text_JessieJamesFinalSeen, TinTower_8F_Text_JessieJamesFinalBeaten, TinTower_8F_Text_JessieJamesNeedTwo
	setflag FLAG_PJR_JESSIE_JAMES_FINAL_DEFEATED
	msgbox TinTower_8F_Text_JessieJamesFinalAfter, MSGBOX_DEFAULT
	removeobject LOCALID_TINTOWER8F_JESSIE
	removeobject LOCALID_TINTOWER8F_JAMES
	removeobject 5  @ Meowth
	releaseall
	end

TinTower_8F_EventScript_NoFinalRocket::
	end

TinTower_8F_Text_JessieJamesFinalSeen:
	.string "JESSIE: Twerp! Did you really think\n"
	.string "we'd let you claim the ULTIMATE RELIC?\p"
	.string "JAMES: One last performance.\n"
	.string "And this time, we're not holding back!$"

TinTower_8F_Text_JessieJamesFinalBeaten:
	.string "JESSIE & JAMES: Blasting off...\n"
	.string "from JOHTO... for now!$"

TinTower_8F_Text_JessieJamesFinalAfter:
	.string "JESSIE: Fine! The summit is yours.\p"
	.string "JAMES: But if that HO-OH joins you...\n"
	.string "we're taking credit for the warm-up!$"

TinTower_8F_Text_JessieJamesNeedTwo:
	.string "JAMES: This is a double battle!\n"
	.string "Bring at least two POK?MON.$"
