import json
import os

from flask import Flask
from app.extensions import db
from app.models import Card, User
from app.settings import DevConfig, ProdConfig
from app.utils import get_timestamp_now

CONFIG = ProdConfig if os.environ.get('ENV') == 'prd' else DevConfig

default_file = "init_db/default.json"


class Worker:
    def __init__(self):
        app = Flask(__name__)

        app.config.from_object(CONFIG)
        db.app = app
        db.init_app(app)
        app_context = app.app_context()
        app_context.push()

        print("=" * 25, f"Starting migrate database on the uri: {CONFIG.SQLALCHEMY_DATABASE_URI}", "=" * 25)
        db.drop_all()
        db.create_all()  # create a new schema

        with open(default_file, encoding='utf-8') as file:
            self.default_data = json.load(file)

    def insert_default_items(self, key, constructor):
        now = get_timestamp_now()
        items = self.default_data.get(key, {})
        for item in items:
            instance = constructor()
            for key in item.keys():
                instance.__setattr__(key, item[key])
            if hasattr(instance, 'created_date'):
                instance.__setattr__('created_date', now)
                now += 1

            db.session.add(instance)

        db.session.commit()


if __name__ == '__main__':
    worker = Worker()
    worker.insert_default_items("users", User)
    # worker.insert_default_items("cards", Card)

    print("=" * 50, "Database migration completed", "=" * 50)
