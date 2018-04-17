import Populacao as p
from FuncoesFitness import FuncFit

problema = "BitsAlternados"
tamPop = 30

a = p.Populacao(FuncFit[problema], tamPop)

#configurações
a.maxGeracoes = 2000
a.elit = True
a.tipoSelecao = "torneio"
a.tamTorneio = 3
a.tipoCrossover = "1pto"
a.tipoMutacao = "bitflip"
a.txMut = 0.03#taxa de mutacao
a.txCross = 0.8#taxa de crossover

r = a.loopEvolucao()

a.geraGraficos(r)