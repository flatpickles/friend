import os

from openai import OpenAI

from config import Config
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
