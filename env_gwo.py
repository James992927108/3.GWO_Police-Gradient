import numpy as np
import random
from copy import deepcopy
import operator

from m_RL_brain import PolicyGradient

class Agent():
    def __init__(self, position, fitness, state_len):
        self.position = position
        self.fitness = fitness
        self.prve_fitness = fitness
        self.ExpRat =  random.randint(0,2)
        self.state = np.zeros(state_len)


class EGWO():
    def __init__(self, func, min_bound, max_bound, dimension, n_point, iteration):
        self.func = func
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.dimension = dimension
        self.n_point = n_point
        self.iteration = iteration

        self.state_len = 5
        self.action_len = 3

        self.swarm = self.init_swarm()
        
        self.Alpha , self.Beta , self.Delta = self.get_alpha_beta_delta()
        
        self.m_RL = PolicyGradient(
            n_actions = 3,
            n_features = self.state_len,
            learning_rate=0.02,
            reward_decay=0.99,
            # output_graph=True,
        )
        self.change_factor = 0.1

        print "success"

    def _get_state_len(self):
        return self.state_len

    def _get_action_len(self):
        return self.action_len
        
    def init_swarm(self):
        swarm = []
        for i in range(self.n_point):
            position = np.random.uniform(self.min_bound, self.max_bound, self.dimension)
            fitness = float("inf")
            swarm.append(Agent(position , fitness , self.state_len))
        return swarm

    def cal_fitness(self , i):
        return self.func(self.swarm[i].position)

    def get_alpha_beta_delta(self):
        for i in range(self.n_point):
            self.swarm[i].fitness = self.cal_fitness(i)

        self.swarm = sorted(self.swarm, key= operator.attrgetter('fitness'))
        return self.swarm[0] , self.swarm[1] , self.swarm[2]

    def move(self):
        for iter in range(self.iteration):
            for i in range(self.n_point):
                ExpRat = self.swarm[i].ExpRat
                # update use eq.(5)
                A1 = (2 * ExpRat * random.random()) - ExpRat
                C1 = 2 * random.random()
                A2 = (2 * ExpRat * random.random()) - ExpRat
                C2 = 2 * random.random()
                A3 = (2 * ExpRat * random.random()) - ExpRat
                C3 = 2 * random.random()

                D_alpha = abs(C1 * self.Alpha.position - self.swarm[i].position) 
                X1 = self.Alpha.position - A1 * D_alpha 
                
                D_beta = abs(C2 * self.Beta.position - self.swarm[i].position)
                X2 = self.Beta.position - A2 * D_beta    
                
                D_delta = abs(C3 * self.Delta.position - self.swarm[i].position)
                X3 = self.Delta.position - A3 * D_delta         
                
                self.swarm[i].position = ( X1 + X2 + X3 ) / 3

                # for i in range(self.n_point):
                #     for j in range(self.dimension):
                #         if(self.swarm[i].position[j]  > self.max_bound or self.swarm[i].position[j]  < self.min_bound):
                #             self.swarm[i].position[j]  = np.random.uniform(self.min_bound, self.max_bound)
                
                self.swarm[i].prev_fitness = self.swarm[i].fitness
                self.swarm[i].fitness = self.cal_fitness(i)
                
                # calculate the Feedback eq.(19)
                if self.swarm[i].fitness < self.swarm[i].prev_fitness:
                    feedback = 1.0
                    sign = 1.0
                    self.swarm[i].ExpRat *= (1 + self.change_factor)
                elif self.swarm[i].fitness > self.swarm[i].prev_fitness:
                    feedback = -1.0
                    sign = -1.0
                    self.swarm[i].ExpRat *= (1 - self.change_factor)
                else:
                    feedback = -1.0
                    sign = 0.0
                    self.swarm[i].ExpRat = self.swarm[i].ExpRat                

                action = self.m_RL.choose_action(np.asarray(self.swarm[i].state))
                self.m_RL.store_transition(self.swarm[i].state, action, feedback)
                """every 20 iteration update nuerl network"""
                if iter % 20 == 0:
                    self.m_RL.learn()
                
                # move to right
                # [0, 1, 2, 3, 4] - > [sign , 0, 1, 2, 3]
                """get new state , import use deepcopy"""
                temp = deepcopy(self.swarm[i].state)         
                for j in range(1,self.state_len):
                    self.swarm[i].state[j] = temp[j-1]
                self.swarm[i].state[0] = sign
    
            print iter , self.Alpha.fitness
        print self.Alpha.position