IcePath_B2F_hns_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, IcePath_B2F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, SetTimeEncounters
	.byte 0

IcePath_B2F_OnTransition:
	@ Self-heal old saves and keep the Crystal-style boulder state consistent.
	@ If a B1F boulder has fallen (source flag set), its B2F counterpart must be visible.
	goto_if_unset FLAG_HIDE_ICEPATH_B1F_BOULDER1, IcePath_B2F_CheckBoulder2
	clearflag FLAG_HIDE_ICEPATH_B2F_BOULDER1
IcePath_B2F_CheckBoulder2::
	goto_if_unset FLAG_HIDE_ICEPATH_B1F_BOULDER2, IcePath_B2F_CheckBoulder3
	clearflag FLAG_HIDE_ICEPATH_B2F_BOULDER2
IcePath_B2F_CheckBoulder3::
	goto_if_unset FLAG_HIDE_ICEPATH_B1F_BOULDER3, IcePath_B2F_CheckBoulder4
	clearflag FLAG_HIDE_ICEPATH_B2F_BOULDER3
IcePath_B2F_CheckBoulder4::
	goto_if_unset FLAG_HIDE_ICEPATH_B1F_BOULDER4, IcePath_B2F_BoulderSyncDone
	clearflag FLAG_HIDE_ICEPATH_B2F_BOULDER4
IcePath_B2F_BoulderSyncDone::
	callnative SetTimeBasedEncounters
	end

IcePath_B2F_EventScript_Item_FullHeal::
	finditem ITEM_FULL_HEAL
	end

IcePath_B2F_EventScript_Item_MaxPotion::
	finditem ITEM_MAX_POTION
	end

IcePath_B2F_EventScript_Item_Carbos::
	finditem ITEM_CARBOS
	end
