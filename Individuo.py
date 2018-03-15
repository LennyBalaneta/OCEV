from abc import ABC, abstractmethod
import numpy as np

class Individuo(ABC):
    @abstractmethod
    def __init__(self, tam, minB=-10, maxB=10):
        pass
    
    @abstractmethod
    def init_cromossomo(self, tamCrom):
        pass
        
    @abstractmethod
    def fitness(self):
        pass
    
    def __str__(self):
        return np.array2string(self.cromossomo)