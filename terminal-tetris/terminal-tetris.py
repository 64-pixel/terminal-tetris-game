#tetris on terminal 

import curses, random, time


def main(stdscr):
    stdscr.clear()
    sh,sw = stdscr.getmaxyx()
    
    drop_rate = 3
    shapes = [
    [[1, 1, 1],
     [0, 1, 0]],
    [[0, 2, 2],
     [2, 2, 0]],
    [[3, 3, 0],
     [0, 3, 3]],
    [[4, 0, 0],
     [4, 4, 4]],
    [[0, 0, 5],
     [5, 5, 5]],
    [[6, 6],
     [6, 6]],
    [[7, 7, 7, 7]]
]

    vib_x = int(sw / 2)
    vib_y = int(sh / 5)

   

    d = curses.KEY_DOWN
    npos = None

    win = curses.newwin(sh + 1, sw + 1, 0, 0)
    win.border()
    win.keypad(True)
    win.timeout(100)
    

    while True:
        npos = None

        if leg[0][0] in (0,sh) or leg[0][1] in (0,sw):
            win.addch(rest)

        key = win.getch()
        if key == ord('q'):
            break
        if d == curses.KEY_DOWN:
            npos = (leg[0][0] + 1, leg[0][1])

        leg.insert(0, npos)
        rest = leg.pop()
        
        win.addch(rest[0], rest[1], " ")
        win.addch(npos[0], npos[1], curses.ACS_BLOCK)
    
    

curses.wrapper(main)