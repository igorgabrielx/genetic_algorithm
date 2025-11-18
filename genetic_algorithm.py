import random
import math

class Genetic_Algorithm:

    # def __init__(self):
    #    self.pop_size   =  100
    #    self.bit_size   =  44
    #    self.x_bit_size =  22
    #    self.y_bit_size =  22
    #    self.max        =  100
    #    self.min        = -100
    #    self.population = []
    #    self.fitness    = []
    #    self.selected_individuals = []
    #    self.num_gen = 0
    #    self.taxa_crossover = 0.65
    #    self.taxa_mutation = 0.008
    #    self.new_population = []
    #    self.max_value  = 0
    def __init__(
        self,
        pop_size=100,
        bit_size=44,
        x_bit_size=22,
        y_bit_size=22,
        max_val=100,
        min_val=-100,
        taxa_crossover=0.65,
        taxa_mutation=0.008,
        num_gen=0
    ):
        self.pop_size = pop_size
        self.bit_size = bit_size
        self.x_bit_size = x_bit_size
        self.y_bit_size = y_bit_size
        self.max = max_val
        self.min = min_val
        self.population = []
        self.fitness = []
        self.selected_individuals = []
        self.num_gen = num_gen
        self.taxa_crossover = taxa_crossover
        self.taxa_mutation = taxa_mutation
        self.new_population = []
        self.max_value = 0
        self.chromosome_max_value = ''

    def initialize_population(self):

        for _ in range(self.pop_size):

            chromosome = self.generate_chromosome()

            self.population.append(chromosome)

        return self.population

    def generate_chromosome(self):

        chromosome = ''

        for _ in range(self.bit_size):
             gene = ''
             gene = random.choice(['0','1'])
             chromosome = chromosome + gene

        return chromosome
    
    def decode_coord_x_y(self, chromosome):

        "Dividido em x e y:"
        x_bin = chromosome[self.x_bit_size:]
        y_bin = chromosome[:self.y_bit_size]

        "Convertendo para base 10"
        int_x = int(x_bin, 2)
        int_y = int(y_bin, 2)

        "Multiplicando por 200/2^22-1 e somando min"
        x = int_x * ( ( self.max - self.min ) / (pow(2, 22) - 1) ) + self.min
        y = int_y * ( ( self.max - self.min ) / (pow(2, 22) - 1) ) + self.min
        
        return x, y
    
    def F6(self, x, y):
        r_squared = pow(x,2) + pow(y,2)
        result = 0.5 - (math.sin(math.sqrt(r_squared))**2 - 0.5) / ((1.0 + 0.001 * r_squared)**2)

        return result
    
    def generate_fitness(self):
        self.fitness = []
        for i, p in enumerate(self.population):
            x, y = self.decode_coord_x_y(p)
      
            self.fitness.append(self.F6(x, y))

        self.max_value = max(self.fitness)

        best_index = self.fitness.index(self.max_value)

        self.chromosome_max_value = self.population[best_index] 
        print(f'Value: {self.max_value} - Chromosome: {self.chromosome_max_value} \n')
        

    def select_parent(self):
        total_fit = sum(self.fitness)
        prob_acum = []
        acum = 0
        
        for f in self.fitness:
            acum += f / total_fit
            prob_acum.append(acum)
        
        # Gira a roleta
        while len(self.selected_individuals) < self.population:

            r = random.random()

            for i, p in enumerate(prob_acum):
                if r <= p:
                    self.selected_individuals.append(self.population[i])
                    break
        
        print(f'Tamanho da populacao: {self.population}')
        print(f'Tamanho da populacao selecionada: {self.new_population}')
        print(f'Tamanho da populacao filhos: {self.selected_individuals}')

    def beget_children(self):
        r = random.random()
        
        self.new_population = max(self.selected_individuals)

        best_index = self.fitness.index(max(self.fitness))
        best_individual = self.population[best_index]
        self.new_population.append(best_individual)

        while len(self.new_population) < self.pop_size:

            for i, p in enumerate(self.selected_individuals):

                child_one = p

                if (i+1) >= len(self.selected_individuals):
                    child_two = p
                else:
                    child_two = self.selected_individuals[i+1]

                if r < self.taxa_crossover:
                    corte = random.randint(1, 44)
                    child_01 = child_one[:corte] + child_two[corte:]
                    child_02 = child_two[:corte] + child_one[corte:]
                else:
                    child_01 = child_two
                    child_02 = child_one
                
                self.new_population.append(child_01)
                self.new_population.append(child_02)

        self.population = self.new_population
        self.new_population = []
        self.selected_individuals = []
    
    def mutation(self):
        print('Iniciando Mutacao')
        pm = self.taxa_mutation

        for i, p in enumerate(self.population):
            # print(f'Antes da mutacao: {p}')

            # converte a string em lista de caracteres (mutável)
            genes = list(p)

            for j, gene in enumerate(genes):
                if random.random() < pm:
                    # print(f'Mutando gene na posição {j}')
                    # inverte o bit
                    genes[j] = '0' if gene == '1' else '1'

            # reconverte a lista de volta para string
            self.population[i] = ''.join(genes)
            # print(f'Depois da mutacao: {self.population[i]}')
                    


                 



            
            


    
    
