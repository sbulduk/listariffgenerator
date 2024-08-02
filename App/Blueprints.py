from flask import Flask
from .Routes.TariffGeneratorRoutes import tariffGeneratorBlueprint as tgp

class Blueprints(object):
    @staticmethod
    def RegisterBlueprints(app:Flask)->None:
        app.register_blueprint(tgp)