from Individuo import *
import numpy as np
import math

class IndividuoReal(Individuo):
    def __init__(self, tam, minB=-10, maxB=10):
        self.min_bound = minB
        self.max_bound = maxB
        self.cod = "REAL"
        self.cromossomo = self.init_cromossomo(tam)
    
    def init_cromossomo(self, tamCrom):
        return np.random.RandomState().uniform(self.min_bound, self.max_bound, size=tamCrom)
        
    def fitness(self):
        return self.ackleyFunc(self.cromossomo)
    
    def ackleyFunc(self, vars):
        first_sum = 0.0
        second_sum = 0.0
        for v in range(len(vars)):
            first_sum += vars[v] ** 2.0
            second_sum += math.cos(2.0 * math.pi * vars[v])
        n = float(len(vars))
        return -20.0*math.exp(-0.2*math.sqrt(first_sum/n)) - math.exp(second_sum/n) + 20 + math.e