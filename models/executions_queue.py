from models.data_base import GeneticDB
import sqlite3
import datetime

class Executions_queue:
    def __init__(self):
        self.db_name = "genetic_algorithm.db"  # armazenamos o nome do banco apenas

    def get_connection(self):
        """Cria uma nova conexão e cursor para cada thread."""
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        cursor = conn.cursor()
        return conn, cursor

    def add_to_queue(self):
        """Adiciona uma execução na fila como 'pendente'."""
        start_time = datetime.datetime.now().isoformat()
        conn, cursor = self.get_connection()
        cursor.execute(
            "INSERT INTO executions_queue (start_time, status) VALUES (?, ?)",
            (start_time, "pendente")
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    def update_queue_status(self, queue_id, status):
        """Atualiza o status de uma execução na fila."""
        end_time = datetime.datetime.now().isoformat() if status in ("concluido", "erro") else None
        conn, cursor = self.get_connection()
        cursor.execute(
            "UPDATE executions_queue SET status = ?, end_time = ? WHERE id = ?",
            (status, end_time, queue_id)
        )
        conn.commit()
        conn.close()

    def get_queue_by_id(self, queue_id):
        """Busca uma execução da fila pelo ID."""
        conn, cursor = self.get_connection()
        cursor.execute("SELECT * FROM executions_queue WHERE id = ?", (queue_id,))
        row = cursor.fetchone()
        data = None
        if row:
            columns = [desc[0] for desc in cursor.description]
            data = dict(zip(columns, row))
        conn.close()
        return data
