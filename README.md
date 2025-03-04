# `friend`

This repository contains a friend, designed for conversation via web & SMS. It's a Flask app, using the SQLAlchemy ORM, and gpt-4o for intelligence. At the moment, `friend` is not online.

## Ideas:

- more contextual knowledge: date, time, weather, current events...
- shared memory between different chats: a friend knows things about all its conversations at any given moment
- 0-N text responses: our friends might not text us back, or might respond with a couple messages
- delayed text responses: a friend will generally only respond immediately for urgent texts (SMS friend only, not live/web chat)
- incorporate time since last message (don't readily reference old messages)
