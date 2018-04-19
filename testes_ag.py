import Populacao as p
from FuncoesFitness import FuncFit

problema = "TSP"
tamPop = 50

a = p.Populacao(FuncFit[problema], tamPop)

#configurações
a.maxGeracoes = 2000
a.elit = False
a.tipoSelecao = "roleta"
a.tamTorneio = 3
a.tipoCrossover = "pmx"
a.tipoMutacao = "swap"
a.txMut = 0.05#taxa de mutacao
a.txCross = 0.8#taxa de crossover

r = a.loopEvolucao()

a.geraGraficos(r)