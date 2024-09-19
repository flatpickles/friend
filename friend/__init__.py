import json
import os
import random
import re
from dataclasses import dataclass

from openai import OpenAI

from config import Config
from db import db
from db.models import Message


@dataclass
class Response:
    response_message: str
    user_name: str | None
    memorable_details: list[str]

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
    reply_txt = get_response(from_number).response_message
    message_to_user = Message(
        user_number=from_number,
        message=reply_txt,
        from_user=False
    )
    db.session.add(message_to_user)
    db.session.commit()
    return reply_txt

def get_response(user_number) -> Response:
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
    response_text: str = response.choices[0].message.content

    # Default values
    response_message = response_text
    user_name = None
    memorable_details = []

    # Extract JSON from response text (if it exists)
    try:
        match = re.search(r'{.*}', response_text, re.DOTALL)
        if match:
            response_json = match.group(0)
            response_data = json.loads(response_json)
            user_name = response_data.get("user_name")
            memorable_details = response_data.get("memorable_details", [])
            response_message = response_data.get("response_message", "")
    except json.JSONDecodeError:
        response_message = get_failure_message()

    # Create and return a Response object
    return Response(
        response_message=response_message,
        user_name=user_name,
        memorable_details=memorable_details
    )

def get_failure_message():
    failure_messages = [
        "whoops something went wrong, maybe try again?",
        "wait sorry what's going on?",
        "uh oh, my brain's a bit fuzzy. mind repeating that?",
        "oops, i think i missed something. can you say that again?",
        "hmm, i'm drawing a blank here. one more time?",
        "oh dang i totally spaced out. one more time?",
        "yikes, i'm having a moment. could you run that by me again?",
        "oh no, i think i short-circuited. can you repeat?",
        "dang, i'm not firing on all cylinders. wassup?",
    ]
    return random.choice(failure_messages)