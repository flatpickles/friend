import os

from openai import OpenAI

from config import Config
from db import db
from db.models import Message

# Create OpenAI client
client = OpenAI(
    api_key=Config.OPENAI_API_KEY,
)

# Read system prompt template once at startup
base_dir = os.path.dirname(__file__)
system_prompt_path = os.path.join(base_dir, 'system.txt')
with open(system_prompt_path, 'r') as file:
    SYSTEM_PROMPT = file.read()

def handle_message(incoming_msg, from_number):
    # Save the message to the db
    message_from_user = Message(
        user_number=from_number,
        message=incoming_msg,
        from_user=True
    )
    db.session.add(message_from_user)
    db.session.commit()

    # Create, save, and return a response message
    reply_txt = get_response(from_number)
    message_to_user = Message(
        user_number=from_number,
        message=reply_txt,
        from_user=False
    )
    db.session.add(message_to_user)
    db.session.commit()
    return reply_txt

def get_response(user_number):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},  # Use the pre-loaded system prompt
    ]

    # Retrieve the conversation history from the database
    conversation_history = Message.query.filter_by(user_number=user_number).order_by(Message.timestamp).all()

    # Add conversation history to the messages list
    for message in conversation_history:
        messages.append({
            "role": "user" if message.from_user else "assistant",
            "content": message.message
        })

    # Generate the response using OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=150,
        temperature=0.7
    )

    # Extract the response text from the OpenAI response
    response_text = response.choices[0].message.content

    return response_text
