from flask import Flask, jsonify, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods=['POST'])
def sms_reply():
    incoming_msg = request.form.get('Body')
    from_number = request.form.get('From')
    resp = MessagingResponse()
    response_txt = f"Hi! Your number is {from_number} and you said: {incoming_msg}"
    resp.message(response_txt)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)