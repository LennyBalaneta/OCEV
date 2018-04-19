from Individuo import *
import numpy as np

class IndividuoIntPerm(Individuo):
    def __init__(self, tam, minB, maxB, fitFunc, funcResultado):
        self.min_bound = minB
        self.max_bound = maxB
        self.cod = "INT-PERM"
        self.cromossomo = self.init_cromossomo(tam)
        self.fitFunc = fitFunc
        self.funcResultado = funcResultado
        self.fit = None
        
    def init_cromossomo(self, tamCrom):
        return np.random.RandomState().permutation(tamCrom)
        
    def fitness(self):
        return self.fitFunc(self.cromossomo)
        
    def crossover(self, i2, tipo):
        #tipo de crossover
        if tipo == "pmx":
            return self.crossoverPMX(i2)
        else:
            raise Exception("Crossover [", tipo, "] indefinido")
    
    def crossoverPMX(self, i2):
        p1, p2 = [0]*len(self.cromossomo), [0]*len(self.cromossomo)
        crom1, crom2 = [], []
        
        
        #inicializa a posicao dos indices
        for i in range(len(self.cromossomo)):
            p1[self.cromossomo[i]] = i
            p2[i2.cromossomo[i]] = i
            crom1 += [self.cromossomo[i]]
            crom2 += [i2.cromossomo[i]]
            
        #Define os pontos de corte
        ptoC1 = np.random.randint(0, len(self.cromossomo)-1)
        ptoC2 = np.random.randint(ptoC1+1, len(self.cromossomo))
        
        for i in range(ptoC1, ptoC2):
            temp1 = crom1[i]
            temp2 = crom2[i]
            
            crom1[i], crom1[p1[temp2]] = temp2, temp1
            crom2[i], crom2[p2[temp1]] = temp1, temp2
            
            p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
            p2[temp1], p2[temp2] = p2[temp2], p2[temp1]
        
        return [crom1, crom2]
        
    def mutacao(self, tx, tipo):
        if tipo == "swap":
            self.mutacaoSwap(tx)
        else:
            raise Exception("Mutacao[", tipo, "] indefinida")
            
    def mutacaoSwap(self, tx):
        #para cada elemento do cromossomo troca com outro com um chance de txMut
        for i in range(len(self.cromossomo)):
            if np.random.random() < tx:
                p2 = np.random.randint(0, len(self.cromossomo))
                atual = self.cromossomo[i]
                self.cromossomo[i] = self.cromossomo[p2]
                self.cromossomo[p2] = atual