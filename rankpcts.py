import genTMgameopts as gtgo
import sys
import os

def placepcts(gmrs, corp_or_plyr="C"):
    # calculate the percentages of each place / rank for represented
    # corporations or players
    placements = {}
    for gmrs in gmrs:
        # player is index 2, corporation is index 3
        plyr = gmrs[2]
        corp = gmrs[3]
        rank = int(gmrs[5])
        if corp_or_plyr == "C":
            focus = corp
        else:
            focus = plyr
        if focus not in placements.keys():
            placements[focus] = [0,0,0,0,0]
        placements[focus][rank-1] += 1
    # print(str(placements))
    maxlen = max([len(fc) for fc in placements.keys()])
    for focus in placements.keys():
        tot = sum(placements[focus])
        pcts = [placements[focus][plc] / tot * 100.0
                for plc in range(len(placements[focus]))]
        disppcts = "\t".join([f"{pct:.2f}" for pct in pcts])
        print(f"{focus.ljust(maxlen+1)}\t{disppcts}")


if __name__ == "__main__":
    datfilepath = os.environ.get("TMDATPATH", "./")
    gamerslts = gtgo.load_game_results(datfilepath)
    if len(sys.argv) > 1:
        plyr_or_corp = sys.argv[1]
    else:
        plyr_or_corp = "C"
    placepcts(gamerslts, plyr_or_corp)
