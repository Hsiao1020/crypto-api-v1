from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string 
import random

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return "User>>> {self.username}"

class BTC(db.Model):
    btc_datetime = db.Column(db.DateTime, primary_key=True)
    Open = db.Column(db.Float, nullable=False)
    High = db.Column(db.Float, nullable=False)
    Low = db.Column(db.Float, nullable=False)
    Close = db.Column(db.Float, nullable=False)
    Adj_Close = db.Column(db.Float, nullable=False)
    Volume = db.Column(db.Integer, nullable=False)
    # url = db.Column(db.Text, nullable=False)
    # short_url = db.Column(db.String(3), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    # def generate_short_characters(self):
    #     charaters = string.digits + string.ascii_letters
    #     picked_chars = ''.join(random.choices(charaters, k=3))
    #     link = self.query.filter_by(short_url=picked_chars).first()

    #     if link:
    #         self.generate_short_characters()
    #     else:
    #         return picked_chars


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.short_url = self.generate_short_characters()

