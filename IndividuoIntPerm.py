from Individuo import *
import numpy as np

class IndividuoIntPerm(Individuo):
    def __init__(self, tam, minB, maxB, fitFunc):
        self.min_bound = minB
        self.max_bound = maxB
        self.cod = "INT-PERM"
        self.cromossomo = self.init_cromossomo(tam)
    
    def init_cromossomo(self, tamCrom):
        return np.random.RandomState().permutation(tamCrom)
        
    def fitness(self):
        print("Funcao Fitness indefinida")
        return -1
        
    def crossover(self, i2, tipo):
        print("Crossover indefinido")
        return -1
        
    def mutacao(self, tx, tipo):
        print("Mutacao indefinida")
        return -1