import asyncio
import time

from utilities import *
import random
import itertools

NUM_MOVES = 16
indexes = list(itertools.product([0, 1, 2, 3], [0, 1, 2, 3]))
print(indexes)
print(random.shuffle(indexes))

letterT = [[0,0], [0,1], [0,2], [1,1], [2,1], [3,1]]
letterI = [[0,1], [1,1], [2,1], [3,1]]
letterC = [[0,0], [0,1], [0,2], [1,0], [2,0], [3,0], [3,1], [3,2]]
letterA = [[0,1],[1,0],[1,1],[1,2],[2,0],[2,2],[3,0],[3,2]]
letterO = [[0,0],[0,1],[0,2],[1,0],[1,2],[2,0],[2,2],[3,0],[3,1],[3,2]]
letterE = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[3,0],[3,1],[3,2]]


def gen_move_sequence(num_moves = NUM_MOVES, index_list = indexes):
    inds = index_list.copy()
    moves = []
    for _ in range(NUM_MOVES):
        #inds = indexes.copy()
        ind = random.choice(inds)
        inds.remove(ind)
        moves.append(ind)
    return moves

def gen_move_sequence_shuffle(num_moves = NUM_MOVES, index_list = indexes):
    random.shuffle(indexes)
    return indexes

def you_won(mv_list, win_count=4):
    won = False
    positions = [0, 1, 2, 3]
    ind1 = [mv[0] for mv in mv_list]
    ind2 = [mv[1] for mv in mv_list]
    for val in positions:
        if max(ind1.count(val), ind2.count(val)) >= win_count:
            won = True
    # Check diagnol:
    diag_list = [(x,x) for x in range(win_count)]
    if set(diag_list).issubset(mv_list):
        won = True
    return won

#await asyncio.sleep(5)
letterOnFor = 1
epBlast = 1

async def tictactoe(lights):
    # print(lights)
    for i in range(16):
        lights[(i % 16)].set_state(off)


    #white epilepsy blast
    '''
    for eb in range(5):
        for i in range(15):
            #whichLight = index(i)
            lights[i].set_state(rgb(255,255,255))

        await asyncio.sleep(epBlast)
        reset_all(lights)
    '''

    #show letter t
    for i in letterT:
        whichLight = index(i)
        lights[whichLight].set_state(rgb(40,90,185))

    await asyncio.sleep(letterOnFor)
    reset_all(lights)

    for i in letterI:
        whichLight = index(i)
        lights[whichLight].set_state(rgb(40,90,185))

    await asyncio.sleep(letterOnFor)
    reset_all(lights)

    for i in letterC:
        whichLight = index(i)
        lights[whichLight].set_state(rgb(40,90,185))

    await asyncio.sleep(letterOnFor)
    reset_all(lights)

    for i in letterT:
        whichLight = index(i)
        lights[whichLight].set_state(rgb(10,10,10))

    await asyncio.sleep(letterOnFor)
    reset_all(lights)

    for i in letterA:
        whichLight = index(i)
        lights[whichLight].set_state(rgb(10,10,10))

    await asyncio.sleep(letterOnFor)
    reset_all(lights)

    for i in letterC:
        whichLight = index(i)
        lights[whichLight].set_state(rgb(10,10,10))

    await asyncio.sleep(letterOnFor)
    reset_all(lights)

    for i in letterT:
        whichLight = index(i)
        lights[whichLight].set_state(rgb(0,50,150))

    await asyncio.sleep(letterOnFor)
    reset_all(lights)

    for i in letterO:
        whichLight = index(i)
        lights[whichLight].set_state(rgb(0,50,150))

    await asyncio.sleep(letterOnFor)
    reset_all(lights)

    for i in letterE:
        whichLight = index(i)
        lights[whichLight].set_state(rgb(0,50,150))

    await asyncio.sleep(letterOnFor)
    reset_all(lights)

    loop = PeriodicLoop(.5)

    i = 0

    #moves = gen_move_sequence()
    #print(moves)
    #print('shuffle ver')
    moves = gen_move_sequence_shuffle()
    print(moves)

    pcolor = [(255,0,0), (0,0,255)]

    #print tic tac toe!
    p0_moves = moves[::2]
    p1_moves = moves[1::2]
    print(p0_moves)
    print(p1_moves)

    p0cnt=0
    p1cnt=0
    while i<NUM_MOVES:
        #print(i)
        player = i % 2

        print(moves[i])
        print('---')
        whichLight = index(moves[i])
        print(whichLight)
        lights[whichLight].set_state(off)
        i += 1
        print(pcolor[player])
        c = pcolor[player]
        #lights[whichLight].set_state(rgb((pcolor[player])))

        lights[whichLight].set_state(rgb(c[0],c[1],c[2]))
        #check for win
        if player == 0:
            p0cnt += 1
        else:
            p1cnt += 1

        if player == 0 and you_won(p0_moves[:p0cnt]):
            print('p0 wins!')
            #flash red
            await asyncio.sleep(1.5)

            for i in range(16):
                lights[i].set_state(rgb(255,0,0))

            await asyncio.sleep(2)
            return
            #return
        elif player == 1 and you_won(p1_moves[:p1cnt]):
            print('player 1 wins!!')
            #flash blue and return
            await asyncio.sleep(1.5)

            for i in range(16):
                lights[i].set_state(rgb(0,0,255))

            await asyncio.sleep(2)

            return
        #lights[whichLight].set_state(rgb(78,109,1))
        await loop.next()

all_patterns = [tictactoe]

active_pattern = tictactoe # pulsate_skeleton