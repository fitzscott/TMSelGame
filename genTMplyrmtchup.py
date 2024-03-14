import sys
import os
import itertools as it
import copy
import genTMgameopts as gtgo

def calc_min_max_cnt(list_len, num_games=2):
    print(f"Calculating for {num_games} games")
    if list_len % num_games == 0:
        mm = int(list_len / num_games)
        min_max = (mm, mm)
    else:
        mxcnt = int(list_len / num_games) + 1
        mncnt = int(list_len / num_games)
        min_max = (mncnt, mxcnt)
    return min_max

def nodupes(itprod):
    # print(str(itprod))
    prlen = len(itprod)
    for pridx in range(prlen-1):
        for plidx in itprod[pridx]:
            for nxtidx in range(prlen - pridx - 1):
                chkidx = pridx + nxtidx + 1
                # print(f"Comparing index {pridx} against index {chkidx} = {plidx} against {itprod[chkidx]}")
                if plidx in itprod[chkidx]:
                    return False
    return True

def make_plyr_product(siz_plyr_lst, min_max, combminmax):
    combolist = []
    sizallocd = 0
    while sizallocd < siz_plyr_lst:
        stilltogo = siz_plyr_lst - sizallocd
        if stilltogo % min_max[0] == 0: # one or multiple max
            use_min_or_max = 0
        elif stilltogo % min_max[1] == 0:   # one or multiple min
            use_min_or_max = 1
        else:
            use_min_or_max = 0
        print(f"appending combo for {min_max[use_min_or_max]} players")
        combolist.append(copy.deepcopy(combminmax[use_min_or_max]))
        sizallocd += min_max[use_min_or_max]
    # combcopy = copy.deepcopy(combminmax[1])
    # combolist = [combminmax[0], combminmax[1], combcopy]
    # for combo in combolist:
    #     print("    Combo List:")
    #     for c in combo:
    #         print(str(c))
    retval = [cprod for cprod in it.product(*combolist)
              if nodupes(cprod)]
    return retval

def plyr_combos(plyr_id_lst, num_games=2):
    print(str(plyr_id_lst))
    min_max = calc_min_max_cnt(len(plyr_id_lst), num_games)
    print(str(min_max))
    # Starting out assuming we have 2 games, but planning to refine later
    combmax = it.combinations(plyr_id_lst, min_max[0])
    combmin = it.combinations(plyr_id_lst, min_max[1])
    legit_matchups = make_plyr_product(len(plyr_id_lst), min_max, (combmax, combmin))
    # for leg_mu in legit_matchups:
    #     print(str(leg_mu))
    return legit_matchups

def score_match_ups(plyrs, plyr_oppos_plyd, match_ups):
    plyopplyidxs = {}
    for popnm in plyr_oppos_plyd.keys():
        plyopplyidxs[plyrs.index(popnm)] = [plyrs.index(oppnm)
                                            for oppnm in plyr_oppos_plyd[popnm]]
    # print(f"player opponent indices {plyopplyidxs}")
    scores = []
    for mu in match_ups:
        score = 0
        for gm in mu:
            # print(f"Checking game {gm} in match-up {mu}")
            for plyridx in range(len(plyrs)):
                if plyridx not in gm:
                    # print(f"player {plyridx} not found in {gm}")
                    continue
                if plyridx not in plyopplyidxs.keys():
                    continue
                for oppo in plyopplyidxs[plyridx]:
                    if oppo in gm:
                        score += 1
        scores.append(score)
    return scores

def prnplyrsingames(plyrs, match_up):
    for muidx in range(len(match_up)):
        print(f"    game {muidx+1}:")
        for plidx in match_up[muidx]:
            print(f"{plidx}: {plyrs[plidx]}")

if __name__ == "__main__":
    datfilepath = os.environ.get("TMDATPATH", "./")
    gamerslts = gtgo.load_game_results(datfilepath)
    plyr_oppos_plyd = gtgo.player_oppos_played(gamerslts)
    for plnm in plyr_oppos_plyd.keys():
        oppolist = " & ".join(plyr_oppos_plyd[plnm])
        print(f"{plnm} has played {oppolist}")
    plyrs = sorted(list(set([gmrs[2] for gmrs in gamerslts])))
    for pidx in range(len(plyrs)):
        print(f"{pidx}\t{plyrs[pidx]}")
    if len(sys.argv) < 2:
        print(f"usage: python {sys.argv[0]} comma-separated-list-of-player-indices [#-of-games=2]")
        sys.exit(-1)
    plyr_id_lst = [int(pid) for pid in sys.argv[1].split(",")]
    if len(sys.argv) >= 3:
        num_games = int(sys.argv[2])
    else:
        num_games = 2
    match_ups = plyr_combos(plyr_id_lst, num_games)
    match_up_scores = score_match_ups(plyrs, plyr_oppos_plyd, match_ups)
    # for scidx in range(len(match_up_scores)):
    #     print(f"score for {match_ups[scidx]} = {match_up_scores[scidx]}")
    min_scor = min(match_up_scores)
    solnnum = 0
    for scidx in range(len(match_up_scores)):
        if match_up_scores[scidx] == min_scor:
            print(f"Solution {solnnum+1}")
            prnplyrsingames(plyrs, match_ups[scidx])
            print(40 * "-")
            solnnum += 1