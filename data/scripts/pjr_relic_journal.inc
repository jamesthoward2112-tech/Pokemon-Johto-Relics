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
	goto_if_unset FLAG_PJR_RELIC_ALPHORACLE, PJR_RelicJournal_Count6NeedFirstVoice
	goto_if_unset FLAG_PJR_GOT_RAINBOW_CREST, PJR_RelicJournal_Count6NeedCrest
	call PJR_RelicQuest_TryUnlockHoOh
	msgbox PJR_RelicJournal_Text_Count6Unlocked, MSGBOX_YESNO
	goto PJR_RelicJournal_AfterMain
PJR_RelicJournal_Count6NeedFirstVoice::
	goto_if_set FLAG_PJR_GOT_RAINBOW_CREST, PJR_RelicJournal_Count6NeedFirstVoiceWithCrest
	msgbox PJR_RelicJournal_Text_Count6NeedFirstVoice, MSGBOX_YESNO
	goto PJR_RelicJournal_AfterMain
PJR_RelicJournal_Count6NeedFirstVoiceWithCrest::
	msgbox PJR_RelicJournal_Text_Count6NeedFirstVoiceWithCrest, MSGBOX_YESNO
	goto PJR_RelicJournal_AfterMain
PJR_RelicJournal_Count6NeedCrest::
	msgbox PJR_RelicJournal_Text_Count6NeedCrest, MSGBOX_YESNO
	goto PJR_RelicJournal_AfterMain

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
	.string "CURRENT OBJECTIVE:\nFind the first RELIC.\p"
	.string "NEXT DESTINATION:\nBURNED TOWER B1F\lECRUTEAK CITY\p"
	.string "Hint: Thunder stirs beneath the\nruined tower.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Count1:
	.string "RELIC JOURNAL\nRELICS: 1 / 6\p"
	.string "CURRENT OBJECTIVE:\nFind the second RELIC.\p"
	.string "NEXT DESTINATION:\nMT. MORTAR 2F\p"
	.string "Hint: Violent heat is building\ndeep inside MT. MORTAR.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Count2:
	.string "RELIC JOURNAL\nRELICS: 2 / 6\p"
	.string "CURRENT OBJECTIVE:\nFind the third RELIC.\p"
	.string "NEXT DESTINATION:\nWHIRL ISLANDS\lLUGIA CHAMBER\p"
	.string "Hint: The signal comes from the\ndeepest chamber below the islands.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Count3:
	.string "RELIC JOURNAL\nRELICS: 3 / 6\p"
	.string "CURRENT OBJECTIVE:\nFind the fourth RELIC.\p"
	.string "NEXT DESTINATION:\nRUINS OF ALPH\lDEEPEST CHAMBER\p"
	.string "Talk to the LAB scientist for a direct\nroute. Inspect the ancient statue.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Count4:
	.string "RELIC JOURNAL\nRELICS: 4 / 6\p"
	.string "CURRENT OBJECTIVE:\nFind the fifth RELIC.\p"
	.string "NEXT DESTINATION:\nILEX FOREST SHRINE\p"
	.string "Hint: The forest shrine is reacting\nto the Resonance.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Count5:
	.string "RELIC JOURNAL\nRELICS: 5 / 6\p"
	.string "CURRENT OBJECTIVE:\nFind the final RELIC.\p"
	.string "NEXT DESTINATION:\nBURNED TOWER B1F\lECRUTEAK CITY\p"
	.string "Hint: The final signal has returned\nto where the chain began.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Count6NeedFirstVoice:
	.string "RELIC JOURNAL\nRELICS: 6 / 6\p"
	.string "CURRENT OBJECTIVE:\nFind the FIRST VOICE.\p"
	.string "NEXT DESTINATION:\nRUINS OF ALPH\lDEEPEST CHAMBER\p"
	.string "Talk to the LAB scientist for a direct\nroute to the ancient statue.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Count6NeedFirstVoiceWithCrest:
	.string "RELIC JOURNAL\nRELICS: 6 / 6\p"
	.string "ANCIENT RAINBOW CREST: OBTAINED\p"
	.string "CURRENT OBJECTIVE:\nFind the FIRST VOICE.\p"
	.string "NEXT DESTINATION:\nRUINS OF ALPH\lDEEPEST CHAMBER\p"
	.string "Talk to the LAB scientist for a direct\nroute to the ancient statue.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Count6NeedCrest:
	.string "RELIC JOURNAL\nRELICS: 6 / 6\p"
	.string "FIRST VOICE: ANSWERED\p"
	.string "CURRENT OBJECTIVE:\nObtain the ANCIENT RAINBOW CREST.\p"
	.string "NEXT DESTINATION:\nMT. SILVER SUMMIT\lDEFEAT RED\p"
	.string "Use the MT. SILVER entrance sign for\na direct route to the summit.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Count6Unlocked:
	.string "RELIC JOURNAL\nRELICS: 6 / 6\p"
	.string "FIRST VOICE: ANSWERED\n"
	.string "RAINBOW CREST: RESONATING\p"
	.string "CURRENT OBJECTIVE:\nFace the final awakening.\p"
	.string "NEXT DESTINATION:\nBELL TOWER ROOF\lECRUTEAK CITY\p"
	.string "Use the glowing beam on BELL TOWER\n1F for a direct ascent.\p"
	.string "View all six records?$"
PJR_RelicJournal_Text_Complete:
	.string "RELIC JOURNAL\nRELICS: 6 / 6\p"
	.string "FIRST VOICE: ANSWERED\n"
	.string "RAINBOW CREST: RESOLVED\p"
	.string "RELIC HO-OH: CAPTURED\p"
	.string "The ancient network is complete.$"

PJR_RelicJournal_Text_Entry1Unknown:
	.string "01  UNDISCOVERED\nPOKéMON: ???\p"
	.string "NEXT: BURNED TOWER B1F\nECRUTEAK CITY.$"
PJR_RelicJournal_Text_Entry1Found:
	.string "01  LOCATION DISCOVERED\nPOKéMON: ???\p"
	.string "BURNED TOWER B1F\nRelic Resonance detected.$"
PJR_RelicJournal_Text_Entry1Caught:
	.string "01  CAPTURED\nRAIKOU - BURNED TOWER B1F\p"
	.string "NEXT: MT. MORTAR 2F.$"

PJR_RelicJournal_Text_EntrySealed02:
	.string "02  UNDISCOVERED\nPOKéMON: ???\pThe text is unreadable.$"
PJR_RelicJournal_Text_Entry2Unknown:
	.string "02  UNDISCOVERED\nPOKéMON: ???\p"
	.string "NEXT: MT. MORTAR 2F.$"
PJR_RelicJournal_Text_Entry2Found:
	.string "02  LOCATION DISCOVERED\nPOKéMON: ???\p"
	.string "MT. MORTAR 2F\nRelic Resonance detected.$"
PJR_RelicJournal_Text_Entry2Caught:
	.string "02  CAPTURED\nENTEI - MT. MORTAR 2F\p"
	.string "NEXT: WHIRL ISLANDS\nLUGIA CHAMBER.$"

PJR_RelicJournal_Text_EntrySealed03:
	.string "03  UNDISCOVERED\nPOKéMON: ???\pThe text is unreadable.$"
PJR_RelicJournal_Text_Entry3Unknown:
	.string "03  UNDISCOVERED\nPOKéMON: ???\p"
	.string "NEXT: WHIRL ISLANDS\nLUGIA CHAMBER.$"
PJR_RelicJournal_Text_Entry3Found:
	.string "03  LOCATION DISCOVERED\nPOKéMON: ???\p"
	.string "WHIRL ISLANDS - LUGIA CHAMBER\nRelic Resonance detected.$"
PJR_RelicJournal_Text_Entry3Caught:
	.string "03  CAPTURED\nLUGIA - WHIRL ISLANDS\p"
	.string "NEXT: RUINS OF ALPH\nDEEPEST CHAMBER.$"

PJR_RelicJournal_Text_EntrySealed04:
	.string "04  UNDISCOVERED\nPOKéMON: ???\pThe text is unreadable.$"
PJR_RelicJournal_Text_Entry4Unknown:
	.string "04  UNDISCOVERED\nPOKéMON: ???\p"
	.string "NEXT: RUINS OF ALPH\nDEEPEST CHAMBER.\p"
	.string "Inspect the ancient statue.$"
PJR_RelicJournal_Text_Entry4Found:
	.string "04  LOCATION DISCOVERED\nPOKéMON: ???\p"
	.string "RUINS OF ALPH - DEEPEST CHAMBER\nThe Journal burns with light.$"
PJR_RelicJournal_Text_Entry4Caught:
	.string "04  CAPTURED\nI-UNOWN - RUINS OF ALPH\p"
	.string "NEXT: ILEX FOREST SHRINE.$"

PJR_RelicJournal_Text_EntrySealed05:
	.string "05  UNDISCOVERED\nPOKéMON: ???\pThe text is unreadable.$"
PJR_RelicJournal_Text_Entry5Unknown:
	.string "05  UNDISCOVERED\nPOKéMON: ???\p"
	.string "NEXT: ILEX FOREST SHRINE.$"
PJR_RelicJournal_Text_Entry5Found:
	.string "05  LOCATION DISCOVERED\nPOKéMON: ???\p"
	.string "ILEX FOREST SHRINE\nRelic Resonance detected.$"
PJR_RelicJournal_Text_Entry5Caught:
	.string "05  CAPTURED\nCELEBI - ILEX FOREST SHRINE\p"
	.string "NEXT: BURNED TOWER B1F\nECRUTEAK CITY.$"

PJR_RelicJournal_Text_EntrySealed06:
	.string "06  UNDISCOVERED\nPOKéMON: ???\pThe text is unreadable.$"
PJR_RelicJournal_Text_Entry6Unknown:
	.string "06  UNDISCOVERED\nPOKéMON: ???\p"
	.string "NEXT: BURNED TOWER B1F\nECRUTEAK CITY.$"
PJR_RelicJournal_Text_Entry6Found:
	.string "06  LOCATION DISCOVERED\nPOKéMON: ???\p"
	.string "BURNED TOWER B1F\nFinal Resonance detected.$"
PJR_RelicJournal_Text_Entry6Caught:
	.string "06  CAPTURED\nSUICUNE - BURNED TOWER B1F\p"
	.string "NEXT: RUINS OF ALPH\nDEEPEST CHAMBER.$"

PJR_RelicQuest_TryUnlockHoOh::
	goto_if_unset FLAG_PJR_RELIC_ALPHORACLE, PJR_RelicQuest_TryUnlockHoOh_Return
	goto_if_unset FLAG_PJR_GOT_RAINBOW_CREST, PJR_RelicQuest_TryUnlockHoOh_Return
	setflag FLAG_PJR_RELIC_HO_OH_UNLOCKED
	setvar VAR_COMPLETED_HO_OH, 4
	clearflag FLAG_HIDE_HO_OH
PJR_RelicQuest_TryUnlockHoOh_Return::
	return

@ PJR RELICS world-encounter quest implementation checkpoint.
