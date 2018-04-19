from Individuo import *
import numpy as np
import math
import random
 
class IndividuoReal(Individuo):
    def __init__(self, tam, minB, maxB, fitFunc, funcResultado):
        self.min_bound = minB
        self.max_bound = maxB
        self.cod = "REAL"
        self.cromossomo = self.init_cromossomo(tam)
        self.fitFunc = fitFunc
        self.funcResultado = funcResultado
        self.fit = None
 
    def init_cromossomo(self, tamCrom):
        return np.random.RandomState().uniform(self.min_bound, self.max_bound, size=tamCrom)
 
    def fitness(self):
        return self.fitFunc(self.cromossomo)
 
    def crossover(self, i2, tipo):
        #tipo de crossover
        if tipo == "unif":
            return self.crossoverUniformA(i2)
        elif tipo == "blx":
            return self.crossoverBLX(i2)
        elif tipo == "aritm":
            return self.crossoverAritm(i2)
        else:
            raise Exception("Crossover [", tipo, "] indefinido")
 
    def crossoverUniformA(self, i2):
        #gera os 2 individuos resultantes do crossover
        #inicializa o array com o primeiro elemento
        if np.random.random() < 0.5:
            crom1 = np.array((self.cromossomo[0]))
            crom2 = np.array((i2.cromossomo[0]))
        else:
            #print("Flip em 0")
            crom1 = np.array((i2.cromossomo[0]))
            crom2 = np.array((self.cromossomo[0]))
 
        #percorre o resto do array verificando se ocorre o flip ou nao
        for i in range(1, len(self.cromossomo)):
            if np.random.random() < 0.5:
                crom1 = np.append(crom1, self.cromossomo[i]);
                crom2 = np.append(crom2, i2.cromossomo[i]);
            else:
                #print("Flip em ", i)
                crom1 = np.append(crom1, i2.cromossomo[i]);
                crom2 = np.append(crom2, self.cromossomo[i]);
        #retorna uma lista com os 2 individuos gerados
        return [crom1, crom2]
    
    def crossoverBLX(self, i2):
        #gera os 2 individuos resultantes do crossover
        a = 0.5 #parametro [0, 1], default é 0.5
                
        #inicializa o array com o primeiro elemento
        di = abs(self.cromossomo[0] - i2.cromossomo[0])
        minB = min(self.cromossomo[0], i2.cromossomo[0]) - a*di
        maxB = max(self.cromossomo[0], i2.cromossomo[0]) + a*di
        c1 = np.random.uniform(minB, maxB)
        c2 = np.random.uniform(maxB, maxB)
        
        #verificacao de bounds
        if c1 < self.min_bound:
            c1 = self.min_bound
        if c1 > self.max_bound:
            c1 = self.max_bound
        if c2 < self.min_bound:
            c2 = self.min_bound
        if c2 > self.max_bound:
            c2 = self.max_bound
        crom1 = np.array(c1)
        crom2 = np.array(c2)
        
        #percorre o resto do array
        for i in range(1, len(self.cromossomo)):
            di = abs(self.cromossomo[i] - i2.cromossomo[i])
            minB = min(self.cromossomo[i], i2.cromossomo[i]) - a*di
            maxB = max(self.cromossomo[i], i2.cromossomo[i]) + a*di
            c1 = np.random.uniform(minB, maxB)
            c2 = np.random.uniform(minB, maxB)
            
            #verificacao dos bound
            if c1 < self.min_bound:
                c1 = self.min_bound
            if c1 > self.max_bound:
                c1 = self.max_bound
            if c2 < self.min_bound:
                c2 = self.min_bound
            if c2 > self.max_bound:
                c2 = self.max_bound
            
            crom1 = np.append(crom1, c1)
            crom2 = np.append(crom2, c2)
        return [crom1, crom2]
        
    def crossoverAritm(self, i2):
        #gera os 2 individuos resultantes do crossover
        a = 0.5 #parametro [0, 1], default é 0.5
                
        #inicializa o array com o primeiro elemento
        c1 = a * self.cromossomo[0] + (1.0-a) * i2.cromossomo[0]
        c2 = (1.0-a) * self.cromossomo[0] + a * i2.cromossomo[0]
        
        #verificacao de bounds
        if c1 < self.min_bound:
            c1 = self.min_bound
        if c1 > self.max_bound:
            c1 = self.max_bound
        if c2 < self.min_bound:
            c2 = self.min_bound
        if c2 > self.max_bound:
            c2 = self.max_bound
        crom1 = np.array(c1)
        crom2 = np.array(c2)
        
        #percorre o resto do array
        for i in range(1, len(self.cromossomo)):
            c1 = a * self.cromossomo[i] + (1.0-a) * i2.cromossomo[i]
            c2 = (1.0-a) * self.cromossomo[i] + a * i2.cromossomo[i]
            
            #verificacao dos bound
            if c1 < self.min_bound:
                c1 = self.min_bound
            if c1 > self.max_bound:
                c1 = self.max_bound
            if c2 < self.min_bound:
                c2 = self.min_bound
            if c2 > self.max_bound:
                c2 = self.max_bound
            crom1 = np.append(crom1, c1)
            crom2 = np.append(crom2, c2)
        return [crom1, crom2]
    
    def mutacao(self, tx, tipo):
        if tipo == "gauss":
            self.mutacaoGaussiana(tx)
        else:
            raise Exception("Mutacao[", tipo, "] indefinida")
            
    def mutacaoGaussiana(self, tx):
        #std usado na mutacao Gaussiana
        std = 0.3#0.1 tava muito pouco
        
        #para cada elemento do cromossomo da bitflip com um chance de txMut
        for i in range(len(self.cromossomo)):
            if np.random.random() < tx:
                mean = self.cromossomo[i]
                x1 = random.random()
                x2 = random.random()
                
                if x1 == 0.0:
                    x1 = 1.0
                if x2 == 0.0:
                    x2 = 1.0
                
                y1 = math.sqrt(-2.0 * math.log(x1)) * math.cos(2.0 * math.pi * x2)
                valor = y1 * std + mean
                #verificacao de bounds
                if valor < self.min_bound:
                    valor = self.min_bound
                if valor > self.max_bound:
                    valor = self.max_bound
                self.cromossomo[i] = valor

                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                