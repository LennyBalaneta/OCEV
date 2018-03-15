import numpy as np
from Individuo import *
 

class Populacao():
    def __init__(self, tamPop, tamCrom, cod, minB=-10, maxB=10):
        self.individuos = [Individuo(tamCrom, cod, minB, maxB) for i in range(tamPop)]
        self.tamCrom = tamCrom
 
    def popFitness(self):
        s = "Individuos->Fitness:\n"
        for i in self.individuos:
            s += str(i) + " -> " + str(i.fitness()) +"\n"
        return s
 
    def centroid(self):
        cent = []
        for i in range(self.tamCrom):#n dimensões
            s = 0
            for j in range(len(self.individuos)):
                s += self.individuos[j].cromossomo[i]
            cent += [s/len(self.individuos)]
        return cent
 
    def inertia(self):
        c = self.centroid()
        i = 0
        for i in range(len(self.individuos)):
            iC = 0
            maioriC = 0
            for j in range(len(self.individuos[i].cromossomo)):
                iC += (self.individuos[i].cromossomo[j] - c[j]) ** 2
                #print(self.individuos[i].cromossomo[j])
            if iC > maioriC:
                maioriC = iC
            i += iC
 
        return i/maioriC
 
    def __str__(self):
        s = "Individuos:\n"
        for i in self.individuos:
            s += str(i) + "\n"
        return s
 
def main():
    pop = Populacao(5, 5, "REAL")
    print(pop)
 
if __name__ == "__main__":
    main()
#mersennetwister
#deixar a medida de diversidade normalizada
#distancia de hamling(?), faz matriz diagonal, soma tudo e divide
#real -> enclidiana
#inteira -> manhattan
#artigo na pg da disciplina-> pro real e pro binario/testar no inteiro