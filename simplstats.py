import genTMgameopts as gtgo
import os
import statistics as stats

class simplstats():

    def __init__(self, gamerslts):
        self._gamerslts = gamerslts
        self._plyrcnts = {}
        self._gametotscore = {}

    def all_stats(self, metric, ky, lbl):
        mnmetr = stats.mean(metric)
        minmetr = min(metric)
        maxmetr = max(metric)
        medmetr = stats.median(metric)
        cnt = len(metric)
        # print(f"{ky} had {lbl} minimum {minmetr}, maximum {maxmetr}, average {mnmetr:.3f}, median {medmetr} over {cnt} games")
        return (mnmetr, minmetr, maxmetr, medmetr, cnt)

    def prnrow(self, ky, mtrc, msrs, first=False):
        rowspan = "4"
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

    def gen_stats(self, bykey, lbl):
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
            scorpct = [bykey[ky][idx][3] for idx in range(len(bykey[ky]))]
            scorstats = self.all_stats(scorz, ky, "score")
            self.prnrow(ky, "Score", scorstats, True)
            rankstats = self.all_stats(ranks, ky, "rank")
            self.prnrow(ky, "Rank", rankstats)
            bestedstats = self.all_stats(bested, ky, "bested")
            self.prnrow(ky, "Bested", bestedstats)
            scorpctstats = self.all_stats(scorpct, ky, "percent")
            self.prnrow(ky, "Score %", scorpctstats)
        print("</table>")
        print("<br><br>")

    def plyr_cnt_per_game(self):
        for gmrs in self._gamerslts:
            # game ID is index 0
            gameid = gmrs[0]
            # score is index 4
            scor = int(gmrs[4])
            self._plyrcnts[gameid] = self._plyrcnts.get(gameid, 0) + 1
            self._gametotscore[gameid] = self._gametotscore.get(gameid, 0) + scor

    def simple_stats(self):
        # for each player, include stats:
        #   number of games, average rank, average & median score, number of corporations
        # for each corporation, same
        plyrz = {}
        corps = {}
        self.plyr_cnt_per_game()
        for gmrs in self._gamerslts:
            # player is index 2, corporation is index 3
            plyr = gmrs[2]
            corp = gmrs[3]
            scor = int(gmrs[4])
            rank = int(gmrs[5])
            # game ID is index 0
            gameid = gmrs[0]
            bested_cnt = float(self._plyrcnts[gameid] - rank)
            # scale to a 4 player game
            scor_pct = float(scor) / float(self._gametotscore[gameid]) / 4.0 * self._plyrcnts[gameid] * 100.0
            if plyr in plyrz.keys():
                plyrz[plyr].append((scor,rank,bested_cnt,scor_pct))
            else:
                plyrz[plyr] = [(scor,rank,bested_cnt,scor_pct)]
            if corp in corps.keys():
                corps[corp].append((scor,rank,bested_cnt,scor_pct))
            else:
                corps[corp] = [(scor,rank,bested_cnt,scor_pct)]
        self.gen_stats(plyrz, "Player")
        self.gen_stats(corps, "Corporation")

if __name__ == "__main__":
    datfilepath = os.environ.get("TMDATPATH", "./")
    gamerslts = gtgo.load_game_results(datfilepath)
    ss = simplstats(gamerslts)
    ss.simple_stats()
