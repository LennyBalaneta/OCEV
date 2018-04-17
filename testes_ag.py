import Populacao as p

a = p.Populacao(30, 100, "BIN")

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