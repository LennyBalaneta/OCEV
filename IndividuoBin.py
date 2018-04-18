from Individuo import *
import numpy as np
import math
 
class IndividuoBin(Individuo):
    def __init__(self, tam, minB, maxB, fitFunc):
        self.min_bound = minB
        self.max_bound = maxB
        self.cod = "BIN"
        self.cromossomo = self.init_cromossomo(tam)
        self.fitFunc = fitFunc
        self.fit = None
 
    def init_cromossomo(self, tamCrom):
        return np.random.RandomState().randint(2, size=tamCrom)
 
    def fitness(self):
        return self.fitFunc(self.cromossomo)
 
    def crossover(self, i2, tipo):
        #tipo de crossover
        if tipo == "1pto":
            return self.crossover1pto(i2)
        elif tipo == "2pto":
            return self.crossover2pto(i2)
        elif tipo == "unif":
            return self.crossoverUnif(i2)
        else:
            raise Exception("Crossover [", tipo, "] indefinido")
 
    def crossover1pto(self, i2):
        #Define o ponto de corte
        ptoC = np.random.randint(0, len(self.cromossomo))
        #gera os 2 individuos resultantes do crossover
        crom1 = np.concatenate((self.cromossomo[:ptoC], i2.cromossomo[ptoC:]))
        crom2 = np.concatenate((i2.cromossomo[:ptoC], self.cromossomo[ptoC:]))
 
        #retorna uma lista com os 2 individuos gerados
        return [crom1, crom2]
 
    def crossover2pto(self, i2):
        #Define os pontos de corte
        ptoC1 = np.random.randint(0, len(self.cromossomo)-1)
        ptoC2 = np.random.randint(ptoC1+1, len(self.cromossomo))
 
        #gera os 2 individuos resultantes do crossover
        crom1 = np.concatenate((self.cromossomo[:ptoC1], i2.cromossomo[ptoC1:ptoC2], self.cromossomo[ptoC2:]))
        crom2 = np.concatenate((i2.cromossomo[:ptoC1], self.cromossomo[ptoC1:ptoC2], i2.cromossomo[ptoC2:]))
 
        #retorna uma lista com os 2 individuos gerados
        return [crom1, crom2]
 
 
    def crossoverUnif(self, i2):
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
 
    def mutacao(self, tx, tipo):
        if tipo == "bitflip":
            self.mutacaoBitFlip(tx)
        else:
            raise Exception("Mutacao[", tipo, "] indefinida")
 
    def mutacaoBitFlip(self, tx):
        #para cada elemento do cromossomo da bitflip com um chance de txMut
        for i in range(len(self.cromossomo)):
            if np.random.random() < tx:
                #print("Flip em ", i)
                if self.cromossomo[i] == 0:
                    self.cromossomo[i] = 1
                else:
                    self.cromossomo[i] = 0