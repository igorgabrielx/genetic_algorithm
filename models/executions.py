from models.data_base import GeneticDB
import datetime

class Executions:
    def __init__(self):
          self.db = GeneticDB()

    def save_execution(self, ga):
            """Salva os atributos principais do algoritmo genético"""
            self.db.cursor.execute('''
            INSERT INTO executions 
            (date, bit_size, x_bit_size, y_bit_size, max, min, taxa_crossover, taxa_mutation, num_gen, max_fitness)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                ga.bit_size,
                ga.x_bit_size,
                ga.y_bit_size,
                ga.max,
                ga.min,
                ga.taxa_crossover,
                ga.taxa_mutation,
                ga.num_gen,
                ga.max_fitness
            ))
            self.db.conn.commit()
            return self.db.cursor.lastrowid