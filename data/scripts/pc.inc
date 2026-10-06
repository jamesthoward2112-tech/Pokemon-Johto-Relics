EventScript_PC::
	lockall
#if IS_HNS
	setvar VAR_0x8004, PC_LOCATION_HNS
#else
	setvar VAR_0x8004, PC_LOCATION_OTHER
#endif
	special DoPCTurnOnEffect
	playse SE_PC_ON
	msgbox Text_BootUpPC, MSGBOX_DEFAULT
	goto EventScript_PCMainMenu
	end

EventScript_FakePC::
	lockall
#if IS_HNS
	setvar VAR_0x8004, PC_LOCATION_HNS
#else
	setvar VAR_0x8004, PC_LOCATION_OTHER
#endif
	playse SE_PC_ON
	msgbox Text_BootUpPC, MSGBOX_DEFAULT
	goto EventScript_FakePCMainMenu
	end

EventScript_PCMainMenu::
	message gText_WhichPCShouldBeAccessed
	waitmessage
	special ScriptMenu_CreatePCMultichoice
	waitstate
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_AccessPC_BeforeLeague
	goto EventScript_AccessPC_AfterLeague
	end


EventScript_FakePCMainMenu::
	message gText_WhichPCShouldBeAccessed
	waitmessage
	special ScriptMenu_CreatePCMultichoice
	waitstate
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_AccessFakePC_BeforeLeague
	goto EventScript_AccessFakePC_AfterLeague
	end

EventScript_AccessPC_BeforeLeague::
	switch VAR_RESULT
	case 0, EventScript_AccessPokemonStorage
	case 1, EventScript_AccessPlayersPC
	case 2, EventScript_ChallengeViewer
	case 3, EventScript_TurnOffPC
	case MULTI_B_PRESSED, EventScript_TurnOffPC
	end

EventScript_AccessFakePC_BeforeLeague::
	switch VAR_RESULT
	case 0, EventScript_AccessFakePokemonStorage
	case 1, EventScript_AccessPlayersFakePC
	case 2, EventScript_FakeChallengeViewer
	case 3, EventScript_TurnOffFakePC
	case MULTI_B_PRESSED, EventScript_TurnOffFakePC
	end

EventScript_AccessPC_AfterLeague::
	switch VAR_RESULT
	case 0, EventScript_AccessPokemonStorage
	case 1, EventScript_AccessPlayersPC
	case 2, EventScript_AccessHallOfFame
	case 3, EventScript_ChallengeViewer
	case 4, EventScript_TurnOffPC
	case MULTI_B_PRESSED, EventScript_TurnOffPC
	end

EventScript_AccessFakePC_AfterLeague::
	switch VAR_RESULT
	case 0, EventScript_AccessFakePokemonStorage
	case 1, EventScript_AccessPlayersFakePC
	case 2, EventScript_AccessFakeHallOfFame
	case 3, EventScript_FakeChallengeViewer
	case 4, EventScript_TurnOffFakePC
	case MULTI_B_PRESSED, EventScript_TurnOffFakePC
	end

EventScript_ChallengeViewer::
	playse SE_PC_LOGIN
	callnative Script_OpenChallengeMenu
	waitstate
	goto EventScript_PCMainMenu
	end

EventScript_FakeChallengeViewer::
	playse SE_PC_LOGIN
	callnative Script_OpenChallengeMenu
	delay 30
	goto EventScript_FakePCMainMenu
	end

EventScript_AccessPlayersPC::
	playse SE_PC_LOGIN
	msgbox gText_AccessedPlayersPC, MSGBOX_DEFAULT
	special PlayerPC
	waitstate
	goto EventScript_PCMainMenu
	end

EventScript_AccessPlayersFakePC::
	playse SE_PC_LOGIN
	msgbox gText_AccessedPlayersPC, MSGBOX_DEFAULT
	special PlayerPC
	waitstate
	goto EventScript_FakePCMainMenu
	end

EventScript_AccessPokemonStorage::
	playse SE_PC_LOGIN
	call_if_unset FLAG_SYS_PC_LANETTE, EventScript_AccessSomeonesPC
	call_if_set FLAG_SYS_PC_LANETTE, EventScript_AccessLanettesPC
	call EventScript_PjrEvolutionQaKit
	msgbox gText_StorageSystemOpened, MSGBOX_DEFAULT
	special ShowPokemonStorageSystemPC
	waitstate
	goto EventScript_PCMainMenu
	end

EventScript_AccessFakePokemonStorage::
	playse SE_PC_LOGIN
	call_if_unset FLAG_SYS_PC_LANETTE, EventScript_AccessSomeonesPC
	call_if_set FLAG_SYS_PC_LANETTE, EventScript_AccessLanettesPC
	call EventScript_PjrEvolutionQaKit
	msgbox gText_StorageSystemOpened, MSGBOX_DEFAULT
	special ShowPokemonStorageSystemPC
	waitstate
	goto EventScript_FakePCMainMenu
	end

EventScript_PjrEvolutionQaKit::
	goto_if_set FLAG_PJR_QA_EVOLUTION_KIT, EventScript_PjrEvolutionQaKit_Done
	special PjrGiveEvolutionQaKit
	goto_if_eq VAR_RESULT, FALSE, EventScript_PjrEvolutionQaKit_NoSpace
	setflag FLAG_PJR_QA_EVOLUTION_KIT
	msgbox gText_PjrEvolutionQaKitInstalled, MSGBOX_DEFAULT
	return
EventScript_PjrEvolutionQaKit_NoSpace::
	msgbox gText_PjrEvolutionQaKitNeedsBox, MSGBOX_DEFAULT
EventScript_PjrEvolutionQaKit_Done::
	return

gText_PjrEvolutionQaKitInstalled:
	.string "PJR EVOLUTION QA KIT loaded!\p"
	.string "26 test POKéMON are in the\n"
	.string "RELICTST Box.\p"
	.string "99 RARE CANDIES and evolution\n"
	.string "stones were added to your BAG.$"

gText_PjrEvolutionQaKitNeedsBox:
	.string "PJR QA KIT needs one completely\n"
	.string "empty PC Box.\p"
	.string "Clear a Box, then access POKéMON\n"
	.string "STORAGE again. Nothing was changed.$"

EventScript_AccessSomeonesPC::
	msgbox gText_AccessedSomeonesPC, MSGBOX_DEFAULT
	return

EventScript_AccessLanettesPC::
#if IS_FRLG || IS_HNS
	msgbox gText_AccessedBillsPC, MSGBOX_DEFAULT
#else
	msgbox gText_AccessedLanettesPC, MSGBOX_DEFAULT
#endif
	return

EventScript_TurnOffPC::
#if IS_HNS
	setvar VAR_0x8004, PC_LOCATION_HNS
#else
	setvar VAR_0x8004, PC_LOCATION_OTHER
#endif
	playse SE_PC_OFF
	special DoPCTurnOffEffect
	releaseall
	end

EventScript_TurnOffFakePC::
	playse SE_PC_OFF
	releaseall
	end

EventScript_AccessHallOfFame::
	goto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_TurnOffPC
	playse SE_PC_LOGIN
	special AccessHallOfFamePC
	waitstate
	goto EventScript_AccessPC_AfterLeague
	end

EventScript_AccessFakeHallOfFame::
	playse SE_PC_LOGIN
	special AccessHallOfFamePC
	waitstate
	goto EventScript_AccessFakePC_AfterLeague
	end

EventScript_AccessPokemonBoxLink::
	lockall
	playse SE_PC_LOGIN
	special ShowPokemonStorageSystemPC
	waitstate
	@ Remote access must never run the physical PC metatile effect.
	goto EventScript_TurnOffFakePC
	end
