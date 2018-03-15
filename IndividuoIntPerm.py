from Individuo import *
import numpy as np

class IndividuoIntPerm(Individuo):
    def __init__(self, tam, minB=-10, maxB=10):
        self.min_bound = minB
        self.max_bound = maxB
        self.cod = "INT-PERM"
        self.cromossomo = self.init_cromossomo(tam)
    
    def init_cromossomo(self, tamCrom):
        return np.random.RandomState().permutation(tamCrom)
        
    def fitness(self):
        return -1