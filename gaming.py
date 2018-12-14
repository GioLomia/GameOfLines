###############################################################
#This is a game of lines
#Game of lines. Rules: Each Player has 3 stones. There are 9 dots on the field. Each dot is connected with all the adjacent
#dots. Each Player Starts on their line on the opposites ends of the field. The stones can only move on the lines and
#have to stop when they get to a dot. Each Player gets to make a single move with a single stone each time. (Just Like Chess)
#The Goal is to line up your 3 stone in a straight line anywhere on the field besides your starting line.
#(During Development came up with an idea to have the same game in 3D where you have to take over a plane rather then a line)
###############################################################
from pygame import *
import pygame
from copy import deepcopy
import tkinter
from sys import exit

grid_positioning={(0,0):(6,10),
                  (0,1):(275,10),
                  (0,2):(540,10),
                  (1,0):(6,275),
                  (1,1):(275,280),
                  (1,2):(540,275),
                  (2,0):(10,540),
                  (2,1):(275,540),
                  (2,2):(545,535)}
reverse_grid_positioning={
                    (6,10):(0,0),
                    (275,10):(0,1),
                    (540,10):(0,2),
                    (6,275):(1,0),
                    (275,280):(1,1),
                    (540,275):(1,2),
                    (10,540):(2,0),
                    (275,540):(2,1),
                    (545,535):(2,2)}
#The Game Grid 0=empty spot, 1=Busy Spot
game_map= [["R1","R2","R3"],
           [ 0,  0,   0],
           ["B1","B2","B3"]]

reset=deepcopy(game_map)

class AI:
    def __init__(self,Game):
        self.game=None
        self.map=game_map






class Stone:
    """
    The stones used to play it.
    """
    def __init__(self, image, id, position,player):
        self.player=player
        self.image=pygame.image.load(image)
        self.identification=id
        self.position=position
        self.grid_position=[]

    def change_pos(self,pos):
        self.grid_position=pos


class Game :
    """
    Game of lines. Rules: Each Player has 3 stones. There are 9 dots on the field. Each dot is connected with all the adjacent
    dots. Each Player Starts on their line on the opposites ends of the field. The stones can only move on the lines and
    have to stop when they get to a dot. Each Player gets to make a single move with a single stone each time. (Just Like Chess)
    The Goal is to line up your 3 stone in a straight line anywhere on the field besides your starting line.

    (During Development came up with an idea to have the same game in 3D where you have to take over a plane rather then a line)

    """

    width,height=600,700
    bg = pygame.image.load("New_Fieald.bmp")

    def __init__(self,player1,player2):
#################################################Screen
        self.screen=None
#################################################Screen
        self.players=[player1,player2]
        self.players_stones=\
                            ([Stone("Stone_Red_Small.png",1,grid_positioning[(0,0)],self.players[0]),  #Player1 Red Stones
                              Stone("Stone_Red_Small.png",2,grid_positioning[(0,1)],self.players[0]),
                              Stone("Stone_Red_Small.png",3,grid_positioning[(0,2)],self.players[0])],

                             [Stone("Stone_Black_Small.png",1,grid_positioning[(2,0)],self.players[1]), #Player2 Black Stones
                              Stone("Stone_Black_Small.png",2,grid_positioning[(2,1)],self.players[1]),
                              Stone("Stone_Black_Small.png",3,grid_positioning[(2,2)],self.players[1])])

        self.stone_rects=[pygame.Rect(10,10,100,100),
                          pygame.Rect(275,10,100,100),
                          pygame.Rect(540,10,100,100),
                          pygame.Rect(10,280,100,100),
                          pygame.Rect(275,280,100,100),
                          pygame.Rect(540,280,100,100),
                          pygame.Rect(10,540,100,100),
                          pygame.Rect(275,540,100,100),
                          pygame.Rect(540,540,100,100),]

        self.stone_grid=[]
    def make_ai_move(self):
        for i in game_map:
            for j in range(len(i)):
                if type(i[j])==str and i[j][0]=="R":
                    print(i[j])
        print(game_map)
    def valid_move(self,fromer,toer):
        """

        :param fromer: where we want to go from
        :param toer: where we want to go to
        :return: True or False
        """
        place_from=str(fromer[0])+str(fromer[1])
        place_to=str(toer[0])+str(toer[1])
        correct_moves={"00":["01","10","11"],
                       "01":["00","02","11"],
                       "02":["01","12","11"],
                       "10":["00","20","11"],
                       "11":["00","01","02","10","12","20","21","22"],
                       "12":["02","22","11"],
                       "20":["10","21","11"],
                       "21":["20","22","11"],
                       "22":["21","12","11"]}
        if place_to in correct_moves[place_from]:
            return True
        else:
            return False

    def make_move(self,stone_to_move,new_y,new_x):
        """
        Function that makes moves happen
        :param stone_to_move: The stone that needs to be moved
        :param new_y: the y position where we need to move
        :param new_x: the
        :return:
        """
        global game_map
        correspond={"R":0,
                    "B":1,
                    "1":0,
                    "2":1,
                    "3":2}
        current_x=0
        current_y=0
        for i in range(len(game_map)):
            # go trough the grid
            for j in range(len(game_map[i])):
                try:
                    #if we selected a correct stone and the place we want to move it to.
                    if game_map[i][j]==stone_to_move:
                        #make that space the stone
                        # print(i,j)
                        current_y=i
                        current_x=j
                except:
                     return "Select a correct space to put your stone in."

        if game_map[new_y][new_x]==0 and self.valid_move([current_y,current_x],[new_y,new_x]):
            #Update Position
            self.players_stones[correspond[stone_to_move[0]]][correspond[stone_to_move[1]]].position=(new_y,new_x)
            #I know this line of code looks very scary, but all it does is move the stone from one place to another
            self.screen.blit(self.players_stones[int(correspond[stone_to_move[0]])][0].image,
                             grid_positioning[self.players_stones[int(correspond[stone_to_move[0]])]
                             [int(correspond[stone_to_move[1]])].position])
            game_map[new_y][new_x]=stone_to_move
            game_map[current_y][current_x]=0
            self.screen.blit(pygame.image.load("Replace.png"),grid_positioning[(current_y,current_x)])
        else:
            return "Can not make this move"
        return game_map

    def getSc(self):
        """
        Screan Generator.
        :return: None
        """
        backg=pygame.image.load("New_Fieald.bmp")
        gameDis=pygame.display.set_mode((self.width,self.height))
        gameDis.blit(backg,(0,0))
        for i in range(3):
            gameDis.blit(self.players_stones[0][0].image,self.players_stones[0][i].position)
        for i in range(3):
            gameDis.blit(self.players_stones[1][0].image,self.players_stones[1][i].position)
        self.screen=gameDis
    def check_win(self,check_for):
        game_mapx=deepcopy(game_map)

        for i in range(len(game_mapx)):
            for j in range(len(game_mapx[i])):
                if game_mapx[j][i]==0:
                    game_mapx[j][i]="X"
        if game_mapx[0][0][0]==check_for and game_mapx[1][0][0]==check_for and game_mapx[2][0][0]==check_for:
            return True
        elif game_mapx[1][0][0]==check_for and game_mapx[1][1][0]==check_for and game_mapx[1][2][0]==check_for:
            return True
        elif game_mapx[0][1][0]==check_for and game_mapx[1][1][0]==check_for and game_mapx[2][1][0]==check_for:
            return True
        elif game_mapx[0][2][0]==check_for and game_mapx[1][2][0]==check_for and game_mapx[2][2][0]==check_for:
            return True
        elif game_mapx[0][0][0]==check_for and game_mapx[1][1][0]==check_for and game_mapx[2][2][0]==check_for:
            return True
        elif game_mapx[0][2][0]==check_for and game_mapx[1][1][0]==check_for and game_mapx[2][0][0]==check_for:
            return True
        elif check_for == "B" and game_mapx[0][0][0]==check_for and game_mapx[0][1][0]==check_for and game_mapx[0][2][0]:
            return True
        elif check_for == "R" and game_mapx[2][0][0]==check_for and game_mapx[2][1][0]==check_for and game_mapx[2][2][0]:
            return True
        return False

    def detect_collision(self):
        """
        Function to determine collisions on the board
        :return: tuple of the coordinates of the stone we selected
        """
        #checks if the

        grids_corr={
            0:(0,0),
            1:(0,1),
            2:(0,2),
            3:(1,0),
            4:(1,1),
            5:(1,2),
            6:(2,0),
            7:(2,1),
            8:(2,2)
        }
        pygame.init()
        running = True
        while running:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
            elif event.type == QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and mouse.get_pressed()[0]==1 :
                for i in range(len(self.stone_rects)):
                    if event.pos[0] in \
                            (range(self.stone_rects[i][0],self.stone_rects[i][0]+self.stone_rects[i][3])) and event.pos[1] in (range(self.stone_rects[i][1],self.stone_rects[i][1]+self.stone_rects[i][2])):
                        return grids_corr[i]
            pygame.display.update()


class Game_GUI:
    def __init__(self,master):
        self.g=None
        self.master=master
        self.master.minsize(width=700, height=500)
        self.master.maxsize(width=1550, height=1100)
        self.master.title("Game of Lines")
        self.label = tkinter.Label(master, text="Start Game")
        self.label.pack()
        #main mode button
        self.number_button=tkinter.Button(self.master, text="2 Player mode", command=self.main)
        self.number_button.pack(padx=30,pady=10)
        #Live mode button
        # self.live_button=tkinter.Button(self.master, text="Live", command=self.get_live)
        # self.live_button.pack(padx=30,pady=10)
        # #Close button

        #Helper button
        self.help_button=tkinter.Button(self.master, text="RULES!", command=self.helper)
        self.help_button.pack(side="top")
        #Helping Text
        self.text_helper=tkinter.StringVar()
        self.words=tkinter.Label(master,textvariable=self.text_helper)
        self.words.pack()

        #exit button
        self.close_button=tkinter.Button(self.master, text="Close", command=exit)
        self.close_button.pack(padx=30,pady=10)


    def helper(self):
        """
        A helping hand for the user.
        :return: None
        """
        self.text_helper.set("""
            Rules: Each Player has 3 stones. There are 9 dots on the field. Each dot is connected with all the adjacent dots. 

            Each Player Starts on their line on the opposites ends of the field. The stones can only move on the lines 
            
            and can only move on empty spots and only move one step ahead. Each Player gets to make a single move with a single stone each time. (Just Like Chess)

            The Goal is to line up your 3 stone in a straight line anywhere on the field besides your starting line.""")

    def main(self):
        #Initializer for the game
        self.g=Game('s','g')
        #creating the screen
        self.g.getSc()
        #checking condition 1
        check1=False
        #checking condition 2
        check2=False
        #Keeps track of whoese turn it is
        turner=True
        point_to=None
        #the game loop
        self.g.screen.blit(pygame.image.load("Black_Move.png"),(0,600))
        moving_stone=None

        while True:

            point_from = self.g.detect_collision()
            stone=game_map[point_from[0]][point_from[1]]
            #Pick the stone we are moving
            #If we picked a spot with a stone in it
            if stone !=0:
                moving_stone=game_map[point_from[0]][point_from[1]]
                check1=True
                point_to=self.g.detect_collision()
            #Position of motion towards
            if point_to!=None:
                stone=game_map[point_to[0]][point_to[1]]
            #makes sure the correct player is taking the turn
            if moving_stone != None:
                if stone==0:
                    if (moving_stone[0]=="R" and turner==False) or (moving_stone[0]=="B" and turner==True):
                        check2=True
                        turner=not turner
                    else:
                        check2=False
            #If all the conditions are satisfied then we make a move
            if check1 and check2:
                self.g.make_move(moving_stone,point_to[0],point_to[1])
                if turner:
                    self.g.screen.blit(pygame.image.load("Black_Move.png"),(0,600))
                else:
                    self.g.screen.blit(pygame.image.load("Red_Move.png"),(0,600))
            if not turner:
                if self.g.check_win("B"):
                    self.g.screen.blit(pygame.image.load("Black_Win.png"),(0,600))
                    # break
            else:
                if self.g.check_win("R"):
                    self.g.screen.blit(pygame.image.load("Red_Wins.png"),(0,600))



def main():
    game=Game('s','g')
    game.make_ai_move()
    print()
    # x=Game_GUI(tkinter.Tk())
    # x.master.mainloop()
if __name__=="__main__":
    main()



















