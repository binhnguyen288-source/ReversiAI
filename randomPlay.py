## Reversi AI by Nguyen The Binh 2052002
## Nov 5, 2020


from timeit import default_timer as timer

mate = 1000;
table = [0] * (2 ** 16);



def Pfill1(r, e):
    e &= 0xfefefefefefefefe;
    r  = (r << 1) & e;
    r |= (r << 1) & e;
    e &= e << 1;
    r |= (r << 2) & e;
    e &= e << 2;
    r |= (r << 4) & e;
    return (r << 1) & 0xfefefefefefefefe;

def Pfill7(r, e):
    e &= 0x7f7f7f7f7f7f7f7f;
    r  = (r << 7) & e;
    r |= (r << 7) & e;
    e &= e << 7;
    r |= (r << 14) & e;
    e &= e << 14;
    r |= (r << 28) & e;
    return (r << 7) & 0x7f7f7f7f7f7f7f7f;

def Pfill8(r, e):
    r  = (r << 8) & e;
    r |= (r << 8) & e;
    e &= e << 8;
    r |= (r << 16) & e;
    e &= e << 16;
    r |= (r << 32) & e;
    return (r << 8) & 0xffffffffffffffff;

def Pfill9(r, e):
    e &= 0xfefefefefefefefe;
    r  = (r << 9) & e;
    r |= (r << 9) & e;
    e &= e << 9;
    r |= (r << 18) & e;
    e &= e << 18;
    r |= (r << 36) & e;
    return (r << 9) & 0xfefefefefefefefe;


def Nfill1(r, e):
    e &= 0x7f7f7f7f7f7f7f7f;
    r  = (r >> 1) & e;
    r |= (r >> 1) & e;
    e &= e >> 1;
    r |= (r >> 2) & e;
    e &= e >> 2;
    r |= (r >> 4) & e;
    return (r >> 1) & 0x7f7f7f7f7f7f7f7f;

def Nfill7(r, e):
    e &= 0xfefefefefefefefe;
    r  = (r >> 7) & e;
    r |= (r >> 7) & e;
    e &= e >> 7;
    r |= (r >> 14) & e;
    e &= e >> 14;
    r |= (r >> 28) & e;
    return (r >> 7) & 0xfefefefefefefefe;

def Nfill8(r, e):
    r  = (r >> 8) & e;
    r |= (r >> 8) & e;
    e &= e >> 8;
    r |= (r >> 16) & e;
    e &= e >> 16;
    r |= (r >> 32) & e;
    return r >> 8;

def Nfill9(r, e):
    e &= 0x7f7f7f7f7f7f7f7f;
    r  = (r >> 9) & e;
    r |= (r >> 9) & e;
    e &= e >> 9;
    r |= (r >> 18) & e;
    e &= e >> 18;
    r |= (r >> 36) & e;
    return (r >> 9) & 0x7f7f7f7f7f7f7f7f;




def pfill1(r, e):
    e &= 0xfefefefefefefefe;
    r |= (r << 1) & e;
    e &= e << 1;
    r |= (r << 2) & e;
    e &= e << 2;
    r |= (r << 4) & e;
    return r;

def pfill7(r, e):
    e &= 0x7f7f7f7f7f7f7f7f;
    r |= (r << 7) & e;
    e &= e << 7;
    r |= (r << 14) & e;
    e &= e << 14;
    r |= (r << 28) & e;
    return r;

def pfill8(r, e):
    e &= 0xffffffffffffffff;
    r |= (r << 8) & e;
    e &= e << 8;
    r |= (r << 16) & e;
    e &= e << 16;
    r |= (r << 32) & e;
    return r;

def pfill9(r, e):
    e &= 0xfefefefefefefefe;
    r |= (r << 9) & e;
    e &= e << 9;
    r |= (r << 18) & e;
    e &= e << 18;
    r |= (r << 36) & e;
    return r;


def nfill1(r, e):
    e &= 0x7f7f7f7f7f7f7f7f;
    r |= (r >> 1) & e;
    e &= e >> 1;
    r |= (r >> 2) & e;
    e &= e >> 2;
    r |= (r >> 4) & e;
    return r;

def nfill7(r, e):
    e &= 0xfefefefefefefefe;
    r |= (r >> 7) & e;
    e &= e >> 7;
    r |= (r >> 14) & e;
    e &= e >> 14;
    r |= (r >> 28) & e;
    return r;

def nfill8(r, e):
    r  = (r >> 8) & e;
    r |= (r >> 8) & e;
    e &= e >> 8;
    r |= (r >> 16) & e;
    e &= e >> 16;
    r |= (r >> 32) & e;
    return r;

def nfill9(r, e):
    e &= 0x7f7f7f7f7f7f7f7f;
    r |= (r >> 9) & e;
    e &= e >> 9;
    r |= (r >> 18) & e;
    e &= e >> 18;
    r |= (r >> 36) & e;
    return r;

def nfill(r, e):
    return Nfill1(r, e) | Nfill7(r, e) | Nfill8(r, e) | Nfill9(r, e);


def pfill(r, e):
    return Pfill1(r, e) | Pfill7(r, e) | Pfill8(r, e) | Pfill9(r, e);
    
def popcnt(x):
    return table[x & 0xffff] + table[(x >> 16) & 0xffff] + table[(x >> 32) & 0xffff] + table[x >> 48];
def slowpopcnt(x):
    count = 0;
    while (x != 0):
        count += 8;
        x &= x - 1;
    return count;

def eva(x):
    return popcnt(x) + popcnt(x & 0xff818181818181ff) + slowpopcnt(x & 0x8100000000000081);

bestmove = 0;
KH = [0] * 32;
def search(x, o, alpha, beta, depth, ply, flag):
    global bestmove;
    global KH;
    if (depth <= 0):
        return eva(x) - eva(o);
    best = -mate;
    allmove = (pfill(x, o) | nfill(x, o)) & ~(o | x);
    if (allmove == 0):
        if (flag == True):
            countx = popcnt(x);
            counto = popcnt(o);
            if(countx > counto):
                return mate;
            if (countx < counto):
                return -mate;
            if (countx == counto):
                return 0;
        return -search(o, x, -beta, -alpha, depth - 1, ply + 1, True);

     
    while (KH[ply] & allmove):
        move = KH[ply];
        delta = (nfill1(move, o) & pfill1(x, o)) | (nfill7(move, o) & pfill7(x, o)) | (nfill8(move, o) & pfill8(x, o)) | (nfill9(move, o) & pfill9(x, o)) | (pfill1(move, o) & nfill1(x, o)) | (pfill7(move, o) & nfill7(x, o)) | (pfill8(move, o) & nfill8(x, o)) | (pfill9(move, o) & nfill9(x, o)) | move;
        score = -search(o & ~delta, x | delta, -beta, -alpha, depth - 1, ply + 1, False);
        if (score > best):
            best = score;
            if (score > alpha):
                alpha = score;
            if (ply == 0):
                bestmove = move;
            if (score >= beta):
                return score;
        allmove &= ~move;
    
    while (allmove != 0):
        move = allmove & -allmove;
        delta = (nfill1(move, o) & pfill1(x, o)) | (nfill7(move, o) & pfill7(x, o)) | (nfill8(move, o) & pfill8(x, o)) | (nfill9(move, o) & pfill9(x, o)) | (pfill1(move, o) & nfill1(x, o)) | (pfill7(move, o) & nfill7(x, o)) | (pfill8(move, o) & nfill8(x, o)) | (pfill9(move, o) & nfill9(x, o)) | move;
        score = -search(o & ~delta, x | delta, -beta, -alpha, depth - 1, ply + 1, False);
        if (score > best):
            best = score;
            if (score > alpha):
                alpha = score;
            if (ply == 0):
                bestmove = move;
            if (score >= beta):
                KH[ply] = move;
                return score;
        allmove &= ~move;

    return best;

def set(x):
    return 1 << x;

def tzcnt(x):
    for i in range(64):
        if (x & (1 << i)):
            return i;
    return 64;

import random
from gameplay import valid

def nextMove(board, color, time):
    global bestmove;
    global KH;
    for i in range(2 ** 16):
        count = 0;
        x = i;
        while (x):
            count += 1;
            x &= x - 1;
        table[i] = count;
    bestmove = 0;
    x = 0;
    o = 0;
    for i in range(32):
        KH[i] = 0;
    
    for i in range(8):
        for j in range(8):
            if (board[i][j] == '.'):
                continue;
            if (board[i][j] == color):
                x |= set(i * 8 + j);
            else:
                o |= set(i * 8 + j);
    score = 0;
    max_depth = 1;
    clock = timer() - timer();
    while (score != mate):
        start = timer()
        score = search(x, o, -mate, mate, max_depth, 0, False);
        end = timer();
        clock += end - start;
        if (clock * 3000 >= time):
            break;
        max_depth += 2;
    bestmove = tzcnt(bestmove);
    if bestmove == 64:
        return "pass"
    return (bestmove // 8, bestmove % 8);


def nextMoveR(board, color, time):
    return nextMove(board, color, time)

