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
 
    def crossover1pto(self, ib2):
        #Define o ponto de corte
        ptoC = np.random.randint(0, len(self.cromossomo))
        #print("Cromossomo 1: ", self.cromossomo)
        #print("Cromossomo 2: ", ib2.cromossomo)
        #print("Ponto de corte: ", ptoC)
 
        #gera os 2 individuos resultantes do crossover
        crom1 = np.concatenate((self.cromossomo[:ptoC], ib2.cromossomo[ptoC:]))
        crom2 = np.concatenate((ib2.cromossomo[:ptoC], self.cromossomo[ptoC:]))
 
        #retorna uma lista com os 2 individuos gerados
        return [crom1, crom2]
 
    def crossover2pto(self, ib2):
        #Define os pontos de corte
        ptoC1 = np.random.randint(0, len(self.cromossomo)-1)
        ptoC2 = np.random.randint(ptoC1+1, len(self.cromossomo))
        print("Cromossomo 1: ", self.cromossomo)
        print("Cromossomo 2: ", ib2.cromossomo)
        print("Ponto de corte 1: ", ptoC1)
        print("Ponto de corte 2: ", ptoC2)
 
        #gera os 2 individuos resultantes do crossover
        crom1 = np.concatenate((self.cromossomo[:ptoC1], ib2.cromossomo[ptoC1:ptoC2], self.cromossomo[ptoC2:]))
        crom2 = np.concatenate((ib2.cromossomo[:ptoC1], self.cromossomo[ptoC1:ptoC2], ib2.cromossomo[ptoC2:]))
 
        #retorna uma lista com os 2 individuos gerados
        return [crom1, crom2]
 
 
    def crossoverUnif(self, ib2):
        #Define os pontos de corte
        print("Cromossomo 1: ", self.cromossomo)
        print("Cromossomo 2: ", ib2.cromossomo)
 
        #gera os 2 individuos resultantes do crossover
        #inicializa o array com o primeiro elemento
        if np.random.random() < 0.5:
            crom1 = self.cromossomo[0]
            crom2 = ib2.cromossomo[0]
        else:
            print("Flip em 0")
            crom1 = ib2.cromossomo[0]
            crom2 = self.cromossomo[0]
 
        #percorre o resto do array verificando se ocorre o flip ou nao
        for i in range(1, len(self.cromossomo)):
            if np.random.random() < 0.5:
                crom1 = np.concatenate((crom1, self.cromossomo[i]));
                crom2 = np.concatenate((crom2, ib2.cromossomo[i]));
            else:
                print("Flip em ", i)
                crom1 = np.concatenate((crom1, ib2.cromossomo[i]));
                crom2 = np.concatenate((crom2, self.cromossomo[i]));
        #retorna uma lista com os 2 individuos gerados
        return [crom1, crom2]