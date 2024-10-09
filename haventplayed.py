import os
import genTMgameopts as gtgo
import sys

def corps_not_played(corps, gmrs, played):
    plyrz = sorted(list(set([gr[2] for gr in gmrs])))
    corps_plyd_plyrz = gtgo.player_corps_played(plyrz, gmrs)
    corps_notplyd_plyrz = {}
    for plyr in corps_plyd_plyrz.keys():
        if played:
            print(f"{plyr} has played {' '.join(corps_plyd_plyrz[plyr])}")
        else:
            for corp in corps.keys():
                if corp not in corps_plyd_plyrz[plyr]:
                    if plyr in corps_notplyd_plyrz.keys():
                        corps_notplyd_plyrz[plyr].append(corp)
                    else:
                        corps_notplyd_plyrz[plyr] = [corp]
            if plyr in corps_notplyd_plyrz.keys():
                print(f"{plyr} has not played {' '.join(corps_notplyd_plyrz[plyr])}")
            else:
                print(f"{plyr} has played all corporations")
    plyrnamez = gtgo.load_players(datfilepath)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        played = sys.argv[1] == "1"
    else:
        played = False
    datfilepath = os.environ.get("TMDATPATH", "./")
    corps = gtgo.load_corps(datfilepath)
    gamerslts = gtgo.load_game_results(datfilepath)
    corps_not_played(corps, gamerslts, played)
