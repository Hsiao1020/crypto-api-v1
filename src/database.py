from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import string 
import random

db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return "User>>> {self.username}"

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class BTC(db.Model):
    btc_datetime = db.Column(db.DateTime, primary_key=True)
    Open = db.Column(db.Float, nullable=False)
    High = db.Column(db.Float, nullable=False)
    Low = db.Column(db.Float, nullable=False)
    Close = db.Column(db.Float, nullable=False)
    Adj_Close = db.Column(db.Float, nullable=False)
    Volume = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class BTCSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BTC
