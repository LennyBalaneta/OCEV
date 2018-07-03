from FuncoesFitness import FuncFit
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt

def buscaAleatoria(problema, avFunc):
    melhorSolucao = None
    melhorFit = 0
    
    fits = []
    maioresFit = []

    for i in range(avFunc):
        solucao = geraSolucao(problema)
        fit = problema["fitnessFunc"](solucao)
        if fit > melhorFit:
            melhorFit = fit
            melhorSolucao = deepcopy(solucao)
        
        if i % 1000000 == 0 and i != 0:
            print(i, ": ", melhorFit)
        maioresFit += [melhorFit]
        fits += [fit]
    problema["funcResultado"](melhorSolucao)
    return {"bF":maioresFit, "mF": fits}

def geraSolucao(problema):
    if problema["codificacao"] == "INT-PERM":
        return np.random.RandomState().permutation(problema["tamCrom"])
    elif problema["codificacao"] == "INT":
        return np.random.RandomState().randint(problema["boundMin"], problema["boundMax"], size=problema["tamCrom"])
    elif problema["codificacao"] == "BIN":
        return np.random.RandomState().randint(2, size=problema["tamCrom"])
    elif problema["codificacao"] == "REAL":
        return np.random.RandomState().uniform(problema["boundMin"], problema["boundMax"], size=problema["tamCrom"])
    else:
        raise Exception("Tipo de codificacao [", problema["codificacao"], "] indefinido")

def geraGraficos(result):
        #criacao dos graficos
        fig, ax = plt.subplots(1, 1)
        #grafico do maior
        ax.set_xlabel("Iteração")
        ax.set_ylabel("Fitness")
        ax.set_title("Fitness por iteração")
        ax.plot(result["mF"], label="Fitness da iteração", lw=1, ls="-")
        ax.legend(loc="upper left")
 
        plt.tight_layout()
        plt.show()

#n execucoes
execucoes = 10
qtdGer = 3000
resultados = []
for i in range(execucoes):
    print("Execucao", (i+1))
    
    resultados.append(buscaAleatoria(FuncFit["labirinto"], qtdGer))

somaBf = [0.0]*qtdGer
somaMf = [0.0]*qtdGer
melhorGeral = 0
for i in range(len(resultados)):#para cada execucao
    for j in range(len(somaBf)):#para cada geracao
        somaBf[j] += resultados[i]["bF"][j]
        somaMf[j] += resultados[i]["mF"][j]
    if(resultados[i]["bF"][-1] > melhorGeral):
        melhorGeral = resultados[i]["bF"][j]
        
for j in range(len(somaBf)):
    somaBf[j] /= execucoes
    somaMf[j] /= execucoes
rMedia = {"bF" : somaBf, "mF" : somaMf}
print("Melhor geral das", execucoes, "execucoes:", melhorGeral)
geraGraficos(rMedia)