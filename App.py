from App import CreateApp
from flask_cors import CORS
from App.Routes.TariffGeneratorRoutes import tariffGeneratorBlueprint as tgb

class App(object):
    def __init__(self):
        self.app=CreateApp()
        CORS(self.app,origins=["http://localhost:3000"])

    def Run(self)->None:
        self.app.run(debug=self.app.config["DEBUG"])

if(__name__=="__main__"):
    app=App()
    app.Run()