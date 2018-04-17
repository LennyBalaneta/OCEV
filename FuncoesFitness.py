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
def fitBitsAlt():
    '''Funcao fitness para problema dos bits alternados'''
    return 1

FuncFit = {
    "BitsAlternados" : {
        "nome" : "Bits Alternados",
        "descricao" : "Problema dos bits alternados em uma string binaria",
        "codificacao" : "BIN",
        "tamCrom" : 100,
        "boundMin" : 0,
        "boundMax" : 0,
        "fitnessFunc" : fitBitsAlt,
    }
}

