import math
 
'''
FuncFit é um dicionario que contem as informações de diversos problemas para serem utilizadas no AG
Informações por problema:
nome        -> nome do problema
descricao   -> descricao do problema
codificacao -> tipo de codificacao
tamCrom      -> tamanho do cromossomo
boundMin    -> bound inferior
boundSup    -> bound superior
fitnessFunc -> funcao fitness para o problema
'''
def fitBitsAlt(cromossomo):
    '''Funcao fitness para problema dos bits alternados'''
    f = 0
    for i in range(len(cromossomo)-1):
        if cromossomo[i] == 1:
            if cromossomo[i+1] == 0:
                f += 1
        else:
            if cromossomo[i+1] == 1:
                f += 1
    return f
 
def fitParImpar(cromossomo):
    '''Funcao fitness para problema dos ints alternados par/impar'''
    f = 0
    for i in range(len(cromossomo)-1):
        if cromossomo[i]%2 == 1:
            if cromossomo[i+1]%2 == 0:
                f += 1
        else:
            if cromossomo[i+1]%2 == 1:
                f += 1
    return f
 
def ackleyFunc(cromossomo):
    '''Funcao fitness para problema da funcao ackley'''
    first_sum = 0.0
    second_sum = 0.0
    for v in range(len(cromossomo)):
        first_sum += cromossomo[v] ** 2.0
        second_sum += math.cos(2.0 * math.pi * cromossomo[v])
    n = float(len(cromossomo))
    result = -20.0*math.exp(-0.2*math.sqrt(first_sum/n)) - math.exp(second_sum/n) + 20 + math.e
    #return result
    return 1.0 - result/22.4#maio valor estimado
 
FuncFit = {
    "BitsAlternados" : {
        "nome" : "Bits Alternados",
        "descricao" : "Problema dos bits alternados em uma string binaria",
        "codificacao" : "BIN",
        "tamCrom" : 100,
        "boundMin" : 0,
        "boundMax" : 0,
        "fitnessFunc" : fitBitsAlt,
    },
    "ParImpar" : {
        "nome" : "Par Impar",
        "descricao" : "Problema dos digitos alternados par/impar",
        "codificacao" : "INT",
        "tamCrom" : 100,
        "boundMin" : -10,
        "boundMax" : 10,
        "fitnessFunc" : fitParImpar,
    },
    "AckleyReal" : {
        "nome" : "Ackley",
        "descricao" : "Funcao ackley com codificacao real",
        "codificacao" : "REAL",
        "tamCrom" : 20,
        "boundMin" : -32.0,
        "boundMax" : 32.0,
        "fitnessFunc" : ackleyFunc,
    }
}