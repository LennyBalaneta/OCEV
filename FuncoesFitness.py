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
funcResultado -> funcao de resultado para o problema
'''

#------------------------------Funcoes fitness para os problemas------------------------------
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
    
def tspFunc(cromossomo):
    '''Funcao fitness para problema do tsp'''
    
    #calcula apenas uma vez a matriz de distancias e guarda em uma variavel global
    global distanciasTSP
    if not "distanciasTSP" in globals():
        cidades = [(0.00, 0.20),
                   (0.15, 0.80),
                   (0.20, 0.65),
                   (0.90, 0.30),
                   (0.75, 0.45),
                   (0.30, 0.75),
                   (0.05, 0.05),
                   (0.95, 0.95),
                   (0.55, 0.55),
                   (0.85, 0.25)]
        distanciasTSP = []
        for i in range(len(cidades)):
            l = []
            for j in range(len(cidades)):
               l.append(math.sqrt((cidades[i][0]-cidades[j][0])**2 + (cidades[i][1]-cidades[j][1])**2))
            distanciasTSP.append(l)
    custo = 0.0
    
    for i in range(1, len(cromossomo)):
        custo += distanciasTSP[cromossomo[i-1]][cromossomo[i]]
    return (11.46 - custo)/11.46

def ackleyFuncBin(cromossomo):
    '''Funcao fitness para problema da funcao ackley com codificacao binaria'''
    vars = [ajuste(cromDecode(cromossomo, 0, 13), 13, -32.00, 32.00), ajuste(cromDecode(cromossomo, 13, 26), 13, -32.00, 32.00)]
    first_sum = 0.0
    second_sum = 0.0
    for v in range(len(vars)):
        first_sum += vars[v] ** 2.0
        second_sum += math.cos(2.0 * math.pi * vars[v])
    n = float(len(vars))
    result = -20.0*math.exp(-0.2*math.sqrt(first_sum/n)) - math.exp(second_sum/n) + 20 + math.e
    #return result
    return 1.0 - result/22.4#maio valor estimado
    
def _12maxFunc(cromossomo):
    '''Funcao fitness para problema da funcao de 12 maximos locais presente nos slides'''
    x = ajuste(cromDecode(cromossomo, 0, 16), 16, -2.0, 2.0)
    result = math.cos(20*x) - (math.sqrt(x**2)/2) + ((x**3)/4)
    return (result+4.0)/6.0
    
def radiosFit(cromossomo):
    '''Funcao de resultado para problema dos radios'''
    #st [0, 5] -> 0-24
    #lx [6, 9] -> 0-16
    st = math.floor(ajuste(cromDecode(cromossomo, 0, 5), 5, 0.0, 24.0))
    lx = math.floor(ajuste(cromDecode(cromossomo, 5, 9), 4, 0.0, 16.0))
    #restricao: st+2lx <= 40
    h = max(0, (st + 2*lx - 40)/16)
    fo = (30*st + 40*lx)/1360.0 - h
    return fo
    
#------------------------------Funcoes para mostrar resultado------------------------------
def resultBitsAlt(cromossomo):
    '''Funcao de resultado para problema dos bits alternados'''
    print("Melhor valor de f:", fitBitsAlt(cromossomo))
    print("Melhor solucao:", cromossomo)
    
def resultParImpar(cromossomo):
    '''Funcao de resultado para problema dos ints alternados par/impar'''
    print("Melhor valor de f:", fitParImpar(cromossomo))
    print("Melhor solucao:", cromossomo)
    
def resultAckley(cromossomo):
    '''Funcao de resultado para problema da funcao ackley'''
    
    #calculo do valor real de f
    first_sum = 0.0
    second_sum = 0.0
    for v in range(len(cromossomo)):
        first_sum += cromossomo[v] ** 2.0
        second_sum += math.cos(2.0 * math.pi * cromossomo[v])
    n = float(len(cromossomo))
    result = -20.0*math.exp(-0.2*math.sqrt(first_sum/n)) - math.exp(second_sum/n) + 20 + math.e
    
    print("Melhor valor de f:", result)
    print("Melhor solucao:", cromossomo)
    
def resultTsp(cromossomo):
    '''Funcao de resultado para problema do tsp'''
    #Melhor indivíduo para o TSP: [7 3 9 4 8 5 1 2 0 6]/[6 0 2 1 5 8 4 9 3 7] -> 2.4567852651255824
    
    #calculo do valor real de f
    custo = 0.0
    for i in range(1, len(cromossomo)):
        custo += distanciasTSP[cromossomo[i-1]][cromossomo[i]]
        
    print("Melhor valor de f:", custo)
    print("Melhor solucao:", cromossomo)
    
def resultAckleyBin(cromossomo):
    '''Funcao de resultado para problema da funcao ackley com codificacao binaria'''
    
    #calculo do valor real de f
    vars = [ajuste(cromDecode(cromossomo, 0, 13), 13, -32.00, 32.00), ajuste(cromDecode(cromossomo, 13, 26), 13, -32.00, 32.00)]
    first_sum = 0.0
    second_sum = 0.0
    for v in range(len(vars)):
        first_sum += vars[v] ** 2.0
        second_sum += math.cos(2.0 * math.pi * vars[v])
    n = float(len(vars))
    result = -20.0*math.exp(-0.2*math.sqrt(first_sum/n)) - math.exp(second_sum/n) + 20 + math.e
    
    print("Melhor valor de f:", result)
    print("Melhor solucao:", vars)
    print("Melhor solucao em binario:", cromossomo)
    
def result12Max(cromossomo):
    '''Funcao de resultado para problema dos 12 maximos locais presente nos slides'''
    x = ajuste(cromDecode(cromossomo, 0, 16), 16, -2.0, 2.0)
    
    print("Melhor valor de f:", math.cos(20*x) - (math.sqrt(x**2)/2) + ((x**3)/4))
    print("Melhor solucao:", x)
    print("Melhor solucao em binario:", cromossomo)
    
def resultRadios(cromossomo):
    '''Funcao de resultado para problema dos radios'''
    #calcula valor real da funcao
    st = math.floor(ajuste(cromDecode(cromossomo, 0, 5), 5, 0.0, 24.0))
    lx = math.floor(ajuste(cromDecode(cromossomo, 5, 9), 4, 0.0, 16.0))
    #restricao: st+2lx <= 40
    h = max(0, (st + 2*lx - 40)/16)
    fo = 30*st + 40*lx
    print("Melhor valor de f:", fo)
    print("Melhor solucao: st=", st, " | lx=", lx)
    if h == 0:
        print("Respeita restricoes")
    else:
        print("nao respeita restricoes")
    print("Melhor solucao em binario:", cromossomo)

#------------------------------Dicionário de informações dos problemas------------------------------    
FuncFit = {
    "BitsAlternados" : {
        "nome" : "Bits Alternados",
        "descricao" : "Problema dos bits alternados em uma string binaria",
        "codificacao" : "BIN",
        "tamCrom" : 100,
        "boundMin" : 0,
        "boundMax" : 0,
        "fitnessFunc" : fitBitsAlt,
        "funcResultado" : resultBitsAlt
    },
    "ParImpar" : {
        "nome" : "Par Impar",
        "descricao" : "Problema dos digitos alternados par/impar",
        "codificacao" : "INT",
        "tamCrom" : 100,
        "boundMin" : -10,
        "boundMax" : 10,
        "fitnessFunc" : fitParImpar,
        "funcResultado" : resultParImpar
    },
    "AckleyReal" : {
        "nome" : "Ackley",
        "descricao" : "Funcao ackley com codificacao real",
        "codificacao" : "REAL",
        "tamCrom" : 20,
        "boundMin" : -32.0,
        "boundMax" : 32.0,
        "fitnessFunc" : ackleyFunc,
        "funcResultado" : resultAckley
    },
    "TSP" : {
        "nome" : "TSP",
        "descricao" : "Problema do caixeiro viajante",
        "codificacao" : "INT-PERM",
        "tamCrom" : 10,
        "boundMin" : 0,
        "boundMax" : 0,
        "fitnessFunc" : tspFunc,
        "funcResultado" : resultTsp
    },
    "AckleyBin" : {
        "nome" : "AckleyReal",
        "descricao" : "Funcao ackley 2 dimensões, 2 casas de precisão com codificacao binaria",
        "codificacao" : "BIN",
        "tamCrom" : 26,
        "boundMin" : -32.0,
        "boundMax" : 32.0,
        "fitnessFunc" : ackleyFuncBin,
        "funcResultado" : resultAckleyBin
    },
    "12Max" : {
        "nome" : "12MaxLocais",
        "descricao" : "Funcao dos slides com 12 maximos locais",
        "codificacao" : "BIN",
        "tamCrom" : 16,
        "boundMin" : -2.0,
        "boundMax" : 2.0,
        "fitnessFunc" : _12maxFunc,
        "funcResultado" : result12Max
    },
    "Radios" : {
        "nome" : "Fabrica de radios",
        "descricao" : "Problema da fabrica de radios",
        "codificacao" : "BIN",
        "tamCrom" : 9,
        "boundMin" : 0,
        "boundMax" : 0,
        "fitnessFunc" : radiosFit,
        "funcResultado" : resultRadios
    }
}


#------------------------------Funções auxiliares------------------------------

def cromDecode(c, ini, fin):
    '''Recebe um cromossomo binario e retorna inteiro entre o intervalo [ini:fin]'''
    numTotal = c[ini:fin]
    numStr = ""
    for n in numTotal:
        numStr += str(n)
    return int(numStr, 2)

    
def ajuste(num, l, x_min, x_max):
        '''Recebe um numero inteiro, e coloca na escala desejada
           num      -> numero inteiro
           l        -> quantidade de bits do numero em binario
           x_min    -> bound inferior
           x_max    -> bound superior
        '''
        
        return x_min + ((x_max - x_min)/(2**l-1)) *  num