from datetime import datetime, timezone

from db import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_number = db.Column(db.String(15), nullable=False)
    message = db.Column(db.Text, nullable=False)
    from_user = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        from_txt = self.user_number if self.from_user else "Self"
        to_txt = "Self" if self.from_user else self.user_number
        return f"<Message from {from_txt} to {to_txt}: {self.message}>"