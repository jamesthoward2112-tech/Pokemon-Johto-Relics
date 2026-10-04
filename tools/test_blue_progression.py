"""Behaviour checks for Blue's Cinnabar/gym/Dojo progression.
Executes the real map scripts with field/UI commands recorded at their boundary.
Trainer battles stop at entry; victory checks explicitly resume after a win.
"""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

class FieldScript:
    def __init__(self, flags=(), badges=15, win=False):
        self.flags=set(flags)
        self.vars={"VAR_NUM_BADGES":badges}
        self.messages=[]
        self.removed=[]
        self.battles=[]
        self.rewards=[]
        self.win=win
        self.code=[]
        self.labels={}
        for name in ("CinnabarIsland_hns", "ViridianCity_Gym_hns"):
            for raw in (ROOT/"data/maps"/name/"scripts.inc").read_text(encoding="utf-8").splitlines():
                line=raw.split("@")[0].strip()
                if not line: continue
                if re.fullmatch(r"\w+::?",line):
                    self.labels[line.rstrip(":")]=len(self.code)
                else: self.code.append(line)
    def transition(self, mapname):
        text=(ROOT/"data/maps"/mapname/"scripts.inc").read_text(encoding="utf-8")
        header=text.split(".byte 0",1)[0]
        m=re.search(r"map_script MAP_SCRIPT_ON_TRANSITION, (\w+)",header)
        if m: self.run(m[1])
    def run(self,label):
        pc=self.labels[label]
        for _ in range(250):
            line=self.code[pc]; pc+=1
            cmd,_,tail=line.partition(" ")
            a=[s.strip() for s in tail.split(",")]
            if cmd=="end": return
            if cmd=="goto": pc=self.labels[a[0]]
            elif cmd in ("goto_if_set","goto_if_unset"):
                if (a[0] in self.flags)==(cmd=="goto_if_set"): pc=self.labels[a[1]]
            elif cmd in ("goto_if_eq","goto_if_ge"):
                value=self.vars.get(a[0],0); other=int(a[1],0)
                if (value==other if cmd=="goto_if_eq" else value>=other): pc=self.labels[a[2]]
            elif cmd=="setflag": self.flags.add(a[0])
            elif cmd=="clearflag": self.flags.discard(a[0])
            elif cmd=="setvar": self.vars[a[0]]=int(a[1],0)
            elif cmd=="addvar": self.vars[a[0]]=self.vars.get(a[0],0)+int(a[1],0)
            elif cmd in ("message","msgbox"): self.messages.append(a[0])
            elif cmd=="removeobject": self.removed.append(a[0])
            elif cmd=="giveitem": self.rewards.append(a[0])
            elif cmd=="trainerbattle_no_intro":
                self.battles.append(a[0])
                if not self.win: return
            elif cmd in ("lock","lockall","release","releaseall","faceplayer","closemessage","waitmessage","fadescreenswapbuffers","callnative"):
                pass
            elif cmd=="call" and a[0] in ("Common_EventScript_PlayGymBadgeFanfare","Common_EventScript_SetGymTrainers_hns"):
                pass
            else: raise AssertionError("Unhandled executed command: "+line)
        raise AssertionError("Script did not terminate")

DEFEATED="FLAG_DEFEATED_VIRIDIAN_GYM"
DOJO="FLAG_HIDE_DOJO_BLUE"
GYM="FLAG_HIDE_VIRIDIAN_BLUE"
CINNABAR="FLAG_HIDE_CINNABAR_BLUE"
BADGE="FLAG_BADGE16_GET"

class BlueProgression(unittest.TestCase):
    def test_legitimately_invited_blue_battles_even_with_stale_dojo_flag(self):
        s=FieldScript([CINNABAR,DOJO])
        s.run("ViridianCity_Gym_EventScript_Blue")
        self.assertEqual(s.battles,["TRAINER_BLUE_HNS"])
        self.assertNotIn(BADGE,s.flags)
    def test_stale_early_blue_cannot_battle_and_is_removed(self):
        s=FieldScript([DOJO],badges=8)
        s.run("ViridianCity_Gym_EventScript_Blue")
        self.assertEqual(s.battles,[])
        self.assertIn(GYM,s.flags)
        self.assertIn("LOCALID_VIRIDIAN_BLUE",s.removed)
    def test_cinnabar_stale_blue_sends_existing_winner_to_dojo(self):
        s=FieldScript([DEFEATED,BADGE,DOJO],badges=15)
        s.run("CinnabarIsland_EventScript_Blue")
        self.assertIn(CINNABAR,s.flags)
        self.assertIn(GYM,s.flags)
        self.assertNotIn(DOJO,s.flags)
        self.assertIn("LOCALID_CINNABAR_BLUE",s.removed)
        self.assertEqual(s.battles,[])
    def test_cinnabar_hides_old_copy_on_map_entry(self):
        s=FieldScript([DEFEATED,BADGE,DOJO],badges=14)
        s.transition("CinnabarIsland_hns")
        self.assertIn(CINNABAR,s.flags)
    def test_unbeaten_invitation_accepts_at_least_fifteen_badges(self):
        for badges in (15,16):
            s=FieldScript([GYM,DOJO],badges=badges)
            s.run("CinnabarIsland_EventScript_Blue")
            self.assertNotIn(GYM,s.flags)
            self.assertIn(CINNABAR,s.flags)
    def test_unbeaten_below_fifteen_does_not_invite(self):
        s=FieldScript([GYM,DOJO],badges=14)
        s.run("CinnabarIsland_EventScript_Blue")
        self.assertIn(GYM,s.flags)
        self.assertNotIn(CINNABAR,s.flags)
    def test_gym_invitation_removes_blue_and_opens_dojo(self):
        s=FieldScript([DEFEATED,BADGE,DOJO])
        s.run("ViridianCity_Gym_EventScript_Blue")
        self.assertIn(GYM,s.flags)
        self.assertIn(CINNABAR,s.flags)
        self.assertNotIn(DOJO,s.flags)
        self.assertIn("LOCALID_VIRIDIAN_BLUE",s.removed)
        self.assertEqual(s.rewards,[])
    def test_early_unbeaten_blue_is_hidden_on_gym_entry(self):
        s=FieldScript([DOJO],badges=8)
        s.transition("ViridianCity_Gym_hns")
        self.assertIn(GYM,s.flags)
    def test_legitimate_cinnabar_invitation_keeps_blue_visible(self):
        s=FieldScript([CINNABAR,DOJO],badges=15)
        s.transition("ViridianCity_Gym_hns")
        self.assertNotIn(GYM,s.flags)
    def test_already_invited_save_repairs_gym_copy_on_entry(self):
        s=FieldScript([DEFEATED,BADGE])
        s.transition("ViridianCity_Gym_hns")
        self.assertIn(GYM,s.flags)
    def test_already_loaded_stale_gym_copy_can_still_leave(self):
        s=FieldScript([DEFEATED,BADGE])
        s.run("ViridianCity_Gym_EventScript_Blue")
        self.assertIn("LOCALID_VIRIDIAN_BLUE",s.removed)
        self.assertIn(GYM,s.flags)
    def test_first_win_awards_once_and_hides_cinnabar_copy(self):
        s=FieldScript([CINNABAR,DOJO],win=True)
        s.run("ViridianCity_Gym_EventScript_Blue")
        self.assertEqual(s.battles,["TRAINER_BLUE_HNS"])
        self.assertEqual(s.rewards,["ITEM_TM_TRICK_ROOM"])
        self.assertEqual(s.vars["VAR_NUM_BADGES"],16)
        self.assertTrue({DEFEATED,BADGE,CINNABAR}.issubset(s.flags))
        s.run("ViridianCity_Gym_EventScript_Blue")
        self.assertEqual(len(s.battles),1)
        self.assertEqual(s.vars["VAR_NUM_BADGES"],16)
        self.assertEqual(len(s.rewards),1)

if __name__=="__main__": unittest.main(verbosity=2)
