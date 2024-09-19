from datetime import datetime, timezone

from db import db


class User(db.Model):
    user_number = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    messages = db.relationship('Message', backref='user', lazy=True)
    details = db.relationship('Detail', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.user_number}: {self.name}>"

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_number = db.Column(db.String(15), db.ForeignKey('user.user_number', name='fk_message_user_number'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    from_user = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        from_txt = self.user_number if self.from_user else "Self"
        to_txt = "Self" if self.from_user else self.user_number
        return f"<Message from {from_txt} to {to_txt}: {self.message}>"

class Detail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_number = db.Column(db.String(15), db.ForeignKey('user.user_number', name='fk_detail_user_number'), nullable=False)
    detail = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Detail for {self.user_number}: {self.detail}>"
