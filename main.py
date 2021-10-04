import pygame
import os
pygame.font.init()

WIDTH, HEIGHT  = 500,600 #coordinates of windows
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku GUI")
 
FPS = 60
GREEN = (0,125,0)
BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)

Rect_Width, Rect_Height = 56,55
SUDOKU_GRID_IMAGE  = pygame.image.load(os.path.join('Assets', 'sudoku.png')) # immage from assets
BACKGROUND_IMAGE = pygame.image.load(os.path.join('Assets', 'background.jpg')) # immage from assets 

SUDOKU_GRID =  pygame.transform.scale(SUDOKU_GRID_IMAGE, (WIDTH, 500))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
pozicia = (-1,-1)

NUMBERS_FONT = pygame.font.SysFont('Calibri', 50)

Solved = 0
Wrong_entry = 0

board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]

#method for drawing window        
class Draw_Window:
    #function draw window draw background, sudoku grid, rectangles and numbers
    def draw_window(self): 
        global pozicia
        DW = Draw_Window()
        TEXT = NUMBERS_FONT.render("Wanna try again? Y/N",1,BLACK)
        TEXT2 = NUMBERS_FONT.render("Wrong entry",1,RED)
        
        WIN.blit(BACKGROUND, (0,0))
        WIN.blit(SUDOKU_GRID, (0,0))

        if not Solved and not Wrong_entry:
            DW.draw_rectangles(pozicia)

        elif Solved and not Wrong_entry:
            DW.draw_rectangles_solved()
            WIN.blit(TEXT, (40, 550))

        elif Wrong_entry:
            DW.draw_rectangles_wrong_entry()
            WIN.blit(TEXT2, (120, 510))
            WIN.blit(TEXT, (40, 550))

        DW.draw_numbers()
        pygame.display.update()
    
    #simply it will go through whole board and draw every number except 0
    def draw_numbers(self):    
        for i in range (len(board)):
            for j in range(len(board[0])):
                if board[i][j] != 0:
                    TEXT = NUMBERS_FONT.render(str(board[i][j]),1,BLACK)
                    WIN.blit(TEXT, (Rect_Width*j+18,Rect_Height*i+5)) # +18 and +5 are there because it will centre the number in middlle of rectangle

    #this function draw rectangles based on variable position which is essentialy last coordinates where user clicked
    def draw_rectangles(self,position):
        self.position = position
        x,y = position
        x //= 56
        y //= 55
        if y < 9:
            if x >= 7 :
                    pygame.draw.rect(WIN, RED,[Rect_Width*x-2,Rect_Height*y,Rect_Width,Rect_Height], 3)
        
            else:
                pygame.draw.rect(WIN, RED,[Rect_Width*x,Rect_Height*y,Rect_Width,Rect_Height], 3)

    #simply draw green rectangles after sudoku is successfully solved
    def draw_rectangles_solved(self):
       for i in range (9):
            for j in range(9):
                pygame.draw.rect(WIN, GREEN,[Rect_Width*i,Rect_Height*j,Rect_Width,Rect_Height], 3)
    
    #draw red rectangles when wrong entry occurs
    def draw_rectangles_wrong_entry(self):
        for i in range (9):
            for j in range(9):
                pygame.draw.rect(WIN, RED,[Rect_Width*i,Rect_Height*j,Rect_Width,Rect_Height], 3)
#method for solving sudoku
class Sudoku_Algoritm:
    #find empty positions(zero in board) and return row and collumn of that position
    def find_empty(self,bo):
        self.bo = bo
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                if bo[i][j] == 0:
                    return (i,j)
        return None
    #check if the added number is valid
    def check(self,bo, num, pos):
        
        #check row
        for i in range(len(bo[0])):
            if bo[pos[0]][i] == num and pos[1] != i:
                return False
        #check column
        for j in range(len(bo)):
            if bo[j][pos[1]] == num and pos[0] != j:
                return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3
        #check 3x3 box
        for i in range(box_y* 3, box_y*3 + 3):
            for j in range(box_x* 3, box_x*3 +3 ):
                if bo[i][j] == num and (i,j) != pos:
                    return False
    
        return True
    #solve algoritm 
    def solve(self,bo):
        self.bo = bo
        SA = Sudoku_Algoritm()
        find = SA.find_empty(bo)
        if not find:
            return True
        else:
            row, col = find
    
        for i in range (1,10):
            if SA.check(bo, i, (row,col)):
                bo[row][col] = i

                if SA.solve(bo):
                    return True
                    
                bo[row][col] = 0

        return False
    #this function will calculate position to board
    def add_to_board(self,num, position):
        self.num = num
        self.position = position
        row, col = position
        row //= 56
        col //= 55
        board[col][row] = num

    #reset the board to all 0
    def clear_board(self):
        for i in range(9):
            for j in range(9):
                board[i][j] = 0
    #this function will check user entry if its along with sudoku rules then its returned true 
    def check_board(self,bo):
        self.bo = bo
        SA = Sudoku_Algoritm()
        count = 0
        for x in range(9):
            for y in range(9):
                if board[x][y] == 0:
                    count += 1
        if count >= 74:
            return False

        for x in range(9):
            for y in range(9):
                pos = (x, y)
                num = board[x][y]

                if num == 0:
                    continue

                for i in range(len(bo[0])):
                    if bo[pos[0]][i] == num and pos[1] != i:
                        return False

                for j in range(len(bo)):
                    if bo[i][pos[1]] == num and pos[0] != i:
                        return False

                box_x = pos[1] // 3
                box_y = pos[0] // 3

                for i in range(box_y* 3, box_y*3 +3 ):
                    for j in range(box_x* 3, box_x*3 +3 ):
                        if bo[i][j] == num and (i,j) != pos:
                            return False
                  
        return True
#main function where event types are handles
def main():
    DW = Draw_Window()
    SA = Sudoku_Algoritm()
    clock = pygame.time.Clock()
     
    Run = True
    while Run:
        clock.tick(FPS)
            #exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Run = False
            #will store the coordinates to global variable where user clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                global pozicia
                pozicia = pygame.mouse.get_pos()
            #calling add to board after pressing numbers    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    SA.add_to_board(1, (pozicia))
                if event.key == pygame.K_2:
                    SA.add_to_board(2, (pozicia))
                if event.key == pygame.K_3:
                    SA.add_to_board(3, (pozicia))
                if event.key == pygame.K_4:
                    SA.add_to_board(4, (pozicia))
                if event.key == pygame.K_5:
                    SA.add_to_board(5, (pozicia))
                if event.key == pygame.K_6:
                    SA.add_to_board(6, (pozicia))
                if event.key == pygame.K_7:
                    SA.add_to_board(7, (pozicia))
                if event.key == pygame.K_8:
                    SA.add_to_board(8, (pozicia))
                if event.key == pygame.K_9:
                    SA.add_to_board(9, (pozicia))
                if event.key == pygame.K_KP1:
                    SA.add_to_board(1, (pozicia))
                if event.key == pygame.K_KP2:
                    SA.add_to_board(2, (pozicia))
                if event.key == pygame.K_KP3:
                    SA.add_to_board(3, (pozicia))
                if event.key == pygame.K_KP4:
                    SA.add_to_board(4, (pozicia))
                if event.key == pygame.K_KP5:
                    SA.add_to_board(5, (pozicia))
                if event.key == pygame.K_KP6:
                    SA.add_to_board(6, (pozicia))
                if event.key == pygame.K_KP7:
                    SA.add_to_board(7, (pozicia))
                if event.key == pygame.K_KP8:
                    SA.add_to_board(8, (pozicia))
                if event.key == pygame.K_KP9:
                    SA.add_to_board(9, (pozicia))
                if event.key == pygame.K_BACKSPACE:
                    SA.add_to_board(0, (pozicia))
                if event.key == pygame.K_SPACE:
                    if SA.check_board(board):
                        SA.solve(board)
                        global Solved
                        Solved += 1
                    else:
                        global Wrong_entry
                        Wrong_entry += 1
                
                #if user wants add new entry to board this will handle it
                if event.key == pygame.K_y and Solved != 0 or event.key == pygame.K_y and Wrong_entry != 0:
                    Solved = 0
                    Wrong_entry = 0
                    SA.clear_board()
                
                if event.key == pygame.K_n and Solved != 0 or event.key == pygame.K_n and Wrong_entry != 0:
                    Run = False                     
             
        DW.draw_window()
             
    pygame.quit()

if __name__ == "__main__":
    main()
