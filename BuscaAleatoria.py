from FuncoesFitness import FuncFit
from copy import deepcopy
import numpy as np

def buscaAleatoria(problema, avFunc):
    melhorSolucao = None
    melhorFit = 0
    
    for i in range(avFunc):
        solucao = geraSolucao(problema)
        fit = problema["fitnessFunc"](solucao)
        if fit > melhorFit:
            melhorFit = fit
            melhorSolucao = deepcopy(solucao)
        
        if i % 100 == 0:
            print(i, ": ", melhorFit)

    problema["funcResultado"](melhorSolucao)
    
    return (melhorSolucao, melhorFit)

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

buscaAleatoria(FuncFit["BitsAlternados"], 10000)