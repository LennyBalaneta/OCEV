import numpy as np
import random
import Individuo
import IndividuoBin
import IndividuoInt
import IndividuoReal
import IndividuoIntPerm
import matplotlib.pyplot as plt



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
        self.maxGeracoes = 100

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
        for i in range(int(len(self.individuos)/2)):#cada iteracao seleciona 2
            #escolhe o individuo de acordo com o numero gerado aleatoriamente
            n = np.random.choice(list(range(len(self.individuos))), p=chances)
            selecionados += [self.individuos[n]]
            
            #recalcula a roleta
            chances2 = []
            for i in self.individuos:
                chances2 += [i.fitness()/(totF-self.individuos[n].fitness())]
            chances2[n] = 0.0
            n2 = np.random.choice(list(range(len(self.individuos))), p=chances2)
            selecionados += [self.individuos[n2]]
        
        #print("Total fitness: ", totF)
        #print("Chances: ", chances)
        return selecionados
        
    def recombinacao(self, individuos):
        popInt = []
        for i in range(int(len(self.individuos)/2)):
            inds = individuos[i*2].crossover1pto(individuos[i*2+1])
            popInt += [inds[0]]
            popInt += [inds[1]]
        return popInt
    
    def loopEvolucao(self):
        melhorF = 0
        melhoresInd = []
        melhoresIndF = []
        mediasIndF = []
        for gen in range(self.maxGeracoes):
            print("---Geracao", gen, "---", "Melhor fitness: ", melhorF)
            #print(self.popFitness())
            
            #print("Selecao:")
            #selecao dos individuos
            sel = self.selecaoRoleta()
            #for s in sel:
            #    print(s)
            
            #print("Recombinacao:")
            #criacao da populacao intermediaria
            popInterm = self.recombinacao(sel)
            #for s in popInterm:
            #    print(s)
            
            #substituia a populacao
            for i in range(len(popInterm)):
                self.individuos[i].cromossomo = popInterm[i]
                
            #mutacao
            for i in self.individuos:
                i.mutacao()
            
            #calculo do melhor e media por geracao
            melhorF = -1
            melhor = None
            soma = 0
            for i in self.individuos:
                fit = i.fitness()
                soma += fit
                if fit > melhorF:
                    melhorF = fit
                    melhor = i.cromossomo
            melhoresInd += [melhor]
            melhoresIndF += [melhorF]
            mediasIndF += [soma/len(self.individuos)]
            #print ao final da geracao
            #print("Populacao final da geracao")
            #print(self.popFitness())
            #print("----------------")
        return {"bInd":melhoresInd, "bF":melhoresIndF, "mF":mediasIndF}
    
    def geraGraficos(self, result):    
        #criacao dos graficos
        fig, ax = plt.subplots(2, 1)
        #grafico do maior
        ax[0].set_xlabel("Geração")
        ax[0].set_ylabel("Maior fitness")
        ax[0].plot(result["bF"])
        
        #grafico da media
        ax[1].set_xlabel("Geração")
        ax[1].set_ylabel("Média de fitness")
        ax[1].plot(result["mF"])
        
        plt.tight_layout()
        plt.show()
    
    def __str__(self):
        s = "Individuos:\n"
        for i in self.individuos:
            s += str(i) + "\n"
        return s

def main():
    pop = Populacao(5, 5, "BIN")
    print(pop)

if __name__ == "__main__":
    main()
#mersennetwister
#deixar a medida de diversidade normalizada
#distancia de hamling(?), faz matriz diagonal, soma tudo e divide
#real -> enclidiana
#inteira -> manhattan
#artigo na pg da disciplina-> pro real e pro binario/testar no inteiro
