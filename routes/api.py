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

@genetic.route("execute-async-ag", methods=["GET"])
def api_start_async_ag():
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


