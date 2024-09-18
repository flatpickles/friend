from flask import Blueprint, jsonify, render_template, request

from friend import handle_message

web_bp = Blueprint("web", __name__)

@web_bp.route("/", methods=["GET"])
def index():
    return render_template("chat.html")

@web_bp.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    user_number = request.json.get('number')
    response_message = handle_message(user_message, user_number)
    return jsonify({'response': response_message})
