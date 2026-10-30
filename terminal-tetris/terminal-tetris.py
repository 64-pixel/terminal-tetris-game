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

    def move(self,piece, stdscr):
        keys = stdscr.getch()
        new_pos = []
        can_move = True
        

        if keys == curses.KEY_RIGHT:
                for x,y in piece:
                    new_y = y+1

                    if new_y >= SIZE_X:
                        can_move = False
                        
                if can_move == True:
                    for x,y in piece:
                        new_y = y+1
                        new_pos.append([x, new_y])
                    for x,y in piece:
                        self.board[x][y] = 0
                    for x,y in piece:
                        new_y = y+1
                        self.board[x][new_y] = 1
                        stdscr.refresh()
                else:
                    for x,y in piece:
                        new_pos.append([x,y])
                        stdscr.refresh()
                    

        elif keys == curses.KEY_LEFT:
            for x,y in piece:
                new_yy = y-1

                if new_yy < 0:
                    can_move = False 
                    
            if can_move == True:
                for x,y in piece:
                    new_yy = y-1
                    new_pos.append([x, new_yy])
                for x,y in piece:
                    self.board[x][y] = 0
                for x,y in piece:
                    new_yy = y-1
                    self.board[x][new_yy] = 1
                    stdscr.refresh()
            else:
                for x,y in piece:
                    new_pos.append([x,y])
                    stdscr.refresh()
        else:
            for x,y in piece:
                new_pos.append([x,y])
                stdscr.refresh()
            
        return new_pos

def main(stdscr):

    board = Board()
    p = board.newpiece()
    stdscr.keypad(True)
    stdscr.nodelay(True)


    while True:


        #keys = stdscr.getch()
        p = board.fallpiece(p)
        
        if p == None:
            p=board.newpiece()

        p=board.move(p, stdscr)
        board.showBoard(stdscr)
        stdscr.refresh()
        time.sleep(0.1)
        

        

wrapper(main)
    
        


#wrapper(main)

