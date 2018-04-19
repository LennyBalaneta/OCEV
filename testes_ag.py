import Populacao as p
from FuncoesFitness import FuncFit

problema = "BitsAlternados"
tamPop = 30


#1 execucao
a = p.Populacao(FuncFit[problema], tamPop)

#configurações
a.maxGeracoes = 2000
a.elit = True
a.tipoSelecao = "torneio"
a.tamTorneio = 3
#a.tipoCrossover = "pmx"
#a.tipoMutacao = "swap"
a.txMut = 0.05#taxa de mutacao
a.txCross = 0.8#taxa de crossover

r = a.loopEvolucao()

a.geraGraficos(r)

'''

#n execucoes
execucoes = 10
resultados = []
for i in range(execucoes):
    print("Execucao", (i+1))
    a = p.Populacao(FuncFit[problema], tamPop)

    #configurações
    a.maxGeracoes = 1000
    a.elit = True
    a.tipoSelecao = "torneio"
    a.tamTorneio = 3
    #a.tipoCrossover = "pmx"
    #a.tipoMutacao = "swap"
    a.txMut = 0.05#taxa de mutacao
    a.txCross = 0.8#taxa de crossover

    r = a.loopEvolucao()
    
    resultados.append(r)

somaBf = [0.0]*a.maxGeracoes
somaMf = [0.0]*a.maxGeracoes
somaDiver = [0.0]*a.maxGeracoes
for i in range(len(resultados)):
    for j in range(len(somaBf)):
        somaBf[j] += resultados[i]["bF"][j]
        somaMf[j] += resultados[i]["mF"][j]
        somaDiver[j] += resultados[i]["diver"][j]
        
for j in range(len(somaBf)):
    somaBf[j] /= execucoes
    somaMf[j] /= execucoes
    somaDiver[j] /= execucoes
rMedia = {"bF" : somaBf, "mF" : somaMf, "diver" : somaDiver}
a.geraGraficos(rMedia)
'''






















