import numpy as np
import random
import Individuo
import IndividuoBin
import IndividuoInt
import IndividuoReal
import IndividuoIntPerm
import matplotlib.pyplot as plt
import copy
 
 
 
class AG():
    def __init__(self, problema, tamPop):
        if problema["codificacao"] == "BIN":
            self.individuos = [IndividuoBin.IndividuoBin(problema["tamCrom"], problema["boundMin"], problema["boundMax"], problema["fitnessFunc"], problema["funcResultado"]) for i in range(tamPop)]
            self.tipoCrossover = "1pto"
            self.tipoMutacao = "bitflip"
        elif problema["codificacao"] == "INT":
            self.individuos = [IndividuoInt.IndividuoInt(problema["tamCrom"], problema["boundMin"], problema["boundMax"], problema["fitnessFunc"], problema["funcResultado"]) for i in range(tamPop)]
            self.tipoCrossover = "1pto"
            self.tipoMutacao = "rndval"
        elif problema["codificacao"] == "REAL":
            self.individuos = [IndividuoReal.IndividuoReal(problema["tamCrom"], problema["boundMin"], problema["boundMax"], problema["fitnessFunc"], problema["funcResultado"]) for i in range(tamPop)]
            self.tipoCrossover = "unif"
            self.tipoMutacao = "gauss"
        elif problema["codificacao"] == "INT-PERM":
            self.individuos = [IndividuoIntPerm.IndividuoIntPerm(problema["tamCrom"], problema["boundMin"], problema["boundMax"], problema["fitnessFunc"], problema["funcResultado"]) for i in range(tamPop)]
            self.tipoCrossover = "pmx"
            self.tipoMutacao = "swap"
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
        self.escLinear = True
        self.alfa = -1.0#escalonamento linear
        self.beta = -1.0#escalonamento linear
        self.c = 1.2#escalonamento linear
 
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

    def geraAlfaBeta(self):
        #encontra fmin, fmax e favg
        fmin = self.individuos[0].fit
        fmax = self.individuos[0].fit
        favg = 0.0
        for i in self.individuos:
            if i.fit < fmin:
                fmin = i.fit

            if i.fit > fmax:
                fmax = i.fit
            favg += i.fit
        favg /= len(self.individuos)

        if fmin > (self.c*favg - fmax) / (self.c - 1):
            self.alfa = (favg * (self.c-1)) / (fmax - favg)
            self.beta = (favg * (fmax - self.c*favg)) / (fmax - favg)
        else:
            self.alfa = favg / (favg - fmin)
            self.beta = (-fmin * favg) / (favg - fmin)
 
    def selecao(self):
        #escalonamento linear
        if self.escLinear:
            self.geraAlfaBeta()

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
        if self.escLinear:
            for i in self.individuos:
                chances += [(i.fit*self.alfa + self.beta)/totF]
        else:
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
                if self.escLinear:
                    if (self.individuos[j].fit*self.alfa + self.beta) > (self.individuos[melhorTorn].fit*self.alfa + self.beta):
                        melhorTorn = j
                else:
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

    def ajustaC(self, geracaoAtual):
        #Geracoes [0, 1]
        #0 -> 1.2
        #0.8 -> 2
        #1 -> 2
        pctEv = geracaoAtual / self.maxGeracoes
        if pctEv > 0.8:
            self.c = 2.0
        else:
            self.c = 1.2 + pctEv


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
            if ger%100 == 0:
                if self.escLinear:
                    print("---Geracao", ger, "--- C:", self.c,"--- Melhor fitness: ", melhorGeral.fit)
                else:
                    print("---Geracao", ger, "--- Melhor fitness: ", melhorGeral.fit)
 
            #ajusta da constante c para o escalonamento linear
            if self.escLinear:
                self.ajustaC(ger)

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
            
        #print("Melhor fitness encontrado:", melhorGeral.fit)
        #print("Melhor individuo encontrado:", melhorGeral.cromossomo)
        #print da melhor solucao
        melhorGeral.funcResultado(melhorGeral.cromossomo)
        return {"bInd":melhoresInd, "bF":melhoresIndF, "mF":mediasIndF, "diver":diver, "bGeral":melhorGeral}
 
    def geraGraficos(self, result):
        #criacao dos graficos
        fig, ax = plt.subplots(2, 1)
        #grafico do maior
        ax[0].set_xlabel("Geração")
        ax[0].set_ylabel("Fitness")
        ax[0].set_title("Fitness por geração")
        ax[0].plot(result["bF"], label="Melhor", lw=1, ls="--")
        ax[0].plot(result["mF"], label="Media", lw=1, ls="-")
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
    
    def help(self):
        print("--- Definicao de problemas: ---")
        print("Para definir um problema é preciso cria-lo arquivo \"FuncoesFitness.py\"")
        print("Definindo uma funcao fitness (com resultado sempre positivo), uma funcao para mostrar o resultado e preencher as informacoes necessarias no dicionario \"FuncFit\"")
        
        print("--- Utilizacao do AG: ---")
        print("1 - é necessario criar uma instancia do AG passando como parametro o problema desejado e o tamanho da populacao")
        print("2 - mudar as configuracoes desejadas")
        print("3 - iniciar o loop evolutivo")
        print("4 - gerar os graficos")
        print("Ex: ")
        print("a = AG.ag(\"BitsAlternados\", 30)\na.maxGeracoes = 2000\nr = a.loopEvolucao()\na.geraGraficos(r)")
        
        print("--- Configuracoes do AG: ---")
        print("Para mudar as configuracoes do AG altere as seguintes variaveis:\n")
        
        #qtdgeracoes
        print("Quantidade de geracoes:")
        print("\tmaxGeracoes = [0, ?] \n")
        
        #selecao
        print("Rotinas de selecao:")
        print("\ttipoSelecao = ")
        print("\t\t\"roleta\" -> selecao por roleta de probabilidades")
        print("\t\t\"torneio\" -> selecao por torneio de tamanho definido pela variavel \"tamTorneio\" \n")
        
        #elitismo
        print("Elitismo:")
        print("\telit = [True | False] \n")
        
        #tipo crossover
        print("Rotinas de crossover:")
        print("\ttipoCrossover = ")
        print("\t\tBIN:")
        print("\t\t\t\"1pto\" -> crossover de 1 ponto")
        print("\t\t\t\"2pto\" -> crossover de 2 pontos")
        print("\t\t\t\"unif\" -> crossover uniforme")
        print("\t\tREAL:")
        print("\t\t\t\"unif\" -> crossover uniforme")
        print("\t\t\t\"blx\" -> crossover BLX")
        print("\t\t\t\"aritm\" -> crossover aritmetico")
        print("\t\tINT:")
        print("\t\t\t\"1pto\" -> crossover de 1 ponto")
        print("\t\t\t\"2pto\" -> crossover de 2 pontos")
        print("\t\t\t\"unif\" -> crossover uniforme")
        print("\t\tINT-PERM:")
        print("\t\t\t\"pmx\" -> crossover PMX \n")
        
        #taxa crossover
        print("Taxa de crossover:")
        print("\ttxCross = [0.0, 1.0] \n")
        
        #tipo mutacao
        print("Rotinas de mutacao:")
        print("\ttipoMutacao = ")
        print("\t\tBIN:")
        print("\t\t\t\"bitflip\" -> mutacao bitflip")
        print("\t\tREAL:")
        print("\t\t\t\"gauss\" -> mutacao Gaussiana")
        print("\t\t\t\"delta\" -> mutacao Delta")
        print("\t\tINT:")
        print("\t\t\t\"rndval\" -> mutacao de valor aleatorio")
        print("\t\tINT-PERM:")
        print("\t\t\t\"swap\" -> mutacao swap \n")

        #taxa crossover
        print("Taxa de mutacao:")
        print("\ttxMut = [0.0, 1.0] \n")
        
    
    def __str__(self):
        s = "Individuos:\n"
        for i in self.individuos:
            s += str(i) + "\n"
        return s