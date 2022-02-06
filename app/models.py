# coding: utf-8
from email.policy import default
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

from app.extensions import db
from app.utils import get_timestamp_now


class User(db.Model):
    __tablename__ = 'user'

    username = db.Column(db.String(30), primary_key=True)
    password_hash = db.Column(db.String(255))
    created_date = db.Column(INTEGER(unsigned=True), default=get_timestamp_now(), index=True)
    is_admin = db.Column(db.Boolean, default=0)
    avatar = db.Column(db.String(200))
    deck = db.Column(db.String(200))

    level = db.Column(INTEGER(unsigned=True), default=1)
    exp = db.Column(INTEGER(unsigned=True), default=0)
    health = db.Column(INTEGER(unsigned=True), default=100)
    gold = db.Column(INTEGER(unsigned=True), default=100)
    diamond = db.Column(INTEGER(unsigned=True), default=100)
    barrel = db.Column(INTEGER(unsigned=True), default=200)
    total_battle = db.Column(INTEGER(unsigned=True), default=0)
    win_battle = db.Column(INTEGER(unsigned=True), default=0)

    @classmethod
    def get_current_user(cls):
        return cls.query.get(get_jwt_identity())

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.get(_id)

    def get_deck(self):
        return self.deck.split(",")


class Card(db.Model):
    __tablename__ = 'card'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(INTEGER(unsigned=True), default=0)
    element = db.Column(INTEGER(unsigned=True), default=0)
    description = db.Column(db.String(500))
    attack = db.Column(INTEGER(unsigned=True), default=0)
    defend = db.Column(INTEGER(unsigned=True), default=0)
    army = db.Column(INTEGER(unsigned=True), default=0)
    created_date = db.Column(INTEGER(unsigned=True), default=get_timestamp_now(), index=True)

    # Xác suất ra khi đăng ký
    probability_register = db.Column(INTEGER(unsigned=True), default=100)

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.get(_id)


class UserCard(db.Model):
    __tablename__ = 'user_card'

    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(ForeignKey('user.username', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    card_id = db.Column(ForeignKey('card.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    rank = db.Column(INTEGER(unsigned=True), default=0)
    attack = db.Column(INTEGER(unsigned=True), default=0)
    defend = db.Column(INTEGER(unsigned=True), default=0)
    army = db.Column(INTEGER(unsigned=True), default=0)
    level = db.Column(INTEGER(unsigned=True), default=1)

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.get(_id)
