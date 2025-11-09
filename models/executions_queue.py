from models.data_base import GeneticDB
import datetime

class Executions_queue:
    def __init__(self):
       self.db = GeneticDB()

    def add_to_queue(self):
        """Adiciona uma execução na fila como 'pendente'."""
        start_time = datetime.datetime.now().isoformat()
        self.db.cursor.execute(
            "insert into executions_queue (start_time, status) VALUES (?, ?)",
            (start_time, "pendente")
        )
        self.db.conn.commit()
        return self.db.cursor.lastrowid

    def update_queue_status(self, queue_id, status):
        """Atualiza o status de uma execução na fila."""
        end_time = datetime.datetime.now().isoformat() if status in ("concluido", "erro") else None
        self.db.cursor.execute(
            "UPDATE executions_queue SET status = ?, end_time = ? WHERE id = ?",
            (status, end_time, queue_id)
        )
        self.db.conn.commit()