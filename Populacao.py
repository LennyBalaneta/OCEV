import numpy as np
import random
import Individuo
import IndividuoBin
import IndividuoInt
import IndividuoReal
import IndividuoIntPerm
import matplotlib.pyplot as plt
import copy
 
 
 
class Populacao():
    def __init__(self, problema, tamPop):
        if problema["codificacao"] == "BIN":
            self.individuos = [IndividuoBin.IndividuoBin(problema["tamCrom"], problema["boundMin"], problema["boundMax"], problema["fitnessFunc"]) for i in range(tamPop)]
            self.tipoCrossover = "1pto"
            self.tipoMutacao = "bitflip"
        elif problema["codificacao"] == "INT":
            self.individuos = [IndividuoInt.IndividuoInt(problema["tamCrom"], problema["boundMin"], problema["boundMax"], problema["fitnessFunc"]) for i in range(tamPop)]
            self.tipoCrossover = "1pto"
            self.tipoMutacao = "rndVal"
        elif problema["codificacao"] == "REAL":
            self.individuos = [IndividuoReal.IndividuoReal(problema["tamCrom"], problema["boundMin"], problema["boundMax"], problema["fitnessFunc"]) for i in range(tamPop)]
            self.tipoCrossover = "unif"
            self.tipoMutacao = "gauss"
        elif problema["codificacao"] == "INT-PERM":
            self.individuos = [IndividuoIntPerm.IndividuoIntPerm(problema["tamCrom"], problema["boundMin"], problema["boundMax"], problema["fitnessFunc"]) for i in range(tamPop)]
            self.tipoCrossover = "null"
            self.tipoMutacao = "null"
        else:
            raise Exception("Codificacao invalida")
        self.nome = problema["nome"]
        self.descricao = problema["descricao"]
        self.tamPop = tamPop
        self.tipoCod = problema["codificacao"]
        self.tamCrom = problema["tamCrom"]
        self.maxDiv = -1.0
        self.maxGeracoes = 2000
        self.elit = True
        self.tamTorneio = 3
        self.tipoSelecao = "roleta"
        self.txMut = 0.05#taxa de mutacao
        self.txCross = 0.8#taxa de crossover
 
    def popFitness(self):
        s = "Individuos->Fitness:\n"
        for i in self.individuos:
            s += str(i) + " -> " + str(i.fitness()) +"\n"
        return s
            
    def diversidade(self):
        chromos = np.array([ind.cromossomo for ind in self.individuos])
        ci = np.sum(chromos, axis=0) / len(self.individuos)
        I = np.sum((chromos - ci) ** 2)
        if I >= self.maxDiv:
            self.maxDiv = I
        return I/self.maxDiv
    
    def totalFitness(self):
        totF = 0
        for i in self.individuos:
            totF += i.fit
        return totF
 
    def selecao(self):
        #executa o tipo de selecao desejada
        if self.tipoSelecao == "roleta":
            #selecao por roleta
            return self.selecaoRoleta()
        elif self.tipoSelecao == "torneio":
            #selecao por torneio
            return self.selecaoTorneio()
        else:
            raise Exception("Selecao [", self.tipoSelecao, "] invalida")
 
    def selecaoRoleta(self):
        #Somatorio de fitness
        totF = self.totalFitness()
 
        #chance de cada individuo de ser escolhido
        chances = []
        for i in self.individuos:
            chances += [i.fit/totF]
 
        #escolha dos individuos
        selecionados = []
        for i in range(int(len(self.individuos)/2)):#cada iteracao seleciona 2
            #escolhe o individuo de acordo com o numero gerado aleatoriamente
            n = np.random.choice(list(range(len(self.individuos))), p=chances)
            selecionados += [self.individuos[n]]
 
            #recalcula a roleta
            chances2 = []
            for i in self.individuos:
                chances2 += [i.fit/(totF-self.individuos[n].fit)]
            chances2[n] = 0.0
            n2 = np.random.choice(list(range(len(self.individuos))), p=chances2)
            selecionados += [self.individuos[n2]]
 
        #print("Total fitness: ", totF)
        #print("Chances: ", chances)
        return selecionados
 
    def selecaoTorneio(self):
        selecionados = []
        melhorTorn = -1
        for i in range(int(len(self.individuos))):
            partTorn = []
            for j in range(self.tamTorneio):
                partTorn += [np.random.randint(len(self.individuos))]
            melhorTorn = partTorn[0]
            for j in partTorn:
                if self.individuos[j].fit > self.individuos[melhorTorn].fit:
                    melhorTorn = j
            selecionados += [self.individuos[melhorTorn]]
        return selecionados
 
    def recombinacao(self, individuos):
        popInt = []
        for i in range(int(len(self.individuos)/2)):
            if np.random.random() < self.txCross:
                inds = individuos[i*2].crossover(individuos[i*2+1], self.tipoCrossover)
                popInt += [inds[0]]
                popInt += [inds[1]]
            else:
                popInt += [individuos[i*2].cromossomo]
                popInt += [individuos[i*2+1].cromossomo]
        return popInt
 
    def calculaFitness(self):
        for i in self.individuos:
            i.fit = i.fitness()
        piorInd = melhorInd = 0
        melhorF = self.individuos[melhorInd].fit
        piorF = self.individuos[piorInd].fit
        
        for i in range(1, len(self.individuos)):
            if self.individuos[i].fit > melhorF:
                melhorInd = i
                melhorF = self.individuos[i].fit
            if self.individuos[i].fit < piorF:
                piorInd = i
                piorF = self.individuos[i].fit          
        return  piorInd, melhorInd
        
    def mediaDaGeracao(self):
        soma = 0.0
        for i in self.individuos:
            soma += i.fit
        return soma/len(self.individuos)
 
 
    def loopEvolucao(self):
        melhoresInd = []#melhores individuos por geracao
        melhoresIndF = []#melhores fitness por geracao
        mediasIndF = []#media de fitness por geracao
        diver = []#diversidade
        ger = 0#n da geracao
        
        #calcula o fitness da populacao inicial
        piorInd, melhorInd = self.calculaFitness()
        
        #guarda o melhor individuo ate entao
        melhorGeral = copy.deepcopy(self.individuos[melhorInd])#melhor individuo encontrado ate o momento
        
        #guarda estatisticas da populacao inicial
        diver += [self.diversidade()]
        melhoresInd += [self.individuos[melhorInd].cromossomo]
        melhoresIndF += [self.individuos[melhorInd].fit]
        mediasIndF += [self.mediaDaGeracao()]
        
        
        #loop principal
        while ger < self.maxGeracoes:
            ger += 1
 
            #print
            if ger%10 == 0:
                print("---Geracao", ger, "---", "Melhor fitness: ", melhorGeral.fit)
 
            #selecao
            sel = self.selecao()

            #criacao da populacao intermediaria
            popInterm = self.recombinacao(sel)

            #substituia a populacao
            for i in range(len(popInterm)):
                self.individuos[i].cromossomo = popInterm[i]
            
            #mutacao
            for i in self.individuos:
                i.mutacao(self.txMut, self.tipoMutacao)
            
            #calcula fitness da geracao
            piorInd, melhorInd = self.calculaFitness()
            
            #elitismo
            if self.elit == True:
                self.individuos[piorInd] = copy.deepcopy(melhorGeral)
            
            #verifica se tem um novo melhor geral
            if self.individuos[melhorInd].fit > melhorGeral.fit:
                melhorGeral = copy.deepcopy(self.individuos[melhorInd])
            else:
                if self.elit == True:
                    #o novo melhor da geracao é o de elitismo, guardado na posicao do pior
                    melhorInd = piorInd
                
            #guarda estatisticas da populacao
            diver += [self.diversidade()]
            melhoresInd += [self.individuos[melhorInd].cromossomo]
            melhoresIndF += [self.individuos[melhorInd].fit]
            mediasIndF += [self.mediaDaGeracao()]
            
        #TODO retornar melhor individuo geral e seu fitness
        print("Melhor fitness encontrado:", melhorGeral.fit)
        print("Melhor individuo encontrado:", melhorGeral.cromossomo)
        return {"bInd":melhoresInd, "bF":melhoresIndF, "mF":mediasIndF, "diver":diver, "bGeral":melhorGeral}
 
    def geraGraficos(self, result):
        #criacao dos graficos
        fig, ax = plt.subplots(2, 1)
        #grafico do maior
        ax[0].set_xlabel("Geração")
        ax[0].set_ylabel("Fitness")
        ax[0].set_title("Fitness por geração")
        ax[0].plot(result["bF"], label="Melhor", lw=1)
        ax[0].plot(result["mF"], label="Media", lw=1)
        ax[0].legend(loc="upper left")
 
        #grafico da media
        ax[1].set_xlabel("Geração")
        ax[1].set_ylabel("Diversidade")
        ax[1].set_title("Diversidade por geração")
        ax[1].plot(result["diver"], lw=1)
 
        plt.tight_layout()
        plt.show()
 
    def info(self):
        print("---", self.nome, "---")
        print(self.descricao)
        print("---Configuracoes do AG---")
        print("Tipo de codificacao:", self.tipoCod)
        print("Tamanho da populacao:", self.tamPop)
        print("Tamanho do cromossomo:", self.tamCrom)
        print("Maximo de geracoes:", self.maxGeracoes)
        print("Tipo de selecao:", self.tipoSelecao)
        print("Tamanho torneio(caso selecao por torneio):", self.tamTorneio)
        print("Elitismo:", self.elit)
        print("Tipo de crossover:", self.tipoCrossover)
        print("Taxa de crossover:", self.txCross)
        print("Tipo de mutacao:", self.tipoMutacao)
        print("Taxa de mutacao:", self.txMut)
 
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