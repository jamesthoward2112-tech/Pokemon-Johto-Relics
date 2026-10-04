@ PJR Kanto post-League initialization.
@ The original game only ran this state setup when leaving the S.S. Aqua.
@ PJR also opens Route 22 after the first League clear, so Kanto can be entered
@ through Viridian first. Keep the setup one-time and preserve progressed saves.

Common_EventScript_PJRInitKanto::
	goto_if_set FLAG_EXTENDED_CONTENT_111, Common_EventScript_PJRInitKanto_Return

	@ Migration: never reset an existing save that already made Kanto progress.
	goto_if_ge VAR_SSAQUA_STATE, 7, Common_EventScript_PJRInitKanto_MarkExisting
	goto_if_ge VAR_NUM_BADGES, 9, Common_EventScript_PJRInitKanto_MarkExisting
	goto_if_set FLAG_BADGE09_GET, Common_EventScript_PJRInitKanto_MarkExisting
	goto_if_set FLAG_BADGE10_GET, Common_EventScript_PJRInitKanto_MarkExisting
	goto_if_set FLAG_BADGE11_GET, Common_EventScript_PJRInitKanto_MarkExisting
	goto_if_set FLAG_BADGE12_GET, Common_EventScript_PJRInitKanto_MarkExisting
	goto_if_set FLAG_BADGE13_GET, Common_EventScript_PJRInitKanto_MarkExisting
	goto_if_set FLAG_BADGE14_GET, Common_EventScript_PJRInitKanto_MarkExisting
	goto_if_set FLAG_BADGE15_GET, Common_EventScript_PJRInitKanto_MarkExisting
	goto_if_set FLAG_BADGE16_GET, Common_EventScript_PJRInitKanto_MarkExisting
	goto_if_ge VAR_KANTO_ROCKET_STORY_STATE, 1, Common_EventScript_PJRInitKanto_MarkExisting

	@ Kanto visibility/state defaults. This is the former S.S. Aqua flag heap.
	setflag FLAG_HIDE_COPYCAT_CLEFAIRY_DOLL
	setflag FLAG_HIDE_CERULEAN_GYM_TRAINERS
	setflag FLAG_HIDE_CERULEAN_CAPE_ROCKET
	setflag FLAG_HIDE_CERULEAN_GYM_ROCKET
	setflag FLAG_HIDDEN_ITEM_MACHINE_PART
	setflag FLAG_HIDE_ROUTE25_MISTY
	setflag FLAG_HIDE_ROUTE25_EUSINE
	setflag FLAG_HIDE_ROUTE25_SUICUNE
	setflag FLAG_HIDE_CELADON_EUSINE
	setflag FLAG_HIDE_SEAFOAM_GYMGUY
	setflag FLAG_HIDE_VIRIDIAN_BLUE
	setflag FLAG_HIDE_ROUTE14_EUSINE
	setflag FLAG_HIDE_ROUTE14_SUICUNE
	setflag FLAG_HIDE_VIRIDIAN_FOREST_SPIKY_EARED_PICHU
	setflag FLAG_HIDE_VIRIDIAN_FOREST_SPIKY_EARED_PICHU1
	setflag FLAG_HIDE_VIRIDIAN_FOREST_SPIKY_EARED_PICHU2
	setflag FLAG_HIDE_VIRIDIAN_FOREST_SPIKY_EARED_PICHU3
	setflag FLAG_HIDE_VIRIDIAN_FOREST_SPIKY_EARED_PICHU4
	setflag FLAG_HIDE_ROUTE13_BOAT
	setflag FLAG_MT_SILVER_1F_HIDE_SCIENTIST
	setflag FLAG_HIDE_VERMILION_CITY_SAMSON
	setflag FLAG_HIDE_ROUTE28_SCIENTIST

	clearflag FLAG_BADGE09_GET
	clearflag FLAG_BADGE10_GET
	clearflag FLAG_BADGE11_GET
	clearflag FLAG_BADGE12_GET
	clearflag FLAG_BADGE13_GET
	clearflag FLAG_BADGE14_GET
	clearflag FLAG_BADGE15_GET
	clearflag FLAG_BADGE16_GET
	clearflag FLAG_GOT_VERMILION_HP_UP
	clearflag FLAG_KANTO_RADIO_GOT
	clearflag FLAG_HIDE_VERMILION_SNORLAX
	clearflag FLAG_HIDE_FAN_CLUB_CLEFAIRY_DOLL
	clearflag FLAG_FOUND_BOTH_VERMILION_GYM_SWITCHES
	clearflag FLAG_RETURNED_MACHINE_PART
	clearflag FLAG_GOT_TM_PSYCHIC
	clearflag FLAG_GOT_HOENN_STARTER
	clearflag FLAG_GOT_UP_GRADE
	clearflag FLAG_GOT_CLEANSE_TAG
	clearflag FLAG_ROUTE25_GOT_NUGGET
	clearflag FLAG_HIDE_POWER_PLANT_ENGINEER
	clearflag FLAG_HIDE_ZAPDOS
	clearflag FLAG_HIDE_ARTICUNO
	clearflag FLAG_HIDE_MOLTRES
	clearflag FLAG_GOT_TM_SLEEP_TALK
	clearflag FLAG_GOT_SUPER_ROD
	clearflag FLAG_HIDE_CINNABAR_BLUE
	clearflag FLAG_GOT_ROUTE2_NUGGET
	clearflag FLAG_GOT_VIRIDIAN_TM_DREAM_EATER
	clearflag FLAG_GOT_ROUTE_14_AERIAL_ACE
	clearflag FLAG_HIDE_PEWTER_ROOT_FOSSIL
	clearflag FLAG_HIDE_PEWTER_CLAW_FOSSIL
	clearflag FLAG_HIDE_MTMOON_SILVER
	clearflag FLAG_GOT_TM_STEEL_WING
	clearflag FLAG_HIDE_CERULEANCAVE_GUARD
	clearflag FLAG_HIDE_MTSILVER_RED
	clearflag FLAG_HIDE_MEWTWO
	clearflag FLAG_HIDE_LATIAS
	clearflag FLAG_HIDE_LATIOS
	clearflag FLAG_HIDE_GROUDON
	clearflag FLAG_HIDE_KYOGRE
	clearflag FLAG_HIDE_RAYQUAZA

	clearflag FLAG_HIDE_CELADON_FALKNER
	clearflag FLAG_HIDE_VIRIDIAN_BUGSY
	clearflag FLAG_HIDE_DEPTSTORE_WHITNEY
	clearflag FLAG_HIDE_BELLCHIME_MORTY
	clearflag FLAG_HIDE_CAFE_JASMINE
	clearflag FLAG_HIDE_LAKE_PRYCE
	clearflag FLAG_HIDE_DEN_CLAIR

	setvar VAR_KANTO_ROCKET_STORY_STATE, 0
	setvar VAR_BILLS_GRANDPA, 0
	setvar VAR_VERMILION_CITY_STEVEN, 0
	setvar VAR_OAK_MT_SILVER_CALL, 0
	setvar VAR_VIRIDIAN_FOREST_PICHU, 0
	setvar VAR_FAN_CLUB_CLEFAIRY, 0
	setvar VAR_FAN_CLUB_GUY, 0
	setvar VAR_CLEFAIRY_DOLL_STATE, 0
	setvar VAR_NUM_BADGES, 8
	setvar VAR_VERMILION_CITY_STATE, 1
	setvar VAR_KANTO_SAFARI_ZONE_PROGRESS, 0
	clearflag FLAG_IN_KANTO_SAFARI_ZONE
	setvar VAR_BAOBA_QUEST_STATE, 0
	setvar VAR_CINNABAR_ISLAND_STATE, 0
	setvar VAR_MT_SILVER_STATE, 0
	setvar VAR_PALLETTOWN_LABSTATE, 0
	clearflag FLAG_HIDE_LEAGUE_BLACKBELT

	setflag FLAG_HIDE_DOJO_FALKNER
	setflag FLAG_HIDE_DOJO_BUGSY
	setflag FLAG_HIDE_DOJO_WHITNEY
	setflag FLAG_HIDE_DOJO_MORTY
	setflag FLAG_HIDE_DOJO_CHUCK
	setflag FLAG_HIDE_DOJO_JASMINE
	setflag FLAG_HIDE_DOJO_PRYCE
	setflag FLAG_HIDE_DOJO_CLAIR
	setflag FLAG_HIDE_DOJO_BROCK
	setflag FLAG_HIDE_DOJO_MISTY
	setflag FLAG_HIDE_DOJO_SURGE
	setflag FLAG_HIDE_DOJO_ERIKA
	setflag FLAG_HIDE_DOJO_JANINE
	setflag FLAG_HIDE_DOJO_SABRINA
	setflag FLAG_HIDE_DOJO_BLAINE
	setflag FLAG_HIDE_DOJO_BLUE

	setflag FLAG_EXTENDED_CONTENT_111
Common_EventScript_PJRInitKanto_Return:
	return

Common_EventScript_PJRInitKanto_MarkExisting:
	setflag FLAG_EXTENDED_CONTENT_111
	return
