import numpy as np
import random
import Individuo
import IndividuoBin
import IndividuoInt
import IndividuoReal
import IndividuoIntPerm



class Populacao():
    def __init__(self, tamPop, tamCrom, cod, minB=-10, maxB=10):
        if cod == "BIN":
            self.individuos = [IndividuoBin.IndividuoBin(tamCrom, minB, maxB) for i in range(tamPop)]
        elif cod == "INT":
            self.individuos = [IndividuoInt.IndividuoInt(tamCrom, minB, maxB) for i in range(tamPop)]
        elif cod == "REAL":
            self.individuos = [IndividuoReal.IndividuoReal(tamCrom, minB, maxB) for i in range(tamPop)]
        elif cod == "INT-PERM":
            self.individuos = [IndividuoIntPerm.IndividuoIntPerm(tamCrom, minB, maxB) for i in range(tamPop)]
        else:
            raise Exception("Codificacao invalida")
        self.tamCrom = tamCrom
        self.maxDiv = None

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

    def diversidade(self):
        c = self.centroid()
        i = 0
        for i in range(len(self.individuos)):
            iC = 0
            for j in range(len(self.individuos[i].cromossomo)):
                iC += (self.individuos[i].cromossomo[j] - c[j]) ** 2
            i += iC

        return i

    def diversidadeN(self):
        d = self.diversidade()
        if self.maxDiv:
            return d/self.maxDiv
        else:
            self.maxDiv = d
            return 1
    
    def totalFitness(self):
        totF = 0
        for i in self.individuos:
            totF += i.fitness()
        return totF
    
    def selecaoRoleta(self):
        #Somatorio de fitness
        totF = self.totalFitness()

        #chance de cada individuo de ser escolhido
        chances = []
        for i in self.individuos:
            chances += [i.fitness()/totF] 
        
        #escolha dos individuos
        selecionados = []
        for i in range(int((len(self.individuos)/2))):#cada iteracao seleciona 2
            #escolhe o individuo de acordo com o numero gerado aleatoriamente
            n = np.random.choice(list(range(len(self.individuos))), p=chances)
            selecionados += [self.individuos[n]]
            cN = chances[n]
            for ch in range(len(chances)):
                chances[ch] += cN/(len(chances)-1)
            chances[n] = 0.0
            n2 = np.random.choice(list(range(len(self.individuos))), p=chances)
            selecionados += [self.individuos[n2]]
            selecionados += [self.individuos[n2]]
            for ch in range(len(chances)):
                chances[ch] -= cN/(len(chances)-1)
            chances[n] = cN
        
        print("Total fitness: ", totF)
        print("Chances: ", chances)
        return selecionados

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
