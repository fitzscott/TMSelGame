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

def prnrow(ky, mtrc, msrs):
    print(f"<tr><td>{ky}</td><td>{mtrc}</td>")
    for msr in msrs:
        if len(str(msr)) > 4:
            prnmsr = f"{msr:.3f}"
        else:
            prnmsr = msr
        print(f"<td>{prnmsr}</td>")
    print("</tr>")

def gen_stats(bykey, lbl):
    metrix = ["Average", "Minimum", "Maximum", "Median"]
    print(f"<table><tr><th>{lbl}</th><th>Metric</th>")
    for metrc in metrix:
        print(f"<th>{metrc}</th>")
    print("<th>Number of games")
    print("</tr>")
    for ky in bykey.keys():
        scorz = [bykey[ky][idx][0] for idx in range(len(bykey[ky]))]
        ranks = [bykey[ky][idx][1] for idx in range(len(bykey[ky]))]
        scorstats = all_stats(scorz, ky, "score")
        prnrow(ky, "Score", scorstats)
        rankstats = all_stats(ranks, ky, "rank")
        prnrow(ky, "Rank", rankstats)
    print("</table>")
    print("<br><br>")

def simple_stats(gamerslts):
    # for each player, include stats:
    #   number of games, average rank, average & median score, number of corporations
    # for each corporation, same
    plyrz = {}
    corps = {}
    for gmrs in gamerslts:
        # player is index 2, corporation is index 3
        plyr = gmrs[2]
        corp = gmrs[3]
        scor = int(gmrs[4])
        rank = int(gmrs[5])
        if plyr in plyrz.keys():
            plyrz[plyr].append((scor,rank))
        else:
            plyrz[plyr] = [(scor,rank)]
        if corp in corps.keys():
            corps[corp].append((scor,rank))
        else:
            corps[corp] = [(scor,rank)]
    gen_stats(plyrz, "Player")
    gen_stats(corps, "Corporation")

if __name__ == "__main__":
    datfilepath = os.environ.get("TMDATPATH", "./")
    gamerslts = gtgo.load_game_results(datfilepath)
    simple_stats(gamerslts)
