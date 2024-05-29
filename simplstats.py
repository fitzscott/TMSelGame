import genTMgameopts as gtgo
import os
import statistics as stats

def all_stats(metric, ky, lbl):
    mnmetr = stats.mean(metric)
    minmetr = min(metric)
    maxmetr = max(metric)
    medmetr = stats.median(metric)
    cnt = len(metric)
    # print(f"{ky} had {lbl} minimum {minmetr}, maximum {maxmetr}, average {mnmetr:.3f}, median {medmetr} over {cnt} games")
    return (mnmetr, minmetr, maxmetr, medmetr, cnt)

def prnrow(ky, mtrc, msrs, first=False):
    rowspan = "3"
    algn = ' align="right"'
    if first:
        print(f'<tr><td rowspan="{rowspan}">{ky}</td><td>{mtrc}</td>')
    else:
        print(f'<tr><td>{mtrc}</td>')
    nummsrs = len(msrs)
    for msridx in range(nummsrs):
        if len(str(msrs[msridx])) > 4:
            prnmsr = f"{msrs[msridx]:.3f}"
        else:
            prnmsr = msrs[msridx]
        # print(f'<td>{prnmsr}</td>')
        # make # of games pretty - same across all metrics
        if msridx == nummsrs - 1 and first:
            print(f'<td rowspan="{rowspan}"{algn}>{prnmsr}</td>')
        elif msridx != nummsrs - 1:
            print(f'<td{algn}>{prnmsr}</td>')
    print("</tr>")

def gen_stats(bykey, lbl):
    metrix = ["Average", "Minimum", "Maximum", "Median"]
    print(f"<table border='1'><tr><th>{lbl}</th><th>Metric</th>")
    for metrc in metrix:
        print(f"<th>{metrc}</th>")
    print("<th>Game Count")
    print("</tr>")
    for ky in sorted(bykey.keys()):
        scorz = [bykey[ky][idx][0] for idx in range(len(bykey[ky]))]
        ranks = [bykey[ky][idx][1] for idx in range(len(bykey[ky]))]
        bested = [bykey[ky][idx][2] for idx in range(len(bykey[ky]))]
        scorstats = all_stats(scorz, ky, "score")
        prnrow(ky, "Score", scorstats, True)
        rankstats = all_stats(ranks, ky, "rank")
        prnrow(ky, "Rank", rankstats)
        bestedstats = all_stats(bested, ky, "bested")
        prnrow(ky, "Bested", bestedstats)
    print("</table>")
    print("<br><br>")

def plyr_cnt_per_game(gameresults):
    pcnts = {}
    for gmrs in gameresults:
        # game ID is index 0
        gameid = gmrs[0]
        pcnts[gameid] = pcnts.get(gameid, 0) + 1
    # print(pcnts)
    return pcnts

def simple_stats(gamerslts):
    # for each player, include stats:
    #   number of games, average rank, average & median score, number of corporations
    # for each corporation, same
    plyrz = {}
    corps = {}
    plyrcnts = plyr_cnt_per_game(gamerslts)
    for gmrs in gamerslts:
        # player is index 2, corporation is index 3
        plyr = gmrs[2]
        corp = gmrs[3]
        scor = int(gmrs[4])
        rank = int(gmrs[5])
        # game ID is index 0
        gameid = gmrs[0]
        bested_cnt = plyrcnts[gameid] - rank
        if plyr in plyrz.keys():
            plyrz[plyr].append((scor,rank,bested_cnt))
        else:
            plyrz[plyr] = [(scor,rank,bested_cnt)]
        if corp in corps.keys():
            corps[corp].append((scor,rank,bested_cnt))
        else:
            corps[corp] = [(scor,rank,bested_cnt)]
    gen_stats(plyrz, "Player")
    gen_stats(corps, "Corporation")

if __name__ == "__main__":
    datfilepath = os.environ.get("TMDATPATH", "./")
    gamerslts = gtgo.load_game_results(datfilepath)
    simple_stats(gamerslts)
