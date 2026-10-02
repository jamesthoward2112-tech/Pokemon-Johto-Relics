TinTower_1F_hns_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, TinTower_OnTransition
	.byte 0

TinTower_OnTransition::
	setescapewarp MAP_BELLCHIME_TRAIL_HNS, 35, 42
	end

TinTower_1F_EventScript_SageA::
	lock
	faceplayer
	goto_if_eq VAR_ECRUTEAK_CITY_STATE, 11, TinTower_1F_EventScript_SageA_Hooh
	msgbox TinTower_1F_Sage4_Text2, MSGBOX_DEFAULT
	closemessage
	release
	end

TinTower_1F_EventScript_SageA_Hooh::
	msgbox TinTower_1F_Sage4_Text1, MSGBOX_DEFAULT
	closemessage
	release
	end

TinTower_1F_EventScript_SageB::
	lock
	faceplayer
	goto_if_eq VAR_ECRUTEAK_CITY_STATE, 11, TinTower_1F_EventScript_SageB_Hooh
	msgbox TinTower_1F_Sage2_Text, MSGBOX_DEFAULT
	closemessage
	release
	end

TinTower_1F_EventScript_SageB_Hooh::
	msgbox TinTower_1F_Sage1_Text, MSGBOX_DEFAULT
	closemessage
	release
	end

TinTower_1F_EventScript_SageC::
	lock
	faceplayer
	goto_if_eq VAR_ECRUTEAK_CITY_STATE, 11, TinTower_1F_EventScript_SageC_Hooh
	msgbox TinTower_1F_Sage6_Text2, MSGBOX_DEFAULT
	closemessage
	release
	end

TinTower_1F_EventScript_SageC_Hooh::
	msgbox TinTower_1F_Sage3_Text, MSGBOX_DEFAULT
	closemessage
	release
	end


TinTower_1F_Sage1_Text:
	.string "According to the oldest scrolls,\n"
	.string "HO-OH answers when JOHTO's\n"
	.string "hidden current awakens.\p"
	.string "Some of those marks match ALPH.\n"
	.string "We now call it RESONANCE.$"

TinTower_1F_Sage2_Text:
	.string "When the BRASS TOWER burned,\n"
	.string "three POKéMON lost their lives.\p"
	.string "HO-OH restored them with a power\n"
	.string "our records could not explain.\p"
	.string "ALPH scholars think it was pure,\n"
	.string "natural RESONANCE.$"

TinTower_1F_Sage3_Text:
	.string "The two TOWERS stand on older\n"
	.string "foundations.\p"
	.string "Stonework beneath them resembles\n"
	.string "the RUINS OF ALPH.\p"
	.string "ECRUTEAK may be only one part\n"
	.string "of a much older network.$"

TinTower_1F_Sage4_Text1:
	.string "HO-OH appears to have descended\n"
	.string "upon this, the TIN TOWER!$"

TinTower_1F_Sage4_Text2:
	.string "The legendary beasts embody\n"
	.string "lightning, fire and rain.\p"
	.string "UNOWN react to the same old pulse.\p"
	.string "Different legends...\n"
	.string "one RESONANCE.$"

TinTower_1F_Sage6_Text2:
	.string "Of the legendary POKéMON,\n"
	.string "SUICUNE is closest to HO-OH.\p"
	.string "Old records show UNOWN glyphs\n"
	.string "beside drawings of the beasts.\p"
	.string "The connection predates ECRUTEAK.$"

TinTower_1F_EusineHoOh_Text:
	.string "I knew it.\p"
	.string "I knew you'd get to see the POKéMON\n"
	.string "of rainbow colors, <PLAYER>.\p"
	.string "It happened just as I envisioned.\n"
	.string "My research isn't bad, I might say.\p"
	.string "I'm going to keep studying POKéMON\n"
	.string "to become a famous POKéMANIAC!$"

TinTower_1F_EusineSuicune_Text:
	.string "EUSINE: Awesome! Too awesome, even!\n"
	.string "I've never seen a battle that great.\p"
	.string "That was truly inspiring to see.\n"
	.string "SUICUNE was tough, but you were even\p"
	.string "more incredible, <PLAYER>.\n"
	.string "I heard SUICUNE's mystic power\p"
	.string "summons a rainbow-colored POKéMON.\n"
	.string "Maybe, just maybe, what went on today\p"
	.string "will cause that POKéMON to appear.\n"
	.string "I'm going to study the legends more.\p"
	.string "Thanks for showing me that fantastic\n"
	.string "battle.\p"
	.string "Later, <PLAYER>!$"
