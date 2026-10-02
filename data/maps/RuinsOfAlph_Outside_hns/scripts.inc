RuinsOfAlph_Outside_hns_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, RuinsOfAlph_Outside_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, SetTimeEncounters
	.byte 0

RuinsOfAlph_Outside_OnTransition: 
	callnative SetTimeBasedEncounters
	end	

RuinsOfAlph_Outside_EventScript_Quagsire::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_QUAGSIRE, CRY_MODE_NORMAL
	msgbox RuinsOfAlph_Outside_Text_Quagsire, MSGBOX_DEFAULT
	waitmoncry
	release
	end

RuinsOfAlph_Outside_Text_Quagsire:
	.string "QUAGSIRE: Quag Quag$"

RuinsOfAlph_Outside_EventScript_Stan::
	trainerbattle_single TRAINER_STAN_HNS, RuinsOfAlph_Outside_Text_SuperNerdStan_Seen, RuinsOfAlph_Outside_Text_SuperNerdStan_Beaten
	msgbox RuinsOfAlph_Outside_Text_SuperNerdStan_After, MSGBOX_AUTOCLOSE
	end

RuinsOfAlph_Outside_EventScript_Nathan::
	trainerbattle_single TRAINER_NATHAN_HNS, RuinsOfAlph_Outside_Text_PsychicNathan_Seen, RuinsOfAlph_Outside_Text_PsychicNathan_Beaten
	msgbox RuinsOfAlph_Outside_Text_PsychicNathan_After, MSGBOX_AUTOCLOSE
	end

RuinsOfAlph_Outside_EventScript_Youngster1::
	lock
	faceplayer
	msgbox RuinsOfAlph_Outside_Text_Youngster1, MSGBOX_DEFAULT
	closemessage
	release
	end

RuinsOfAlph_Outside_EventScript_Youngster2::
	lock
	faceplayer
	msgbox RuinsOfAlph_Outside_Text_Youngster2, MSGBOX_DEFAULT
	closemessage
	release
	end

RuinsOfAlph_Outside_EventScript_Fisher1::
	lock
	faceplayer
	msgbox RuinsOfAlph_Outside_Text_Fisher1, MSGBOX_DEFAULT
	closemessage
	release
	end

RuinsOfAlph_Outside_EventScript_Fisher2::
	lock
	faceplayer
	msgbox RuinsOfAlph_Outside_Text_Fisher2, MSGBOX_DEFAULT
	closemessage
	release
	end

RuinsOfAlph_Outside_EventScript_Sign1::
	lock
	msgbox RuinsOfAlph_Outside_Text_MainSign, MSGBOX_SIGN
	closemessage
	release
	end

RuinsOfAlph_Outside_EventScript_Sign2::
	lock
	msgbox RuinsOfAlph_Outside_Text_ResearchSign, MSGBOX_SIGN
	closemessage
	release
	end

RuinsOfAlph_Outside_EventScript_Sign3::
	lock
	msgbox RuinsOfAlph_Outside_Text_MysteryChamberSign, MSGBOX_SIGN
	closemessage
	release
	end

RuinsOfAlph_Outside_Text_Scientist:
	.string "Hm? That's a POKéDEX, isn't it?\p"
	.string "These wall shapes match UNOWN,\n"
	.string "but our instruments react too.\p"
	.string "A pulse runs through the stone.\n"
	.string "We call it RESONANCE.\p"
	.string "If UNOWN are part of it, your\n"
	.string "POKéDEX may help us understand.$"

RuinsOfAlph_Outside_Text_SuperNerdStan_Seen:
	.string "What do you want? I'm studying--\n"
	.string "don't disturb me!$"

RuinsOfAlph_Outside_Text_SuperNerdStan_Beaten:
	.string "Sorry…\n"
	.string "I'm frustrated by our lack of\p"
	.string "real understanding…$"

RuinsOfAlph_Outside_Text_SuperNerdStan_After:
	.string "The RUINS are about 1500\n"
	.string "years old.\p"
	.string "Recently the stone began giving\n"
	.string "off measurable RESONANCE.\p"
	.string "Nobody knows why it woke now.\n"
	.string "That's driving me mad!$"

RuinsOfAlph_Outside_Text_PsychicNathan_Seen:
	.string "Hmmm… This is a strange place.$"

RuinsOfAlph_Outside_Text_PsychicNathan_Beaten:
	.string "…$"

RuinsOfAlph_Outside_Text_PsychicNathan_After:
	.string "Something here is listening.\p"
	.string "Not a voice exactly...\n"
	.string "more like a thought.$"

RuinsOfAlph_Outside_Text_MysteryChamberSign:
	.string "MYSTERY STONE PANEL CHAMBER$"

RuinsOfAlph_Outside_Text_MainSign:
	.string "RUINS OF ALPH\n"
	.string "VISITORS WELCOME$"

RuinsOfAlph_Outside_Text_ResearchSign:
	.string "RUINS OF ALPH RESEARCH CENTER\p"
	.string "UNOWN - RELICS - RESONANCE$"

RuinsOfAlph_Outside_Text_Fisher1:
	.string "We heard the RUINS humming\n"
	.string "under our feet.\p"
	.string "Then every POKéMON nearby went\n"
	.string "completely still.\p"
	.string "We ran. Wouldn't you?$"

RuinsOfAlph_Outside_Text_Fisher2:
	.string "The RUINS hide a huge secret!\p"
	.string "The researchers keep saying\n"
	.string "RESONANCE.\p"
	.string "Sounds important, right?$"

RuinsOfAlph_Outside_Text_Youngster1:
	.string "UNOWN react when the old stones\n"
	.string "start humming.\p"
	.string "Maybe they're reading us back!$"

RuinsOfAlph_Outside_Text_Youngster2:
	.string "V... O... I... C... E...\p"
	.string "These old symbols keep spelling\n"
	.string "VOICE. Weird, huh?$"
