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
                datetime.datetime.now().isoformat(),
                ga.bit_size,
                ga.x_bit_size,
                ga.y_bit_size,
                ga.max,
                ga.min,
                ga.taxa_crossover,
                ga.taxa_mutation,
                ga.num_gen,
                ga.max_value
            ))
            self.db.conn.commit()
            return self.db.cursor.lastrowid
    
    def get_executions(self):
        """Retorna todas as execuções salvas na tabela executions"""
        try:
            self.db.cursor.execute('select * from executions order by date desc')
            rows = self.db.cursor.fetchall()

            # Transforma os resultados em uma lista de dicionários
            columns = [desc[0] for desc in self.db.cursor.description]
            results = [dict(zip(columns, row)) for row in rows]

            return results

        except Exception as e:
            print(f"Erro ao buscar execuções: {e}")
            return []
        
    def get_execution_by_id(self, execution_id):
        """Retorna uma execução específica pelo ID"""
        try:
            self.db.cursor.execute('select * from executions where id = ?', (execution_id,))
            row = self.db.cursor.fetchone()
            if not row:
                return None

            columns = [desc[0] for desc in self.db.cursor.description]
            return dict(zip(columns, row))

        except Exception as e:
            print(f"Erro ao buscar execução: {e}")
            return None