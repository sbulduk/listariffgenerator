from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    DEBUG=os.getenv("DEBUG","False").lower() in ["true","1","t"]
    PYTHONDONTWRITEBYTECODE=os.getenv("PYTHONDONTWRITEBYTECODE","0")=="1"
    HTTPSERVER=f"http://localhost:5000/api/tariff"
    # FILESPATH=os.path.join(os.getcwd(),"App","Files")