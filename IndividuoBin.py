from Individuo import *
import numpy as np

class IndividuoBin(Individuo):
    def __init__(self, tam, minB=-10, maxB=10):
        self.min_bound = minB
        self.max_bound = maxB
        self.cod = "BIN"
        self.cromossomo = self.init_cromossomo(tam)
    
    def init_cromossomo(self, tamCrom):
        return np.random.RandomState().randint(2, size=tamCrom)
        
    def fitness(self):
        f = 0
        for i in range(len(self.cromossomo)-1):
            if self.cromossomo[i] == 1:
                if self.cromossomo[i+1] == 0:
                    f += 1
            else:
                if self.cromossomo[i+1] == 1:
                    f += 1
        return f