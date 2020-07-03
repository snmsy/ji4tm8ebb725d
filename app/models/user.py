from flask_login import UserMixin

from extensions import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    profile_pic = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.now())
