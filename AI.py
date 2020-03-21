import gaming
import copy
import numpy as np
import math
import random
import gym

def sigmoid(x):
    return 1/(1+(math.e**(-x)))

def sigm_der(x):
    return x*(1-x)

grid_pos={0:(0,0),
          1:(0,1),
          2:(0,2),
          3:(1,0),
          4:(1,1),
          5:(1,2),
          6:(2,0),
          7:(2,1),
          8:(2,2)}

class AI:
    def __init__(self,x,y,color,map):
        self.game=gaming.Game('s','g')
        self.map=map
        self.color=color
        self.win=False
        self.turn_que=[]
        self.current_pos=[]
        self.stone_that=0
        self.place_to=0
        self.input = {(0,0):0,
                      (0,1):0,
                      (0,2):0,
                      (1,0):0,
                      (1,1):0,
                      (1,2):0,
                      (2,0):0,
                      (2,1):0,
                      (2,2):0,}
        self.input_list=[]
        self.weights1 = [0.56293375,-0.65510277,0.56916019,-0.71955828,0.7051864,0.50926152,-0.51367474,0.60935218,-0.7304235]
        self.true_output = []
        self.answer=[0,0,0,0,0,0,0,0,0]

    def scan_map(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j]!=0:
                    if self.map[i][j][0]==self.color:
                        self.input[(i,j)]=1
                        self.current_pos.append((i,j))

                    else:
                        self.input[(i,j)]=-1

    def transform(self):
        inp=self.input.values()
        for i in inp:
            self.input_list.append(i)
    def empty(self):
        self.input_list=[]

    def make_move(self):


        for i in range(len(self.input)):
            self.true_output.append(self.input_list[i]*self.weights1[i])

        out_copy=copy.copy(self.true_output)
        stone_to_move=int(np.argmax(out_copy))
        del out_copy[stone_to_move]


        place_to_go=int(np.argmax(out_copy))
        del out_copy[place_to_go]

        print(stone_to_move,place_to_go)
        self.answer[stone_to_move]=2
        self.answer[place_to_go]=1


        # self.map[grid_pos[stone_to_move][0]][grid_pos[stone_to_move][1]],self.map[grid_pos[place_to_go][0]][grid_pos[place_to_go][1]]=\
        #     self.map[grid_pos[place_to_go][0]][grid_pos[place_to_go][1]],self.map[grid_pos[stone_to_move][0]][grid_pos[stone_to_move][1]]

        self.stone_that,self.place_to=stone_to_move,place_to_go
        self.true_output=[]




    def evolve(self):
        for i in range(len(self.weights1)):
            self.weights1[i]+=random.uniform(-10,10)

    def udjust_weight(self,given):
        error=max(self.true_output) - given
        adjustment = error-sigm_der(given)
        self.weights1+=np.dot(np.transpose(self.input_list),adjustment)

    def check_win(self):
        if self.game.check_win("R"):
            self.win=True

    def change_map(self):
        self.map[grid_pos[self.stone_that][0]][grid_pos[self.stone_that][1]],self.map[grid_pos[self.place_to][0]][grid_pos[self.place_to][1]]=\
            self.map[grid_pos[self.place_to][0]][grid_pos[self.place_to][1]],self.map[grid_pos[self.stone_that][0]][grid_pos[self.stone_that][1]]


    def check_valid(self):
        return self.game.valid_move(grid_pos[self.stone_that],grid_pos[self.place_to])



ai=AI(10,10,"R",gaming.game_map)

while ai.win!=True:

    ai.scan_map()
    ai.transform()
    while not ai.check_valid():
        ai.make_move()
        ai.evolve()
    ai.change_map()
    ai.empty()
    ai.evolve()

    print(ai.map)
    ai.check_win()











