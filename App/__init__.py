from flask import Flask
from .Config import Config
from .Blueprints import Blueprints

def CreateApp()->Flask:
    app=Flask(__name__)
    app.config.from_object(Config)
    app.config.from_pyfile("Config.py",silent=True)
    Blueprints.RegisterBlueprints(app)
    return app