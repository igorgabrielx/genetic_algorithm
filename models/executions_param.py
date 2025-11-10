from models.data_base import GeneticDB
import datetime

class Executions_param:
    def __init__(self):
          self.db = GeneticDB()
    
    def get_parameter_by_id(self, parameter_id):
        """Busca um parâmetro de execução pelo ID."""
        self.db.cursor.execute("SELECT pop_size, taxa_crossover, taxa_mutation, num_gen FROM execution_parameters WHERE id = ?", (parameter_id,))
        row = self.db.cursor.fetchone()

        if row:
            columns = [desc[0] for desc in self.db.cursor.description]
            return dict(zip(columns, row))
        return None
    
    def update_parameters(self, parameter_id, taxa_mutation=None, taxa_crossover=None, pop_size=None, num_gen=None):
        """
        Atualiza os parâmetros principais do algoritmo genético.
        Apenas os valores informados serão alterados.
        """
        updates = {}
        if taxa_mutation is not None:
            updates["taxa_mutation"] = taxa_mutation
        if taxa_crossover is not None:
            updates["taxa_crossover"] = taxa_crossover
        if pop_size is not None:
            updates["pop_size"] = pop_size
        if num_gen is not None:
            updates["num_gen"] = num_gen

        if not updates:
            return False
        
        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [parameter_id]

        self.db.cursor.execute(f"UPDATE execution_parameters SET {set_clause} WHERE id = ?", values)
        self.db.conn.commit()

        return self.db.cursor.rowcount > 0 
    def insert_parameters(
        self,
        bit_size,
        x_bit_size,
        y_bit_size,
        pop_size,
        max_value,
        min_value,
        taxa_crossover,
        taxa_mutation,
        num_gen
    ):
        """
        Insere um novo conjunto de parâmetros do algoritmo genético na tabela execution_parameters.
        Retorna o ID do registro inserido.
        """
        self.db.cursor.execute('''
            INSERT INTO execution_parameters 
            (bit_size, x_bit_size, y_bit_size, pop_size, max, min, taxa_crossover, taxa_mutation, num_gen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            bit_size,
            x_bit_size,
            y_bit_size,
            pop_size,
            max_value,
            min_value,
            taxa_crossover,
            taxa_mutation,
            num_gen
        ))
        self.db.conn.commit()
        return self.db.cursor.lastrowid
    

    