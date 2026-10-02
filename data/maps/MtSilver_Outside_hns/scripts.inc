MtSilver_Outside_hns_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtSilver_Outside_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, SetTimeEncounters
	.byte 0

MtSilver_Outside_OnTransition: 
	callnative SetTimeBasedEncounters
	setflag FLAG_VISITED_MT_SILVER
	end

MtSilver_Outside_EventScript_Sign::
	goto_if_unset FLAG_PJR_GOT_RELIC_JOURNAL, MtSilver_Outside_EventScript_SignStandard
	goto_if_unset FLAG_PJR_RELIC_ALPHORACLE, MtSilver_Outside_EventScript_SignStandard
	goto_if_set FLAG_PJR_GOT_RAINBOW_CREST, MtSilver_Outside_EventScript_SignStandard
	lock
	msgbox MtSilver_Outside_Text_RelicShortcut, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MtSilver_Outside_EventScript_RelicShortcutCancel
	closemessage
	warp MAP_MT_SILVER_SUMMIT_DAY_HNS, 10, 20
	waitstate
	end

MtSilver_Outside_EventScript_RelicShortcutCancel::
	closemessage
	release
	end

MtSilver_Outside_EventScript_SignStandard::
	msgbox MtSilver_Outside_Text_Sign, MSGBOX_SIGN
	end

MtSilver_Outside_Text_Sign:
	.string "MT. SILVER$"

MtSilver_Outside_Text_RelicShortcut:
	.string "The RELIC JOURNAL resonates here.\p"
	.string "A direct path to the SUMMIT has opened.\n"
	.string "Travel to RED now?$"
