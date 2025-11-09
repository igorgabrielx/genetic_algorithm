
import sqlite3
from datetime import datetime

class GeneticDB:
    def __init__(self, db_name="genetic_algorithm.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

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
            max_fitness REAL
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

       self.conn.commit()

    def create_table(self):
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS executions_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_time TEXT,
                    end_time TEXT,
                    status TEXT
                )
            """)

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
