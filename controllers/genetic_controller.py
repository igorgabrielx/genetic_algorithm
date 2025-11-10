from models.executions import Executions
from models.executions_queue import Executions_queue
from models.executions_param import Executions_param
from genetic_algorithm import Genetic_Algorithm
from threading import Thread
from flask import request, jsonify

class Genetic_Controller:
    def __init__(self):
        self.execution = Executions()
        self.ex_queue = Executions_queue()
        self.ex_param = Executions_param()

    def help_check(self):
        return jsonify({"mensagem": "Bem-vindo à API do Algoritmo Genético!"})
    
    def start_async_ag(self):
        # queue_id = self.ex_queue.add_to_queue()
        # thread = Thread(target=self.execute_ag, args=(queue_id,))
        # thread.start()  
        # return jsonify({
        #     "message": "Execução adicionada à fila.",
        #     "execution_id": queue_id
        # })
        data = request.get_json(force=True)

        pop_size = data.get("pop_size", 100)
        taxa_crossover = data.get("taxa_crossover", 0.65)
        taxa_mutation = data.get("taxa_mutation", 0.008)
        num_gen = data.get("num_gen", 4000)
        
        queue_id = self.ex_queue.add_to_queue()

        thread = Thread(
            target=self.execute_ag,
            args=(queue_id, pop_size, taxa_crossover, taxa_mutation, num_gen)
        )
        thread.start()
    
    def execute_ag(self, queue_id, pop_size=100, taxa_crossover=0.65, taxa_mutation=0.008, num_gen=4000):
        try:
            
            self.ex_queue.update_queue_status(queue_id, "executando")

            ag = Genetic_Algorithm(
                pop_size=pop_size,
                taxa_crossover=taxa_crossover,
                taxa_mutation=taxa_mutation,
                num_gen=400
            )
            ag.initialize_population()
            ag.generate_fitness()

            while ag.num_gen < 400:
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

    def get_execution_id(self, id_execution):
        data = self.execution.get_execution_by_id(id_execution)
        return jsonify({
            "status": 200,
            "data": data
        })
    
    def get_queue_id(self, id_queue):
        data = self.ex_queue.get_queue_by_id(id_queue)
        return jsonify({
            "status": 200,
            "data": data
        })
    
    def get_all_execution(self):
        data = self.execution.get_executions()
        return jsonify({
            "status": 200,
            "data": data
        })
    
    def update_param(self, param_id, taxa_mutation=None, taxa_crossover=None, pop_size=None, num_gen=None):
        try:
            updated = self.ex_param.update_parameters(
                param_id,
                taxa_mutation=taxa_mutation,
                taxa_crossover=taxa_crossover,
                pop_size=pop_size,
                num_gen=num_gen
            )

            if updated:
                return {"message": "Parâmetros atualizados com sucesso!"}
            else:
                return {"error": "Nenhum registro atualizado ou ID não encontrado."}
        except Exception as e:
            return {"error": f"Erro ao atualizar parâmetros: {str(e)}"}


        
