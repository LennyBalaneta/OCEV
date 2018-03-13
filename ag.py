import numpy as np
 
class Individuo():
    def __init__(self, tam, cod, minB, maxB):
        self.min_bound = minB
        self.max_bound = maxB
        self.cod = cod
        self.cromossomo = self.init_cromossomo(tam, cod)
 
    def init_cromossomo(self, tamCrom, cod):
        if cod == "BIN":
            return np.random.RandomState().randint(2, size=tamCrom)
        elif cod == "INT":
            return np.random.RandomState().randint(self.min_bound, self.max_bound, size=tamCrom)
        elif cod == "REAL":
            return np.random.RandomState().uniform(self.min_bound, self.max_bound, size=tamCrom)
        elif cod == "INT-PERM":
            return np.random.RandomState().permutation(tamCrom)
        else:
            raise Exception("Codificacao invalida")
 
    def fitness(self):
        if self.cod == "BIN":
            f = 0
            for i in range(len(self.cromossomo)-1):
                if self.cromossomo[i] == 1:
                    if self.cromossomo[i+1] == 0:
                        f += 1
                else:
                    if self.cromossomo[i+1] == 1:
                        f += 1
            return f
        elif self.cod == "INT":
            return 0
        elif self.cod == "REAL":
            return 0
        elif self.cod == "INT-PERM":
            return 0
        else:
            raise Exception("Codificacao invalida")
 
    def __str__(self):
        return np.array2string(self.cromossomo)
 
class Populacao():
    def __init__(self, tamPop, tamCrom, cod, minB=-10, maxB=10):
        self.individuos = [Individuo(tamCrom, cod, minB, maxB) for i in range(tamPop)]
        self.tamCrom = tamCrom
 
    def popFitness(self):
        s = "Individuos->Fitness:\n"
        for i in self.individuos:
            s += str(i) + " -> " + str(i.fitness()) +"\n"
        return s
 
    def centroid(self):
        cent = []
        for i in range(self.tamCrom):#n dimensões
            s = 0
            for j in range(len(self.individuos)):
                s += self.individuos[j].cromossomo[i]
            cent += [s/len(self.individuos)]
        return cent
 
    def inertia(self):
        c = self.centroid()
        i = 0
        for i in range(len(self.individuos)):
            iC = 0
            maioriC = 0
            for j in range(len(self.individuos[i].cromossomo)):
                iC += (self.individuos[i].cromossomo[j] - c[j]) ** 2
                #print(self.individuos[i].cromossomo[j])
            if iC > maioriC:
                maioriC = iC
            i += iC
 
        return i/maioriC
 
    def __str__(self):
        s = "Individuos:\n"
        for i in self.individuos:
            s += str(i) + "\n"
        return s
 
def main():
    pop = Populacao(5, 5, "REAL")
    print(pop)
 
if __name__ == "__main__":
    main()