from flask import Blueprint, jsonify, render_template, request

web_bp = Blueprint("web", __name__)

@web_bp.route("/", methods=["GET"])
def index():
    return render_template("chat.html")

@web_bp.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response_message = handle_message(user_message)
    return jsonify({'response': response_message})

def handle_message(message):
    if message.lower() == 'hi':
        return "Hello from Flask!"
    else:
        return "I'm still learning. Try saying 'hi'."