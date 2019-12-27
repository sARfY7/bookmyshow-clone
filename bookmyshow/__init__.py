from bookmyshow.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from elasticsearch import Elasticsearch
from celery import Celery

# Initialize App and App Extensions
app = Flask(__name__) # Creating a new Flask App Instance
app.config.from_object(Config) # Add configuration to Flask App Instance
db = SQLAlchemy(app) # Creating a new Flask-SQLAlchemy instance by passing in Flask App Instance
bcrypt = Bcrypt(app) # Creating a new Flask-Bcrypt instance by passing in Flask App Instance
es = Elasticsearch() # Creating Elasticsearch intance for searching
celery = Celery(app.name, broker="redis://localhost:6379/0")
celery.conf.update(
    task_track_started=True,
    result_backend="redis://localhost:6379/0"
)

# Models Import
import bookmyshow.models

# Route Imports
from bookmyshow.main.routes import main
from bookmyshow.theatre.routes import theatre
from bookmyshow.user.routes import user
from bookmyshow.error.handlers import errors

# Blueprint Registerations
app.register_blueprint(main)
app.register_blueprint(theatre)
app.register_blueprint(user)
app.register_blueprint(errors)
