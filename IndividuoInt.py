from Individuo import *
import numpy as np

class IndividuoInt(Individuo):
    def __init__(self, tam, minB=-10, maxB=10):
        self.min_bound = minB
        self.max_bound = maxB
        self.cod = "INT"
        self.cromossomo = self.init_cromossomo(tam)
    
    def init_cromossomo(self, tamCrom):
        return np.random.RandomState().randint(self.min_bound, self.max_bound, size=tamCrom)
        
    def fitness(self):
        return -1