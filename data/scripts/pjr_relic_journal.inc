EventScript_OpenRelicJournal::
	lockall
	goto_if_set FLAG_PJR_RELIC_HO_OH, PJR_RelicJournal_Complete
	goto_if_unset FLAG_PJR_RELIC_RAIKOU, PJR_RelicJournal_Count0
	goto_if_unset FLAG_PJR_RELIC_ENTEI, PJR_RelicJournal_Count1
	goto_if_unset FLAG_PJR_RELIC_LUGIA, PJR_RelicJournal_Count2
	goto_if_unset FLAG_PJR_RELIC_UNOWN_I, PJR_RelicJournal_Count3
	goto_if_unset FLAG_PJR_RELIC_CELEBI, PJR_RelicJournal_Count4
	goto_if_unset FLAG_PJR_RELIC_SUICUNE, PJR_RelicJournal_Count5
	goto PJR_RelicJournal_Count6

PJR_RelicJournal_Count0::
	msgbox PJR_RelicJournal_Text_Count0, MSGBOX_YESNO
	goto PJR_RelicJournal_AfterMain
PJR_RelicJournal_Count1::
	msgbox PJR_RelicJournal_Text_Count1, MSGBOX_YESNO
	goto PJR_RelicJournal_AfterMain
PJR_RelicJournal_Count2::
	msgbox PJR_RelicJournal_Text_Count2, MSGBOX_YESNO
	goto PJR_RelicJournal_AfterMain
PJR_RelicJournal_Count3::
	msgbox PJR_RelicJournal_Text_Count3, MSGBOX_YESNO
	goto PJR_RelicJournal_AfterMain
PJR_RelicJournal_Count4::
	msgbox PJR_RelicJournal_Text_Count4, MSGBOX_YESNO
	goto PJR_RelicJournal_AfterMain
PJR_RelicJournal_Count5::
	msgbox PJR_RelicJournal_Text_Count5, MSGBOX_YESNO
	goto PJR_RelicJournal_AfterMain
PJR_RelicJournal_Count6::
	goto_if_set FLAG_PJR_RELIC_HO_OH_UNLOCKED, PJR_RelicJournal_Count6Unlocked
	msgbox PJR_RelicJournal_Text_Count6, MSGBOX_YESNO
	goto PJR_RelicJournal_AfterMain
PJR_RelicJournal_Count6Unlocked::
	msgbox PJR_RelicJournal_Text_Count6Unlocked, MSGBOX_YESNO

PJR_RelicJournal_AfterMain::
	goto_if_eq VAR_RESULT, NO, PJR_RelicJournal_Close
	call PJR_RelicJournal_Entry1
	call PJR_RelicJournal_Entry2
	call PJR_RelicJournal_Entry3
	call PJR_RelicJournal_Entry4
	call PJR_RelicJournal_Entry5
	call PJR_RelicJournal_Entry6
	goto PJR_RelicJournal_Close

PJR_RelicJournal_Entry1::
	goto_if_set FLAG_PJR_RELIC_RAIKOU, PJR_RelicJournal_Entry1Caught
	goto_if_set FLAG_PJR_RELIC_FOUND_RAIKOU, PJR_RelicJournal_Entry1Found
	msgbox PJR_RelicJournal_Text_Entry1Unknown, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry1Found::
	msgbox PJR_RelicJournal_Text_Entry1Found, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry1Caught::
	msgbox PJR_RelicJournal_Text_Entry1Caught, MSGBOX_DEFAULT
	return

PJR_RelicJournal_Entry2::
	goto_if_set FLAG_PJR_RELIC_ENTEI, PJR_RelicJournal_Entry2Caught
	goto_if_set FLAG_PJR_RELIC_FOUND_ENTEI, PJR_RelicJournal_Entry2Found
	goto_if_set FLAG_PJR_RELIC_RAIKOU, PJR_RelicJournal_Entry2Clue
	msgbox PJR_RelicJournal_Text_EntrySealed02, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry2Clue::
	msgbox PJR_RelicJournal_Text_Entry2Unknown, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry2Found::
	msgbox PJR_RelicJournal_Text_Entry2Found, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry2Caught::
	msgbox PJR_RelicJournal_Text_Entry2Caught, MSGBOX_DEFAULT
	return

PJR_RelicJournal_Entry3::
	goto_if_set FLAG_PJR_RELIC_LUGIA, PJR_RelicJournal_Entry3Caught
	goto_if_set FLAG_PJR_RELIC_FOUND_LUGIA, PJR_RelicJournal_Entry3Found
	goto_if_set FLAG_PJR_RELIC_ENTEI, PJR_RelicJournal_Entry3Clue
	msgbox PJR_RelicJournal_Text_EntrySealed03, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry3Clue::
	msgbox PJR_RelicJournal_Text_Entry3Unknown, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry3Found::
	msgbox PJR_RelicJournal_Text_Entry3Found, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry3Caught::
	msgbox PJR_RelicJournal_Text_Entry3Caught, MSGBOX_DEFAULT
	return

PJR_RelicJournal_Entry4::
	goto_if_set FLAG_PJR_RELIC_UNOWN_I, PJR_RelicJournal_Entry4Caught
	goto_if_set FLAG_PJR_RELIC_FOUND_UNOWN_I, PJR_RelicJournal_Entry4Found
	goto_if_set FLAG_PJR_RELIC_LUGIA, PJR_RelicJournal_Entry4Clue
	msgbox PJR_RelicJournal_Text_EntrySealed04, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry4Clue::
	msgbox PJR_RelicJournal_Text_Entry4Unknown, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry4Found::
	msgbox PJR_RelicJournal_Text_Entry4Found, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry4Caught::
	msgbox PJR_RelicJournal_Text_Entry4Caught, MSGBOX_DEFAULT
	return

PJR_RelicJournal_Entry5::
	goto_if_set FLAG_PJR_RELIC_CELEBI, PJR_RelicJournal_Entry5Caught
	goto_if_set FLAG_PJR_RELIC_FOUND_CELEBI, PJR_RelicJournal_Entry5Found
	goto_if_set FLAG_PJR_RELIC_UNOWN_I, PJR_RelicJournal_Entry5Clue
	msgbox PJR_RelicJournal_Text_EntrySealed05, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry5Clue::
	msgbox PJR_RelicJournal_Text_Entry5Unknown, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry5Found::
	msgbox PJR_RelicJournal_Text_Entry5Found, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry5Caught::
	msgbox PJR_RelicJournal_Text_Entry5Caught, MSGBOX_DEFAULT
	return

PJR_RelicJournal_Entry6::
	goto_if_set FLAG_PJR_RELIC_SUICUNE, PJR_RelicJournal_Entry6Caught
	goto_if_set FLAG_PJR_RELIC_FOUND_SUICUNE, PJR_RelicJournal_Entry6Found
	goto_if_set FLAG_PJR_RELIC_CELEBI, PJR_RelicJournal_Entry6Clue
	msgbox PJR_RelicJournal_Text_EntrySealed06, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry6Clue::
	msgbox PJR_RelicJournal_Text_Entry6Unknown, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry6Found::
	msgbox PJR_RelicJournal_Text_Entry6Found, MSGBOX_DEFAULT
	return
PJR_RelicJournal_Entry6Caught::
	msgbox PJR_RelicJournal_Text_Entry6Caught, MSGBOX_DEFAULT
	return

PJR_RelicJournal_Complete::
	msgbox PJR_RelicJournal_Text_Complete, MSGBOX_DEFAULT
PJR_RelicJournal_Close::
	releaseall
	end

PJR_RelicJournal_Text_Count0:
	.string "RELIC JOURNAL\nRELICS: 0 / 6\p"
	.string "FIRST INSCRIPTION:\n"
	.string "Where three sleepers fled from flame,\l"
	.string "thunder returns to broken stone.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Count1:
	.string "RELIC JOURNAL\nRELICS: 1 / 6\p"
	.string "NEW INSCRIPTION:\n"
	.string "Seek the mountain whose heart burns\l"
	.string "behind the lone fighter.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Count2:
	.string "RELIC JOURNAL\nRELICS: 2 / 6\p"
	.string "NEW INSCRIPTION:\n"
	.string "Below four islands, the deepest tide\l"
	.string "guards the third answer.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Count3:
	.string "RELIC JOURNAL\nRELICS: 3 / 6\p"
	.string "NEW INSCRIPTION:\n"
	.string "Return to ALPH. One eye watches\l"
	.string "from a chamber of written stone.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Count4:
	.string "RELIC JOURNAL\nRELICS: 4 / 6\p"
	.string "NEW INSCRIPTION:\n"
	.string "Where forest time gathers at a shrine,\l"
	.string "the fifth waits between moments.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Count5:
	.string "RELIC JOURNAL\nRELICS: 5 / 6\p"
	.string "FINAL INSCRIPTION:\n"
	.string "Return beneath the burned tower.\l"
	.string "Pure water remembers the three.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Count6:
	.string "RELIC JOURNAL\nRELICS: 6 / 6\p"
	.string "The six inscriptions are glowing.\n"
	.string "A seventh symbol has appeared.\p"
	.string "PROF.ELM must see this.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Count6Unlocked:
	.string "RELIC JOURNAL\nRELICS: 6 / 6\p"
	.string "The seventh symbol points toward\n"
	.string "BELL TOWER. A vast presence is awake.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Complete:
	.string "RELIC JOURNAL\nRELICS: 6 / 6\p"
	.string "SEVENTH SYMBOL: RESOLVED\n"
	.string "RELIC HO-OH: CAPTURED\p"
	.string "The ancient network is complete.$"

PJR_RelicJournal_Text_Entry1Unknown:
	.string "01  UNDISCOVERED\nPOKéMON: ???\p"
	.string "Clue: three sleepers fled from flame.\n"
	.string "Thunder returns to broken stone.$"
PJR_RelicJournal_Text_Entry1Found:
	.string "01  LOCATION DISCOVERED\nPOKéMON: ???\p"
	.string "BURNED TOWER B1F\nRelic Resonance detected.$"
PJR_RelicJournal_Text_Entry1Caught:
	.string "01  CAPTURED\nRAIKOU - BURNED TOWER B1F\p"
	.string "Its thunder mark deciphers the next path.$"

PJR_RelicJournal_Text_EntrySealed02:
	.string "02  UNDISCOVERED\nPOKéMON: ???\pThe text is unreadable.$"
PJR_RelicJournal_Text_Entry2Unknown:
	.string "02  UNDISCOVERED\nPOKéMON: ???\p"
	.string "Clue: a mountain heart burns behind\n"
	.string "the lone fighter.$"
PJR_RelicJournal_Text_Entry2Found:
	.string "02  LOCATION DISCOVERED\nPOKéMON: ???\p"
	.string "MT. MORTAR - DEEP CHAMBER\nRelic Resonance detected.$"
PJR_RelicJournal_Text_Entry2Caught:
	.string "02  CAPTURED\nENTEI - MT. MORTAR\p"
	.string "Its volcanic mark reveals the sea.$"

PJR_RelicJournal_Text_EntrySealed03:
	.string "03  UNDISCOVERED\nPOKéMON: ???\pThe text is unreadable.$"
PJR_RelicJournal_Text_Entry3Unknown:
	.string "03  UNDISCOVERED\nPOKéMON: ???\p"
	.string "Clue: below four islands, the deepest\n"
	.string "tide guards the answer.$"
PJR_RelicJournal_Text_Entry3Found:
	.string "03  LOCATION DISCOVERED\nPOKéMON: ???\p"
	.string "WHIRL ISLANDS - DEEPEST CHAMBER\nRelic Resonance detected.$"
PJR_RelicJournal_Text_Entry3Caught:
	.string "03  CAPTURED\nLUGIA - WHIRL ISLANDS\p"
	.string "Its abyssal mark points back to ALPH.$"

PJR_RelicJournal_Text_EntrySealed04:
	.string "04  UNDISCOVERED\nPOKéMON: ???\pThe text is unreadable.$"
PJR_RelicJournal_Text_Entry4Unknown:
	.string "04  UNDISCOVERED\nPOKéMON: ???\p"
	.string "Clue: one eye watches from a chamber\n"
	.string "of written stone.$"
PJR_RelicJournal_Text_Entry4Found:
	.string "04  LOCATION DISCOVERED\nPOKéMON: ???\p"
	.string "RUINS OF ALPH - HIDDEN CHAMBER\nThe Journal burns with light.$"
PJR_RelicJournal_Text_Entry4Caught:
	.string "04  CAPTURED\nI-UNOWN - RUINS OF ALPH\p"
	.string "The Eye mark bends the clue toward time.$"

PJR_RelicJournal_Text_EntrySealed05:
	.string "05  UNDISCOVERED\nPOKéMON: ???\pThe text is unreadable.$"
PJR_RelicJournal_Text_Entry5Unknown:
	.string "05  UNDISCOVERED\nPOKéMON: ???\p"
	.string "Clue: forest time gathers at an old shrine.$"
PJR_RelicJournal_Text_Entry5Found:
	.string "05  LOCATION DISCOVERED\nPOKéMON: ???\p"
	.string "ILEX FOREST SHRINE\nRelic Resonance detected.$"
PJR_RelicJournal_Text_Entry5Caught:
	.string "05  CAPTURED\nCELEBI - ILEX FOREST SHRINE\p"
	.string "Its time mark reveals the final text.$"

PJR_RelicJournal_Text_EntrySealed06:
	.string "06  UNDISCOVERED\nPOKéMON: ???\pThe text is unreadable.$"
PJR_RelicJournal_Text_Entry6Unknown:
	.string "06  UNDISCOVERED\nPOKéMON: ???\p"
	.string "Clue: beneath the burned tower, pure\n"
	.string "water remembers the three.$"
PJR_RelicJournal_Text_Entry6Found:
	.string "06  LOCATION DISCOVERED\nPOKéMON: ???\p"
	.string "BURNED TOWER - SACRED SPRING\nFinal Resonance detected.$"
PJR_RelicJournal_Text_Entry6Caught:
	.string "06  CAPTURED\nSUICUNE - SACRED SPRING\p"
	.string "All six marks now resonate as one.$"
