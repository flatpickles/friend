# `friend`

This repository contains a friend you can talk to. It's a Flask app, using the SQLAlchemy ORM, and gpt-4o for intelligence.

`friend` will eventually be available over SMS (via Twilio), but it's taking time to get [A2P 10DLC](https://help.twilio.com/articles/1260800720410) compliance sorted. In the meantime, `friend` offers a [simple web interface](https://friend.flatpickles.com) for conversation.

## Ideas:

- shared context memory: a friend knows things about all its conversations at any given moment
- 0-N text responses: our friends might not text us back, or might respond with a couple messages
- delayed text responses: a friend will generally only respond immediately for urgent texts
