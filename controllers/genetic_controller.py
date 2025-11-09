from models.executions import Executions
from models.executions_queue import Executions_queue
from genetic_algorithm import Genetic_Algorithm
from threading import Thread
from flask import jsonify

class Genetic_Controller:
    def __init__(self):
        self.execution = Executions()
        self.ex_queue = Executions_queue()

    def help_check(self):
        return jsonify({"mensagem": "Bem-vindo à API do Algoritmo Genético!"})
    
    def start_async_ag(self):
        queue_id = self.ex_queue.add_to_queue()
        thread = Thread(target=self.execute_ag, args=(queue_id,))
        thread.start()  # inicia em background
        return jsonify({
            "message": "Execução adicionada à fila.",
            "execution_id": queue_id
        })
    
    def execute_ag(self, queue_id):
        try:
            
            self.ex_queue.update_queue_status(queue_id, "executando")

            ag = Genetic_Algorithm()
            ag.initialize_population()
            ag.generate_fitness()

            while ag.num_gen < 4000:
                ag.select_parent()
                ag.beget_children()
                ag.mutation()
                ag.generate_fitness()
                ag.num_gen += 1

            
            self.execution.save_execution(ag)
            self.ex_queue.update_queue_status(queue_id, "concluido")

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"[ERRO] Execução {queue_id} falhou: {e}\n{error_details}")
            self.ex_queue.update_queue_status(queue_id, "erro")

        finally:
            print(f"[INFO] Execução {queue_id} finalizada.")
