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
        return jsonify({
            "message": "Execução adicionada à fila.",
            "execution_id": queue_id
        })
    
    def execute_ag(self):
        ag = Genetic_Algorithm()

        ag.initialize_population()

        ag.generate_fitness()

        while ag.num_gen < 4000:

            ag.select_parent()

            ag.beget_children()

            ag.mutation()

            ag.generate_fitness()

            ag.num_gen = ag.num_gen + 1