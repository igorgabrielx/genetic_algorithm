from flask import Blueprint, request, jsonify
from controllers.genetic_controller import Genetic_Controller


genetic = Blueprint('genetic', __name__)
controller = Genetic_Controller()

@genetic.route("/help-check", methods=["GET"])
def api_help_check():
    return controller.help_check()

@genetic.route("execute-ag", methods=["POST"])
def api_execute_ag():
    return controller.execute_ag()

@genetic.route("execute-async-ag", methods=["POST"])
def api_start_async_ag():
    """Inicia a execução assíncrona do algoritmo genético."""
    return controller.start_async_ag()

@genetic.route("get-executions/<int:execution_id>", methods=["GET"])
def api_get_executions(execution_id):
    return controller.get_execution_id(execution_id)

@genetic.route("get-all-executions", methods=["GET"])
def api_get__all_executions():
    return controller.get_all_execution()

@genetic.route("get-status-queue/<int:queue_id>", methods=["GET"])
def api_get_status_queue(queue_id):
    return controller.get_queue_id(queue_id)

@genetic.route("/parameters/<int:param_id>", methods=["POST"])
def update_parameters(param_id):
    data = request.get_json()

    result = controller.update_param(
        param_id=param_id,
        taxa_mutation=data.get("taxa_mutation"),
        taxa_crossover=data.get("taxa_crossover"),
        pop_size=data.get("pop_size"),
        num_gen=data.get("num_gen")
    )

    status = 200 if "message" in result else 400
    return jsonify(result), status


