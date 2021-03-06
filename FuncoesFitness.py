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
 
def rainhasFit(cromossomo):
    n = int(len(cromossomo)/2)
    conf = 0
    for i in range(n - 1):#0 a 6
        for j in range(i+1, n):#i a 7
            if cromossomo[i*2] == cromossomo[j*2]:#linha
                #print("Colisao L: ", i, "|", j)
                conf += 1
            if cromossomo[i*2+1] == cromossomo[j*2+1]:#coluna
                #print("Colisao C: ", i, "|", j)
                conf += 1
            if cromossomo[i*2]+cromossomo[i*2+1] == cromossomo[j*2]+cromossomo[j*2+1]:#diagonal 1 x1+y1 == x2+y2
                #print("Colisao D1: ", i, "|", j)
                conf += 1
            if cromossomo[i*2]-cromossomo[i*2+1] == cromossomo[j*2]-cromossomo[j*2+1]:#diagonal 2 x1-y1 == x2-y2
                #print("Colisao D2: ", i, "|", j)
                conf += 1
    m = (((n-1)*(n))/2) * 4
    #print("Conf:", conf)
    #print("n:", n)
    #print("m:", m)
    return (m - conf)/m
 
def rainhasFitBIN(cromossomo):
    pos = []
    n = int(len(cromossomo)/6)
    for i in range(n):
        pos.append(math.floor(ajuste(cromDecode(cromossomo, i*6, i*6+3), 3, 0.0, float(n-1))))
        pos.append(math.floor(ajuste(cromDecode(cromossomo, i*6+3, i*6+6), 3, 0.0, float(n-1))))
 
    conf = 0
    for i in range(n - 1):#0 a 6
        for j in range(i+1, n):#i a 7
            if pos[i*2] == pos[j*2]:#linha
                #print("Colisao L: ", i, "|", j)
                conf += 1
            if pos[i*2+1] == pos[j*2+1]:#coluna
                #print("Colisao C: ", i, "|", j)
                conf += 1
            if pos[i*2]+pos[i*2+1] == pos[j*2]+pos[j*2+1]:#diagonal 1 x1+y1 == x2+y2
                #print("Colisao D1: ", i, "|", j)
                conf += 1
            if pos[i*2]-pos[i*2+1] == pos[j*2]-pos[j*2+1]:#diagonal 2 x1-y1 == x2-y2
                #print("Colisao D2: ", i, "|", j)
                conf += 1
    m = (((n-1)*(n))/2) * 4
    #print("Conf:", conf)
    #print("n:", n)
    #print("m:", m)
    return (m - conf)/m
 
def rainhasFitPerm(cromossomo):
    n = len(cromossomo)
    conf = 0
    for i in range(n-1):#0 a 6
        for j in range(i+1, n):#i a 7
            if abs(i-j) == abs(cromossomo[i]-cromossomo[j]):
                conf += 1
    m = ((n-1) * n) / 2
    return (m - conf) / m
 
def rainhasFitPerm2(cromossomo):
    n = len(cromossomo)
    qtd = 1
    tab = [(0, cromossomo[0])]
    for i in range(1, n):#0 a 6
        conf = False
        for j in range(len(tab)):#i a 7
            if abs(i-tab[j][0]) == abs(cromossomo[i]-tab[j][1]):
                conf = True
                break
        if conf == False:
            qtd += 1
            tab.append((j, cromossomo[j]))
 
    return qtd / n
 
def rainhasFitPermL(cromossomo):
    n = len(cromossomo)
 
    #calcula apenas uma vez a matriz de lucros e guarda em uma variavel global
    global lucros, maxLuc
    if not "lucros" in globals():
        lucros = []
        c = 1
        for i in range(n):
            l = []
            for j in range(n):
                if i % 2 == 0:
                    l.append(math.sqrt(c))
                else:
                    l.append(math.log(c, 10.0))
                c += 1
            lucros.append(l)
        maxLuc = 0
        for i in range(n):
            maxLuc += lucros[i][n-1]#soma da diagonal principal
        print("maxLuc:", maxLuc)
 
    #calculo da primeira parte do fitness
    conf = 0
    for i in range(n-1):#0 a 6
        for j in range(i+1, n):#i a 7
            if abs(i-j) == abs(cromossomo[i]-cromossomo[j]):
                conf += 1
    m = ((n-1) * n) / 2
 
    fit = (m - conf) / m#fitness base
 
    #se achou uma solucao otima, adiciona o valor do lucro
    peso = 0.8
    fit *= peso
    somaLucro = 0
    if fit == peso:
        for i in range(n):
            somaLucro += lucros[i][cromossomo[i]]
        fit += (somaLucro/maxLuc)*(1.0-peso)#20% para cada parte
    return fit
 
def rainhasFitPermLPen(cromossomo):
    n = len(cromossomo)
 
    #calcula apenas uma vez a matriz de lucros e guarda em uma variavel global
    global lucros, maxLuc
    if not "lucros" in globals():
        lucros = []
        c = 1
        for i in range(n):
            l = []
            for j in range(n):
                if i % 2 == 0:#impares
                    l.append(math.sqrt(c))
                else:#pares
                    l.append(math.log(c, 10.0))
                c += 1
            lucros.append(l)
        maxLuc = 0
        for i in range(n):
            maxLuc += lucros[i][n-1]#soma da diagonal principal
 
    #calculo da primeira parte do fitness
    conf = 0
    for i in range(n-1):#0 a 6
        for j in range(i+1, n):#i a 7
            if abs(i-j) == abs(cromossomo[i]-cromossomo[j]):
                conf += 1
    m = ((n-1) * n) / 2
 
    somaLucro = 0
    for i in range(n):
        somaLucro += lucros[i][cromossomo[i]]
 
    fit = somaLucro / maxLuc#fitness base
 
    h = conf/m
 
    fo = max(0, fit - h)
 
    return fo

def labirintoFit(cromossomo):
    global labirintoBoard
    if not "labirintoBoard" in globals():
        labirintoBoard = [
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,2,1,1,0,0],
                    [0,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,1,0],
                    [0,1,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,0],
                    [0,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1,1,1,0],
                    [0,1,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,0,1,0],
                    [0,1,0,0,0,0,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0],
                    [0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,1,0],
                    [0,1,1,1,1,1,1,1,0,1,1,0,1,1,1,0,1,0,1,0,1,0,1,1,0],
                    [0,0,0,0,0,0,1,1,0,1,1,0,1,1,1,0,1,0,1,0,1,0,0,1,0],
                    [0,3,1,1,1,0,1,0,0,1,1,0,1,0,0,0,1,0,1,0,1,0,1,1,0],
                    [0,1,0,0,1,0,1,0,0,1,1,0,1,0,0,0,1,0,1,0,1,1,1,1,0],
                    [0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,1,0],
                    [0,1,0,0,1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,0],
                    [0,1,0,0,1,0,1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0],
                    [0,1,1,0,1,0,0,1,1,1,0,0,0,0,0,1,1,1,1,0,1,0,0,1,0],
                    [0,1,1,0,1,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,1,0,1,1,0],
                    [0,0,1,0,1,0,1,1,0,0,0,0,0,0,0,1,1,1,1,0,1,0,1,0,0],
                    [0,1,1,0,0,0,1,1,0,1,1,1,1,0,0,0,0,0,1,0,1,1,1,1,0],
                    [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,0,0,1,0],
                    [0,0,0,0,1,0,0,0,0,1,1,0,1,1,1,0,1,0,1,0,1,1,0,1,0],
                    [0,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,0,1,0,1,0],
                    [0,1,1,0,1,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0],
                    [0,1,1,0,1,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,0],
                    [0,1,1,0,1,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0],
                    [0,1,1,0,1,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,0,1,0,1,0],
                    [0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,0,1,1,1,1,1,0],
                    [0,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0],
                    [0,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                ]
    #dir:
    #0 -> cima
    #1 -> direita
    #2 -> baixo
    #3 -> esquerda
    
    distMax = abs(0 - 24) + abs(0 - 29)
    atualX = 1
    atualY = 10
    melhorX = 1
    melhorY = 1
    melhorDist = distMax
    fimX = 20
    fimY = 1
    visitados = [[10, 1]]

    for gene in cromossomo:
        movimentos = movimentosPossiveis(atualX, atualY, visitados)
        if len(movimentos) > 0:
            dir = movimentos[gene % len(movimentos)]
            if dir == 0:
                if labirintoBoard[atualY-1][atualX] != 0:
                    atualY -= 1
                    visitados.append([atualY, atualX])
            elif dir == 1:
                if labirintoBoard[atualY][atualX+1] != 0:
                    atualX += 1
                    visitados.append([atualY, atualX])
            elif dir == 2:
                if labirintoBoard[atualY+1][atualX] != 0:
                    atualY += 1
                    visitados.append([atualY, atualX])
            else:
                if labirintoBoard[atualY][atualX-1] != 0:
                    atualX -= 1
                    visitados.append([atualY, atualX])
            distDest = abs(atualX - fimX) + abs(atualY - fimY)
            if distDest < melhorDist:
                melhorDist = distDest
                melhorX = atualX
                melhorY = atualY
            if labirintoBoard[atualY][atualX] == 2:#saida
                break
        
    distDest = abs(melhorX - fimX) + abs(melhorY - fimY)
    fit = 1.0 - distDest/distMax
    
    return fit
 
def movimentosPossiveis(x, y, visitados):
    movs = []
    #cima
    if labirintoBoard[y-1][x] != 0 :
        if [y-1, x] not in visitados:
            movs.append(0)
    #direita
    if labirintoBoard[y][x+1] != 0 :
        if [y, x+1] not in visitados:
            movs.append(1)
    #baixo
    if labirintoBoard[y+1][x] != 0 :
        if [y+1, x] not in visitados:
            movs.append(2)
    #esquerda
    if labirintoBoard[y][x-1] != 0 :
        if [y, x-1] not in visitados:
            movs.append(3)
    return movs
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
 
def resultRainhas(cromossomo):
    '''Funcao de resultado para problema das rainhas'''
    n = int(len(cromossomo)/2)
    m = (((n-1)*(n))/2) * 4
    f = rainhasFit(cromossomo)
    conf = m - m*f
    print("Melhor valor de f:", rainhasFit(cromossomo))
    print("Melhor solucao:", cromossomo)
    print("Quantidade de colisoes:", conf)
 
def resultRainhasBIN(cromossomo):
    '''Funcao de resultado para problema das rainhas binario'''
    pos = []
    n = int(len(cromossomo)/6)
    for i in range(n):
        pos.append(math.floor(ajuste(cromDecode(cromossomo, i*6, i*6+3), 3, 0.0, float(n-1))))
        pos.append(math.floor(ajuste(cromDecode(cromossomo, i*6+3, i*6+6), 3, 0.0, float(n-1))))
    m = (((n-1)*(n))/2) * 4
    f = rainhasFitBIN(cromossomo)
    conf = m - m*f
    print("Melhor valor de f:", rainhasFitBIN(cromossomo))
    print("Melhor solucao:", pos)
    print("Melhor solucao binario:", cromossomo)
    print("Quantidade de colisoes:", int(conf))
 
def resultRainhasPerm(cromossomo):
    '''Funcao de resultado para problema das rainhas permutado'''
    n = len(cromossomo)
    conf = 0
    for i in range(n-1):#0 a 6
        for j in range(i+1, n):#i a 7
            if abs(i-j) == abs(cromossomo[i]-cromossomo[j]):
                conf += 1
    m = ((n-1) * n) / 2
    fit = (m - conf) / m
 
    pos = []
    for i in range(n):
        pos.append((i, cromossomo[i]))
 
    print("Melhor valor de f:", fit)
    print("Melhor solucao(coordenadas):", pos)
    print("Melhor solucao permutada:", cromossomo)
    print("Quantidade de colisoes:", int(conf))
 
def resultRainhasPerm2(cromossomo):
    '''Funcao de resultado para problema das rainhas permutado'''
    n = len(cromossomo)
    qtd = 1
    tab = [(0, cromossomo[0])]
    for i in range(1, n):#0 a 6
        conf = False
        for j in range(len(tab)):#i a 7
            if abs(i-tab[j][0]) == abs(cromossomo[i]-tab[j][1]):
                conf = True
                break
        if conf == False:
            qtd += 1
            tab.append((j, cromossomo[j]))
 
    fit = qtd / n
 
    pos = []
    for i in range(n):
        pos.append((i, cromossomo[i]))
 
    print("Melhor valor de f:", fit)
    print("Melhor solucao(coordenadas):", pos)
    print("Melhor solucao permutada:", cromossomo)
    print("Quantidade de rainhas posicionadas:", int(qtd))

 
def resultRainhasPermL(cromossomo):
    n = len(cromossomo)
    #calculo da primeira parte do fitness
    conf = 0
    for i in range(n-1):#0 a 6
        for j in range(i+1, n):#i a 7
            if abs(i-j) == abs(cromossomo[i]-cromossomo[j]):
                conf += 1
    m = ((n-1) * n) / 2
 
    fit = (m - conf) / m#fitness base
 
    #se achou uma solucao valida, adiciona o valor do lucro
    peso = 0.6
    fit *= peso
    somaLucro = 0
    if fit == peso:
        for i in range(n):
            somaLucro += lucros[i][cromossomo[i]]
        fit += (somaLucro/maxLuc)*(1.0-peso)
 
    pos = []
    for i in range(n):
        pos.append((i, cromossomo[i]))
 
    print("Melhor valor de f:", fit)
    print("Melhor solucao(coordenadas):", pos)
    print("Melhor solucao permutada:", cromossomo)
    print("Quantidade de colisoes:", int(conf))
    print("Lucro obtido:", somaLucro)
 
def resultRainhasPermLPen(cromossomo):
    n = len(cromossomo)
    #calculo da primeira parte do fitness
    conf = 0
    for i in range(n-1):#0 a 6
        for j in range(i+1, n):#i a 7
            if abs(i-j) == abs(cromossomo[i]-cromossomo[j]):
                conf += 1
    m = ((n-1) * n) / 2
 
    somaLucro = 0
    for i in range(n):
        somaLucro += lucros[i][cromossomo[i]]
 
    fit = somaLucro / maxLuc#fitness base
 
    h = conf/m
 
    fo = max(0, fit - h)
 
 
 
    pos = []
    for i in range(n):
        pos.append((i, cromossomo[i]))
 
    print("Melhor valor de f:", fo)
    print("Melhor solucao(coordenadas):", pos)
    print("Melhor solucao permutada:", cromossomo)
    print("Quantidade de colisoes:", int(conf))
    print("Lucro obtido:", somaLucro)

def resultLabirinto(cromossomo):
    distMax = abs(0 - 24) + abs(0 - 29)
    atualX = 1
    atualY = 10
    melhorX = 1
    melhorY = 1
    melhorDist = distMax
    fimX = 20
    fimY = 1
    visitados = [[10, 1]]

    for gene in cromossomo:
        movimentos = movimentosPossiveis(atualX, atualY, visitados)
        if len(movimentos) > 0:
            dir = movimentos[gene % len(movimentos)]
            if dir == 0:
                if labirintoBoard[atualY-1][atualX] != 0:
                    atualY -= 1
                    visitados.append([atualY, atualX])
            elif dir == 1:
                if labirintoBoard[atualY][atualX+1] != 0:
                    atualX += 1
                    visitados.append([atualY, atualX])
            elif dir == 2:
                if labirintoBoard[atualY+1][atualX] != 0:
                    atualY += 1
                    visitados.append([atualY, atualX])
            else:
                if labirintoBoard[atualY][atualX-1] != 0:
                    atualX -= 1
                    visitados.append([atualY, atualX])
            distDest = abs(atualX - fimX) + abs(atualY - fimY)
            if distDest < melhorDist:
                melhorDist = distDest
                melhorX = atualX
                melhorY = atualY
            if labirintoBoard[atualY][atualX] == 2:#saida
                break
        
    distDest = abs(melhorX - fimX) + abs(melhorY - fimY)
    fit = 1.0 - distDest/distMax

    print("Melhor valor de f:", fit)
    print("Valores finais: x=", melhorX, " | y=", melhorY)
    print("Distancia da saida:", distDest)
    print("Quantidade de movimentos executados:", len(visitados))
    print("Nos visitados:", visitados)
    print("Melhor solucao:", cromossomo)
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
    },
    "rainhas" : {
        "nome" : "Rainhas",
        "descricao" : "Problema das rainhas",
        "codificacao" : "INT",
        "tamCrom" : 8,#2 * qtd de rainhas
        "boundMin" : 0,#0
        "boundMax" : 3,#qtd de rainhas - 1
        "fitnessFunc" : rainhasFit,
        "funcResultado" : resultRainhas
    },
    "rainhasBIN" : {
        "nome" : "Rainhas BIN",
        "descricao" : "Problema das rainhas com codificacao binaria",
        "codificacao" : "BIN",
        "tamCrom" : 384,#6 * qtd de rainhas
        "boundMin" : 0,#0
        "boundMax" : 63,#qtd de rainhas - 1
        "fitnessFunc" : rainhasFitBIN,
        "funcResultado" : resultRainhasBIN
    },
    "rainhasPERM" : {
        "nome" : "Rainhas PERM",
        "descricao" : "Problema das rainhas com codificacao permutada",
        "codificacao" : "INT-PERM",
        "tamCrom" : 128,#qtd de rainhas
        "boundMin" : 0,
        "boundMax" : 0,
        "fitnessFunc" : rainhasFitPerm,
        "funcResultado" : resultRainhasPerm
    },
    "rainhasPERM2" : {
        "nome" : "Rainhas PERM",
        "descricao" : "Problema das rainhas com codificacao permutada",
        "codificacao" : "INT-PERM",
        "tamCrom" : 64,#qtd de rainhas
        "boundMin" : 0,
        "boundMax" : 0,
        "fitnessFunc" : rainhasFitPerm2,
        "funcResultado" : resultRainhasPerm2
    },
    "rainhasPERML" : {
        "nome" : "Rainhas PERM com lucro",
        "descricao" : "Problema das rainhas com codificacao permutada com lucro",
        "codificacao" : "INT-PERM",
        "tamCrom" : 8,#qtd de rainhas
        "boundMin" : 0,
        "boundMax" : 0,
        "fitnessFunc" : rainhasFitPermL,
        "funcResultado" : resultRainhasPermL
    },
    "rainhasPERMLPEN" : {
        "nome" : "Rainhas PERM com lucro com penalidades",
        "descricao" : "Problema das rainhas com codificacao permutada com lucro com penalidades",
        "codificacao" : "INT-PERM",
        "tamCrom" : 8,#qtd de rainhas
        "boundMin" : 0,
        "boundMax" : 0,
        "fitnessFunc" : rainhasFitPermLPen,
        "funcResultado" : resultRainhasPermLPen
    },
    "labirinto" : {
        "nome" : "Navegacao no labirinto",
        "descricao" : "Problema da navegacao no labirinto",
        "codificacao" : "INT",
        "tamCrom" : 100,#qtd de rainhas
        "boundMin" : 0,
        "boundMax" : 12,
        "fitnessFunc" : labirintoFit,
        "funcResultado" : resultLabirinto
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