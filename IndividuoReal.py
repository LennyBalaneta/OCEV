from Individuo import *
import numpy as np
import math

class IndividuoReal(Individuo):
    def __init__(self, tam, minB=-10, maxB=10):
        self.min_bound = minB
        self.max_bound = maxB
        self.cod = "REAL"
        self.isBin = True
        self.cromossomo = self.init_cromossomo(tam)
    
    def init_cromossomo(self, tamCrom):
        if not self.isBin:#Real normal
            return np.random.RandomState().uniform(self.min_bound, self.max_bound, size=tamCrom)
        else:#Real em binario
            return np.random.RandomState().randint(2, size=26)
        
    def fitness(self):
        if not self.isBin:#Real normal
            return self.ackleyFunc(self.cromossomo)
        else:#Real em binario
            '''
            var1 -> [0:13]
            var2 -> [13:26]
            '''
            vars = [self.ajuste(self.cromDecode(self.cromossomo, 0, 13)), self.ajuste(self.cromDecode(self.cromossomo, 13, 26))]
            return self.ackleyFunc(vars)
        
    def cromDecode(self, c, ini, fin):
        numTotal = c[ini:fin]
        numStr = ""
        for n in numTotal:
            numStr += str(n)
        return int(numStr, 2)

    def crossover(self, i2, tipo):
        print("Crossover indefinido")
        return -1
        
    def mutacao(self, tx, tipo):
        print("Mutacao indefinida")
        return -1
        
    def ajuste(self, num):
        '''
        numero recebido -> [0, 8191]
        bounds desejados -> [-32.00, 32.00]
        '''
        l = 13
        x_min = -32.0
        x_max = 32.0
        x = x_min + ((x_max - x_min)/(2**l-1)) *  num
        return x

    def ackleyFunc(self, vars):
        first_sum = 0.0
        second_sum = 0.0
        for v in range(len(vars)):
            first_sum += vars[v] ** 2.0
            second_sum += math.cos(2.0 * math.pi * vars[v])
        n = float(len(vars))
        return -20.0*math.exp(-0.2*math.sqrt(first_sum/n)) - math.exp(second_sum/n) + 20 + math.e
        
        
'''
    #funcao 12 maximos locais
    #arrrumar a quantidade de bits -> 16
    def fitness2(self):
        x = self.ajuste2(self.cromDecode(self.cromossomo, 0, 16))
        return math.cos(20*x) - (math.sqrt(x**2)/2) + ((x**3)/4)
        
    def ajuste2(self, num):
        
        #numero recebido -> [0, 65536]
        #bounds desejados -> [-2.0000, 2.0000]
        n = num/10000
        n -= 2
        if n > 2:
            n = 2
        return n
'''