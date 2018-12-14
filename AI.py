import gaming
import copy
import numpy as np
import math

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
        self.map=map
        self.color=color
        self.win=False
        self.turn_que=[]
        self.current_pos=[]
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


    def make_move(self):
        for i in range(len(self.input)):
            self.true_output.append(self.input_list[i]*self.weights1[i])

        print(self.true_output)
        print(np.argmax(self.true_output))
        self.true_output = np.dot(np.transpose(self.input_list),self.weights1)

    def udjust_weight(self,given):
        error=max(self.true_output) - given
        adjustment = error-sigm_der(given)
        self.weights1+=np.dot(np.transpose(self.input_list),adjustment)





ai=AI(10,10,"R",gaming.game_map)

ai.scan_map()
ai.transform()
ai.make_move()







