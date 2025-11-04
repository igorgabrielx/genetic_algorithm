from genetic_algorithm import Genetic_Algorithm 

if __name__ == "__main__":
   
   ag = Genetic_Algorithm()

   ag.initialize_population()

   ag.generate_fitness()

   while ag.num_gen < 4000:

      ag.select_parent()

      ag.beget_children()

      ag.mutation()

      ag.generate_fitness()

      ag.num_gen = ag.num_gen + 1

   print('Fim')

   print(f'Populacao Final: ${ag.population}')
   print(f'Resultado Populacao {ag.fitness}')

   
