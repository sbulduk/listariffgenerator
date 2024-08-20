from App import CreateApp
from flask_cors import CORS
from App.Routes.TariffGeneratorRoutes import tariffGeneratorBlueprint as tgb

class App(object):
    def __init__(self):
        self.app=CreateApp()
        # CORS(self.app,origins=["http://localhost:3000"])
        # CORS(self.app,resources={r"/*":{"origins":"http://localhost:3000"}})
        CORS(self.app,resources={r"/*":{"origins":"http://localhost:3000"}},
            supports_credentials=True,
            methods=["GET","POST","POST","DELETE","OPTIONS"],
            allow_headers=["Content-Type","Authorization","Access-Control-Allow-Credentials"])
        CORS(self.app)

    def Run(self)->None:
        self.app.run(debug=self.app.config["DEBUG"])

if(__name__=="__main__"):
    app=App()
    app.Run()