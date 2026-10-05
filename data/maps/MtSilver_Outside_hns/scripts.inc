MtSilver_Outside_hns_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtSilver_Outside_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, SetTimeEncounters
	.byte 0

MtSilver_Outside_OnTransition: 
	callnative SetTimeBasedEncounters
	setflag FLAG_VISITED_MT_SILVER
	end

MtSilver_Outside_EventScript_Sign::
	msgbox MtSilver_Outside_Text_Sign, MSGBOX_YESNO
	switch VAR_RESULT
	case YES, MtSilver_Outside_EventScript_SummitShortcut
	case NO, MtSilver_Outside_EventScript_SignCancel
	case MULTI_B_PRESSED, MtSilver_Outside_EventScript_SignCancel

MtSilver_Outside_EventScript_SummitShortcut::
	closemessage
	warp MAP_MT_SILVER_SUMMIT_DAY_HNS, 10, 8
	waitstate
	end

MtSilver_Outside_EventScript_SignCancel::
	end

MtSilver_Outside_Text_Sign:
	.string "MT. SILVER\n"
	.string "A hidden trail skips the\n"
	.string "long climb.\p"
	.string "Take the shortcut to RED?$"
