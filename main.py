from genetic_algorithm import Genetic_Algorithm 

if __name__ == "__main__":
   
   ag = Genetic_Algorithm()

   ag.initialize_population()

   ag.generate_fitness()

   # num_gen = ag.num_gen 
   param_stop = 0
   while param_stop < ag.num_gen:   

      ag.select_parent()

      ag.beget_children()

      ag.mutation()

      ag.generate_fitness()

      param_stop = param_stop + 1

   print('Fim')
   ag.show()

   # print(f'Populacao Final: ${ag.population}')
   # print(f'Resultado Populacao {ag.fitness}')

   
