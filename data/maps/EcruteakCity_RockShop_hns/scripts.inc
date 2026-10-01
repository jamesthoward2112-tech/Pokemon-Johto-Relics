EcruteakCity_RockShop_hns_MapScripts::
	.byte 0

@ Azul Agua / Water Blue inspired Rock Shop.
@ Keep PJR progression/economy; visuals are ported separately from the donor asset bank.
EcruteakCity_RockShop_EventScript_Clerk::
	lock
	faceplayer
	goto_if_set FLAG_BADGE04_GET, EcruteakCity_RockShop_EventScript_ClerkAdvanced
	message gText_HowMayIServeYou
	waitmessage
	pokemart EcruteakCity_RockShop_Basic
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

EcruteakCity_RockShop_EventScript_ClerkAdvanced::
	message gText_HowMayIServeYou
	waitmessage
	pokemart EcruteakCity_RockShop_Advanced
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

EcruteakCity_RockShop_EventScript_Collector::
	lock
	faceplayer
	msgbox EcruteakCity_RockShop_Text_Collector, MSGBOX_DEFAULT
	closemessage
	release
	end

	.align 2
EcruteakCity_RockShop_Basic:
	.2byte ITEM_FIRE_STONE
	.2byte ITEM_WATER_STONE
	.2byte ITEM_THUNDER_STONE
	.2byte ITEM_LEAF_STONE
	.2byte ITEM_ICE_STONE
	.2byte ITEM_MOON_STONE
	.2byte ITEM_SUN_STONE
	pokemartlistend

	.align 2
EcruteakCity_RockShop_Advanced:
	.2byte ITEM_FIRE_STONE
	.2byte ITEM_WATER_STONE
	.2byte ITEM_THUNDER_STONE
	.2byte ITEM_LEAF_STONE
	.2byte ITEM_ICE_STONE
	.2byte ITEM_MOON_STONE
	.2byte ITEM_SUN_STONE
	.2byte ITEM_SHINY_STONE
	.2byte ITEM_DUSK_STONE
	.2byte ITEM_DAWN_STONE
	pokemartlistend

EcruteakCity_RockShop_Text_Collector:
	.string "These stones have been gathered\n"
	.string "from all across JOHTO.\p"
	.string "Some seem to react strangely near\n"
	.string "ECRUTEAK's old towers...$"
