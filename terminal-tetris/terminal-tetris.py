#tetris on terminal 

import curses, random, time, math, sys, pygame
from curses import wrapper


SIZE_X = 10
SIZE_Y = 20
NORMAL_FALL_TIME = 1
FAST_FALL_TIME = 0.05

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
        self.game_over = False

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
                    char="□"
                else:
                    char ="■"
                stdscr.addstr(y + 4,x + 1,char)
            stdscr.addstr(y + 4, SIZE_X + 1,"|")

        stdscr.refresh()


    def newpiece(self):
        piece = [LINE, SQUARE, L, L2, WASD, Z, Z2][random.randint(0,6)]
        location = random.randint(0, SIZE_X - 1 - len(piece[0]))
        temp = []
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                if piece[i][j] == 1 and self.board[i][j] == 2:
                    self.game_over = True

        for i in range(len(piece)):
            for j in range(len(piece[0])):
                if not self.game_over and piece[i][j] == 1: 
                    self.board[i][j+location] = 1
                    temp.append([i, j+location])
                        
        return temp, piece

    def fallpiece(self, piece):

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

    def delete_line(self):
        deleted = 0
        for i in range(len(self.board) -2, -1, -1):
            if all(cell == 2 for cell in self.board[i]):
                pygame.mixer.Sound("line-clear.mp3").play()
                self.board.pop(i)
                deleted += 1
                self.board.insert(0,[0] * SIZE_X)
        return deleted

    def rotate(self, piece):
        temp = []
        for j in range(len(piece[0])):
            t = []
            for i in range(len(piece)-1,-1,-1):
                t.append(piece[i][j])
            temp.append(t)
        return temp
    def rotated_piece(self,piece):
        new_pos = []
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                if piece[i][j] == 1:
                    new_pos.append([i,j])
        return new_pos
    def rotate_coordinates(self,piece, rotated):
        min_x = min(x for x, y in piece)
        min_y = min(y for x, y in piece)
        can_rotate = True
        new_piece = []
        for x,y in piece:
            self.board[x][y] = 0
        for x,y in rotated:
            new_x = x + min_x
            new_y = y + min_y
            new_piece.append([x + min_x,y + min_y])
            if new_y < 0 or new_y >= SIZE_X:
                can_rotate = False
            elif new_x < 0 or new_x >= SIZE_Y:
                can_rotate = False
            elif self.board[new_x][new_y] == 2:
                can_rotate = False

        if can_rotate == True:
            pygame.mixer.Sound("rotate-piece.mp3").play()
            for x,y in new_piece:
                self.board[x][y] = 1
            return new_piece
        else:
            for x,y in piece:
                self.board[x][y] = 1
            return piece

    def move(self,piece, stdscr, keys):
        new_pos = []
        can_move = True
        

        if keys == curses.KEY_RIGHT:
                for x,y in piece:
                    new_y = y+1

                    if new_y >= SIZE_X:
                        can_move = False

                for x,y in piece:
                    new_y = y+1
                    new_pos.append([x, new_y])


                for x,y in new_pos:
                    if y < 0 or y >= SIZE_X:
                        can_move = False
                    elif self.board[x][y] == 2:
                            can_move = False

                if can_move == True:
                    pygame.mixer.Sound("move-piece.mp3").play()
                    for x,y in piece:
                        self.board[x][y] = 0
                    for x,y in new_pos:
                        self.board[x][y] = 1
                        stdscr.refresh()
                else:
                    return piece
                    

        elif keys == curses.KEY_LEFT:
            for x,y in piece:
                new_yy = y-1

                if new_yy < 0:
                    can_move = False 

            for x,y in piece:
                new_yy = y-1
                new_pos.append([x, new_yy])

            for x,y in new_pos:
                if y <0 or y >= SIZE_X:
                    can_move = False
                elif self.board[x][y] == 2:
                    can_move = False
                    
            if can_move == True:
                pygame.mixer.Sound("move-piece.mp3").play()
                for x,y in piece:
                    self.board[x][y] = 0
                for x,y in new_pos:
                    self.board[x][y] = 1
                    stdscr.refresh()
            else:
                return piece

        else:
            for x,y in piece:
                new_pos.append([x,y])
                stdscr.refresh()
        return new_pos

def run(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    board = Board()
    p, shape = board.newpiece()
    last_fall = time.time()
    current_fall_time = NORMAL_FALL_TIME
    last_down_press = 0
    lines_deleted = 0
    music_volume = 0.5
    stdscr.keypad(True)
    stdscr.nodelay(True)
    stdscr.addstr(18,18, "Turn off music:q")
    stdscr.addstr(20,18, "Turn on music:e")
    stdscr.addstr(22,18, "Volume up:a")
    stdscr.addstr(24,18, "Volume down:d")
    pygame.mixer.init()
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.load("videoplayback.mp3")
    pygame.mixer.music.play(-1)
    
    
    
    
    while True:

            
            keys = stdscr.getch()
            stdscr.addstr(26,18, "Volume:" + str(round(music_volume, 3)))

            if keys == ord("q"):
                pygame.mixer.music.stop()
            elif keys == ord("e"):
                pygame.mixer.music.play(-1)
            if keys == ord("a"):
                    music_volume += 0.05
                    music_volume =max(0.0, min(1.0, music_volume))
                    pygame.mixer.music.set_volume(music_volume)
            if keys == ord("d"):
                music_volume -= 0.05
                music_volume =max(0.0, min(1.0, music_volume))
                pygame.mixer.music.set_volume(music_volume)
    
            if  keys == curses.KEY_DOWN:
                last_down_press = time.time()
    
            if time.time() - last_down_press < 0.1:
                current_fall_time = FAST_FALL_TIME
                
            else:
                current_fall_time = NORMAL_FALL_TIME
    
            if keys == curses.KEY_UP:
                new_shape = board.rotate(shape)
                
                rotated_shape = board.rotated_piece(new_shape)
                old_p = p.copy()
                p = board.rotate_coordinates(p, rotated_shape )
    
                if old_p != p:
                    shape = new_shape
                else:
                    shape = shape
            
            p=board.move(p, stdscr, keys)
            
    
            if time.time() - last_fall >= current_fall_time:
                p = board.fallpiece(p)
                last_fall = time.time()
    
                if p == None:
                    lines_deleted += board.delete_line()
                    
                    p, shape=board.newpiece()
                    if board.game_over == True:
                        stdscr.clear()
                        end_screen(stdscr, lines_deleted)
                        stdscr.refresh()
                        break

    
    
            stdscr.addstr(SIZE_Y + 8,0,"Lines deleted: " + str(lines_deleted))
            board.showBoard(stdscr)
            stdscr.refresh()

def end_screen(stdscr, lines_deleted):
    pygame.mixer.Sound("game-over.mp3").play()
    stdscr.nodelay(False)
    pygame.mixer.music.stop()
    stdscr.clear()
    stdscr.addstr(10,10, "Game Over")
    stdscr.addstr(12,10, "You have deleted " + str(lines_deleted) + " lines")
    stdscr.addstr(14,10, "Do you wish to play again(r/n)")
    stdscr.refresh()

    while True:
        input_ke = stdscr.getch()
        if input_ke == ord("r"):
            run(stdscr)
        elif input_ke == ord("n"):
            sys.exit()

    
def main(stdscr):

    #main menu
    stdscr.clear()
    stdscr.addstr(10,10, "Welcome")
    stdscr.addstr(12,10, "This is terminal Tetris")
    stdscr.addstr(14,10, "Do you wish to start(y/n)")
    stdscr.refresh()
    while True:
        input_k = stdscr.getch()
        if input_k == ord("y"):
            run(stdscr)
        elif input_k == ord("n"):
            sys.exit()
        
        
wrapper(main)
    