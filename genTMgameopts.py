import sys
# import random
import itertools as it
import os

def load_corps(datfilepath):
    corps = {}
    flnm = datfilepath + "corpsa.tsv"
    fl = open(flnm)
    for ln in fl:
        (corp_nm, corp_id) = ln.strip().split('\t')
        corps[corp_id] = corp_nm
    fl.close()
    return (corps)

def load_players(datfilepath):
    plyrs = {}
    flnm = datfilepath + "players.tsv"
    fl = open(flnm)
    for ln in fl:
        flds = ln.strip().split('\t')
        plyrs[flds[0]] = flds[3]
    fl.close()
    return (plyrs)

def corp_combos(corps):
    # generate all 2-corporation combinations that the players can choose between
    comb = it.combinations(list(corps.keys()), 2)
    return comb

def load_game_results(datfilepath):
    flnm = datfilepath + "gameResults1a.tsv"
    fl = open(flnm)
    gmrslts = [ln.strip().split('\t') for ln in fl.readlines()]
    fl.close()
    return gmrslts

def player_corps_played(plyrz, game_rslts):
    # for each player, list the corporations they've played
    corps_played = {}
    for gr in game_rslts:
        plyr = gr[2]
        # print(f"game {gr[0]} had player {plyr}")
        if plyr in plyrz:
            corp = gr[3]
            # print(f"adding corp {corp} to player {plyr}")
            if plyr not in corps_played.keys():
                corps_played[plyr] = [corp]
            else:
                corps_played[plyr].append(corp)
    reord_corps_played = {player: corps_played[player] for player in plyrz}
    return reord_corps_played

# def gen_plyr_corp_combos(plyrs, corpcombs):
#     pcc = it.product(plyrs, corpcombs)
#     return pcc

def player_oppos_played(game_rslts):
    game_plyrz = {}
    plyr_oppos = {}
    for gr in game_rslts:
        game_id = gr[0]
        plyr_id = gr[2]
        # print(f"player {plyr_id} played in game {game_id}")
        if game_id not in game_plyrz.keys():
            game_plyrz[game_id] = [plyr_id]
        else:
            game_plyrz[game_id].append(plyr_id)
    # print(str(game_plyrz))
    for game_id in game_plyrz.keys():
        for plyr in game_plyrz[game_id]:
            oppos = [oppo for oppo in game_plyrz[game_id] if oppo != plyr]
            if plyr not in plyr_oppos.keys():
                plyr_oppos[plyr] = [oppo for oppo in oppos]
            else:
                plyr_oppos[plyr].extend(oppos)
    for plyr in plyr_oppos.keys():
        plyr_oppos[plyr] = list(set(plyr_oppos[plyr]))
        # print(f"player {plyr} has played {plyr_oppos[plyr]}")
    return plyr_oppos

def legit_game(game_combo):
    # for a combination of 2-corporation sets to make a potential game,
    # eliminate any that have the same corporation listed more than once.
    corp_cnts = {}
    retval = True
    for corp_combos in game_combo:
        for cidx in range(2):
            corp_cnts[corp_combos[cidx]] = corp_cnts.get(corp_combos[cidx], 0) + 1
    for cnt in corp_cnts.values():
        if cnt > 1:
            retval = False
            break
    return retval

def gen_game_combos(corp_comb, plyrcnt):
    # generate all potential games from corporation combinations
    game_combos = [gc for gc in it.product(corp_comb, repeat=plyrcnt) if legit_game(gc)]
    return game_combos

def score_game_combos(game_combos, ply_corps, plyr_oppos_plyd):
    # score each potential game (i.e. combination of 2-corporation sets) by the
    # players that will be participating.  Low scores are better, as they indicate
    # fewer players have corporations they have already played.
    scores = []
    plyr_ids = list(ply_corps.keys())
    for gc in game_combos:
        score = 0
        mult_plyr_corp_present = []
        for plyr_pos in range(len(plyr_ids)):
            for corp in ply_corps[plyr_ids[plyr_pos]]:
                # print(f"checking corp {corp} in game {gc} = player {plyr_ids[plyr_pos]} position {plyr_pos} {gc[plyr_pos]}")
                if corp in gc[plyr_pos]:
                    # multiple matches should score higher (worse)
                    if plyr_pos in mult_plyr_corp_present:
                        fctr = 10
                    else:
                        fctr = 1
                    score += 100 * fctr
                    mult_plyr_corp_present.append(plyr_pos)
            if plyr_oppos_plyd is not None:
                oppos = [plyr_id for plyr_id in plyr_ids if plyr_id != plyr_ids[plyr_pos]]
                for oppo in oppos:
                    if oppo in plyr_oppos_plyd[plyr_ids[plyr_pos]]:
                        score += 1
        scores.append(score)
    return scores

def show_plyr_corps_game(game, plyrz, corps):
    disppcg = [plyrz[pidx] + " " + ",".join(game[pidx])
               for pidx in range(len(plyrz))]
    return "; ".join(disppcg)

def find_corp_assgnmt(plyrs, plidxs, gamerslts, corps, corp_comb, max_solns):
    plyridxs = [int(pix) for pix in plidxs]
    curr_plyrz = [plyrs[cpix] for cpix in plyridxs]
    plyr_corps_plyd = player_corps_played(curr_plyrz, gamerslts)
    print(str(plyr_corps_plyd))
    plyr_oppos_plyd = player_oppos_played(gamerslts)
    game_combs = gen_game_combos(corp_comb, len(plyridxs))
    scores = score_game_combos(game_combs, plyr_corps_plyd, plyr_oppos_plyd)
    min_score = min(scores)
    match_cnt = 0
    print(f"number of scored combos = {len(scores)}, minimum score = {min_score}, number of game combos = {len(game_combs)}, max solutions shown = {max_solns}")
    for scidx in range(len(scores)):
        if scores[scidx] <= min_score:
            print(show_plyr_corps_game(game_combs[scidx], curr_plyrz, corps) + " - score: " + str(scores[scidx]))
            match_cnt += 1
        if match_cnt >= max_solns:
            break

def prn_plyrz(plyrz):
    plystrlen = 15
    scrnwid, scrnhi = os.get_terminal_size()
    idxprnlen = 3
    numplyrz2prn = scrnwid // (plystrlen + idxprnlen + 9)
    toprn = ""
    for pidx in range(len(plyrs)):
        idxprn = str(pidx).zfill(idxprnlen)
        toprn += f"{pidx} {plyrs[pidx].ljust(plystrlen)}\t"
        if (pidx + 1) % numplyrz2prn == 0:
            print(toprn)
            toprn = ""
    if toprn != "":
        print(toprn)

if __name__ == "__main__":
    datfilepath = os.environ.get("TMDATPATH", "./")
    corps = load_corps(datfilepath)
    corp_comb = corp_combos(corps)
    gamerslts = load_game_results(datfilepath)
    # print(f"found {len(gamerslts)} game results records")
    plyrs = sorted(list(set([gmrs[2] for gmrs in gamerslts])))
    prn_plyrz(plyrs)

    if len(sys.argv) < 2:
        print(f"usage: python {sys.argv[0]} comma-separated-list-of-player-indices [number-solutions=10]")
        sys.exit(-1)
    if len(sys.argv) < 3:
        max_solns = 10
    else:
        max_solns = int(sys.argv[2])

    find_corp_assgnmt(plyrs, sys.argv[1].split(","), gamerslts, corps, corp_comb, max_solns)
