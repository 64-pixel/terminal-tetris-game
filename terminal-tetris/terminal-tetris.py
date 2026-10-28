#tetris on terminal 

import curses, random, time, math
from curses import wrapper


SIZE_X = 10
SIZE_Y = 20

# pieces

LINE = [[1],[1],[1],[1]]
SQUARE = [[1,1], [1,1]]
L = [[1,0],[1,0],[1,1]]
L2 = [[0,1],[0,1],[1,1]]
WASD = [[0,1,0], [1,1,1]]
Z = [[1,1,0], [0,1,1]]
Z2 = [[0,1,1],[1,1,0]]



class Board():
    def __init__(self):

        self.board = [[0]* SIZE_X for _ in range(SIZE_Y)]
        self.board.append([2]*SIZE_X)

    def showBoard(self, stdscr):

        stdscr.addstr(0,0,"-"* 50)
        stdscr.addstr(1,18,"Terminal Tetris")
        stdscr.addstr(2,0,"-"* 50)

        for y,row in enumerate(self.board):
            stdscr.addstr(y + 4,0,"|")
            for x, v in enumerate(row):
                if v ==0:
                    char = " "
                elif v == 1:
                    char="■"
                else:
                    char ="□"
                stdscr.addstr(y + 4,x + 1,char)
            stdscr.addstr(y + 4, SIZE_X + 1,"|")

        stdscr.refresh()


    def newpiece(self):
        piece = [LINE, SQUARE, L, L2, WASD, Z, Z2][random.randint(0,6)]
        location = random.randint(0, SIZE_X - 1 - len(piece[0]))
        temp = []
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                if piece[i][j]:
                    self.board[i][j+location] = 1
                    temp.append([i, j+location])
        return temp

    def fallpiece(self, piece):
        flag = True
        for x,y in piece:
            if self.board[x+1][y]==2:
                self.setpiece(piece)
                return None
        temp = []
        for x,y in piece:
            temp.append([x+1,y])
            self.board[x][y] = 0
        for x,y in temp:
            self.board[x][y] = 1
        return temp

    def setpiece(self, piece):
        for x,y in piece:
            self.board[x][y] = 2
        return -1

    #def move_right(self,p):
        if self.board[y][x+1] == "|":
            None

def main(stdscr):

    board = Board()
    p = board.newpiece()

    while True:

        #keys = stdscr.getch()
        p = board.fallpiece(p)
        if p == None:
            p=board.newpiece()
        board.showBoard(stdscr)
        stdscr.refresh()
        stdscr.nodelay(True)
        time.sleep(0.5)
        

        

wrapper(main)
    
        


#wrapper(main)

