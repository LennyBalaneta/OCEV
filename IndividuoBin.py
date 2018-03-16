from Individuo import *
import numpy as np
import math

class IndividuoBin(Individuo):
    def __init__(self, tam, minB=-10, maxB=10):
        self.min_bound = minB
        self.max_bound = maxB
        self.cod = "BIN"
        self.cromossomo = self.init_cromossomo(tam)

    def init_cromossomo(self, tamCrom):
        return np.random.RandomState().randint(2, size=tamCrom)

    def fitnessOld(self):
        f = 0
        for i in range(len(self.cromossomo)-1):
            if self.cromossomo[i] == 1:
                if self.cromossomo[i+1] == 0:
                    f += 1
            else:
                if self.cromossomo[i+1] == 1:
                    f += 1
        return f

    def fitness(self):
        '''
        var1 -> [0:13]
        var2 -> [13:26]
        '''
        if len(self.cromossomo) != 26:
            print("Tamanho do cromossomo incorreto para aplicar na funcao de ackley")
            return -1
        vars = [self.cromDecode(self.cromossomo, 0, 13), self.cromDecode(self.cromossomo, 13, 26)]
        return self.ackleyFunc(vars)

    def cromDecode(self, c, ini, fin):
        '''
        Estrutura do numero binario:
        [0:6] -> parte inteira
        [6:13] -> parte decimal
        '''
        numTotal = c[ini:fin]
        
        pInt = numTotal[0:6]
        pDec = numTotal[6:13]
        
        numInt = 0
        for i in range(len(pInt)):
            numInt += pInt[i] * (2**(len(pInt)-i-1))
        numDec = 0
        for i in range(len(pDec)):
            numDec += pDec[i] * (2**(len(pDec)-i-1))
        inBounds = self.ajuste(numInt + (numDec/100))
        return self.ajuste(numInt + (numDec/100))
        
    def ajuste(self, num):
        '''
        numero recebido -> [0, 64.27]
        bounds desejados -> [-30, 30]
        '''
        num -= 30
        if num > 30:
            num = 30
        return num

    def ackleyFunc(self, vars):
        first_sum = 0.0
        second_sum = 0.0
        for v in range(len(vars)):
            first_sum += vars[v] ** 2.0
            second_sum += math.cos(2.0 * math.pi * vars[v])
        n = float(len(vars))
        return -20.0*math.exp(-0.2*math.sqrt(first_sum/n)) - math.exp(second_sum/n) + 20 + math.e
        
        

        
