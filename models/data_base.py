
import sqlite3
from datetime import datetime

class GeneticDB:
    def __init__(self, db_name="genetic_algorithm.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()
        self.populate_default_parameters()

    def _create_tables(self):
       """Cria as tabelas principais e de fila de execuções se não existirem."""
        # Tabela principal das execuções do algoritmo genético
       self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS executions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            bit_size INTEGER,
            x_bit_size INTEGER,
            y_bit_size INTEGER,
            max REAL,
            min REAL,
            taxa_crossover REAL,
            taxa_mutation REAL,
            num_gen INTEGER,
            max_fitness REAL,
            chromosome_max_value TEXT      
        )
        ''')

        # Tabela da fila de execuções (controla tarefas pendentes ou em execução)
       self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS executions_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT,
            end_time TEXT,
            status TEXT CHECK(status IN ('pendente', 'executando', 'concluido', 'erro')) DEFAULT 'pendente'
        )
        ''')
       
       self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS execution_parameters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bit_size INTEGER,
                    x_bit_size INTEGER,
                    y_bit_size INTEGER,
                    pop_size INTEGER,
                    max REAL,
                    min REAL,
                    taxa_crossover REAL,
                    taxa_mutation REAL,
                    num_gen INTEGER
                )
        ''')

       self.conn.commit()

    def save_execution(self, ga):
        """Salva os atributos principais do algoritmo genético"""
        self.cursor.execute('''
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
        self.conn.commit()
        return self.cursor.lastrowid

    def close(self):
        self.conn.close()

    def populate_default_parameters(self):
        """
        Popula a tabela execution_parameters com os parâmetros padrão
        do algoritmo genético, caso ela esteja vazia.
        """
        # Verifica se já existe algum registro
        self.cursor.execute("SELECT COUNT(*) FROM execution_parameters")
        count = self.cursor.fetchone()[0]

        if count == 0:
            default_params = {
                "bit_size": 44,
                "x_bit_size": 22,
                "y_bit_size": 22,
                "pop_size": 100,
                "max": 100.0,
                "min": -100.0,
                "taxa_crossover": 0.65,
                "taxa_mutation": 0.008,
                "num_gen": 0
            }

            self.cursor.execute('''
                INSERT INTO execution_parameters 
                (bit_size, x_bit_size, y_bit_size, pop_size, max, min, taxa_crossover, taxa_mutation, num_gen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                default_params["bit_size"],
                default_params["x_bit_size"],
                default_params["y_bit_size"],
                default_params["pop_size"],
                default_params["max"],
                default_params["min"],
                default_params["taxa_crossover"],
                default_params["taxa_mutation"],
                default_params["num_gen"]
            ))

            self.conn.commit()
            print("Parâmetros padrão do algoritmo genético inseridos com sucesso!")
        else:
            print(" A tabela execution_parameters já possui registros. Nenhuma inserção feita.")

