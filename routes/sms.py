from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse

from db import db
from db.models import Message
from friend import get_response

sms_bp = Blueprint("sms", __name__)

@sms_bp.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body")
    from_number = request.form.get("From")

    # Save the message to the db
    message_from_user = Message(
        user_number=from_number,
        message=incoming_msg,
        from_user=True
    )
    db.session.add(message_from_user)
    db.session.commit()

    # Create and save a response message
    reply_txt = get_response(from_number)
    message_to_user = Message(
        user_number=from_number,
        message=reply_txt,
        from_user=False
    )
    db.session.add(message_to_user)
    db.session.commit()

    # Reply to the user
    resp = MessagingResponse()
    resp.message(reply_txt)
    return str(resp)
    