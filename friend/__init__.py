import json
import os
import random
import re
from dataclasses import dataclass

from openai import OpenAI

from config import Config
from db import db
from db.models import Detail, Message, User


@dataclass
class Response:
    response_message: str
    user_name: str | None
    memorable_details: list[str]

# Create OpenAI client
client = OpenAI(
    api_key=Config.OPENAI_API_KEY,
)

# Read prompt templates once at startup
base_dir = os.path.dirname(__file__)
system_prompt_path = os.path.join(base_dir, 'system.txt')
info_prompt_path = os.path.join(base_dir, 'info.txt')
with open(system_prompt_path, 'r') as system_prompt_file:
    SYSTEM_PROMPT = system_prompt_file.read()
with open(info_prompt_path, 'r') as info_prompt_file:
    INFO_PROMPT = info_prompt_file.read()

def handle_message(incoming_msg, from_number):
    # Retrieve or create the user
    user = User.query.get(from_number)
    if not user:
        user = User(user_number=from_number)
        db.session.add(user)

    # Save the message to the db
    message_from_user = Message(
        user_number=from_number,
        message=incoming_msg,
        from_user=True
    )
    db.session.add(message_from_user)

    # Get the response from the AI
    response = get_response(user)

    # Save the name if it exists in the response
    if response.user_name:
        user.name = response.user_name

    # Save the memorable details if they exist in the response
    if response.memorable_details:
        for detail in response.memorable_details:
            detail_obj = Detail(
                user_number=from_number,
                detail=detail
            )
            db.session.add(detail_obj)

    # Save the response to the db
    message_to_user = Message(
        user_number=from_number,
        message=response.response_message,
        from_user=False
    )
    db.session.add(message_to_user)

    # Commit the changes to the db and return the response message
    db.session.commit()
    return response.response_message

def get_response(user: User) -> Response:
    # Create the system prompt using what we already know about the user
    additional_info = ""
    if user.name or (user.details and len(user.details) > 0):
        additional_info = INFO_PROMPT.format(
            user_name=(f" (named {user.name})" if user.name else ""),
            details=", ".join(detail.detail for detail in user.details)
        )
    system_prompt = SYSTEM_PROMPT.format(additional_info=additional_info)

    # Create the messages list
    messages = [
        {"role": "system", "content": system_prompt},
    ]

    # Retrieve the conversation history from the database
    conversation_history: list[Message] = user.messages

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
        "uh oh, i'm a bit fuzzy. mind repeating that?",
        "oops, i think i missed something. can you say that again?",
        "hmm, i'm drawing a blank here. one more time?",
        "oh dang i totally spaced out. one more time?",
        "yikes, i'm having a moment. could you run that by me again?",
        "oh no, i think i short-circuited. can you repeat?",
        "dang, i'm not firing on all cylinders. wassup?",
    ]
    return random.choice(failure_messages)