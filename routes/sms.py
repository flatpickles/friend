from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse

from db import db
from db.models import Message
from friend import handle_message

sms_bp = Blueprint("sms", __name__)

@sms_bp.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body")
    from_number = request.form.get("From")

    # Reply to the user
    reply_txt = handle_message(incoming_msg, from_number)
    resp = MessagingResponse()
    resp.message(reply_txt)
    return str(resp)
    