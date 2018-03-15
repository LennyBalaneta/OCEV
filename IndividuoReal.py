from Individuo import *
import numpy as np

class IndividuoReal(Individuo):
    def __init__(self, tam, minB=-10, maxB=10):
        self.min_bound = minB
        self.max_bound = maxB
        self.cod = "REAL"
        self.cromossomo = self.init_cromossomo(tam)
    
    def init_cromossomo(self, tamCrom):
        return np.random.RandomState().uniform(self.min_bound, self.max_bound, size=tamCrom)
        
    def fitness(self):
        return -1