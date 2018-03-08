import numpy as np

class Individuo():
    def __init__(self, tam, cod):
        self.min_bound = -10
        self.max_bound = 10
        self.cromossomo = self.init_cromossomo(tam, cod)
    
    def init_cromossomo(self, tamCrom, cod):
        if cod == "BIN":
            return np.random.randint(2, size=tamCrom)
        elif cod == "INT":
            return np.random.randint(self.min_bound, self.max_bound, size=tamCrom)
        elif cod == "REAL":
            return np.random.uniform(self.min_bound, self.max_bound, size=tamCrom)
        elif cod == "INT-PERM":
            return np.random.permutation(tamCrom)
        else:
            raise Exception("Codificacao invalida")
            
    def __str__(self):
        return np.array2string(self.cromossomo)
    
class Populacao():
    def __init__(self, tamPop, tamCrom, cod):
        self.individuos = [Individuo(tamCrom, cod) for i in range(tamPop)]
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
    