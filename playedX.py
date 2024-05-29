import genTMgameopts as gtgo
import sys
import os

def disp_corps_plyd(corps, gmrs):
    plyrz = sorted(list(set([gr[2] for gr in gmrs])))
    corps_plyd_plyrz = gtgo.player_corps_played(plyrz, gmrs)
    # print(str(corps_plyd_plyrz))
    corpkys = sorted(corps.keys())
    print("Player\t" + "\t".join([corps[ck] for ck in corpkys]))
    for plyr in plyrz:
        print(plyr + "\t" + "\t".join(["X" if ck in corps_plyd_plyrz[plyr]
                                       else " "for ck in corpkys]))

if __name__ == "__main__":
    datfilepath = os.environ.get("TMDATPATH", "./")
    corps = gtgo.load_corps(datfilepath)
    gamerslts = gtgo.load_game_results(datfilepath)
    disp_corps_plyd(corps, gamerslts)
