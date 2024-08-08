from flask import Blueprint,request,jsonify,current_app as app,send_from_directory
import os
from ..Services.ExcelService import ExcelService as es
from ..Services.TariffGeneratorService import TariffGeneratorService as tgs

tariffGeneratorBlueprint=Blueprint("tariffGeneratorBlueprint",__name__,url_prefix="/api/tariff")

FILES_DIRECTORY=os.path.join(os.getcwd(),"App","Files")
    
@tariffGeneratorBlueprint.route("/generatetargetfile",methods=["POST"])
def GenerateTargetFile():
    sourceFileName=request.json.get("sourceFileName")
    sourceSheetName=request.json.get("sourceSheetName")
    targetFileName=request.json.get("targetFileName")
    targetSheetName=request.json.get("targetSheetName")

    excelService=es(app.root_path)
    tariffGeneratorService=tgs(excelService)
    try:
        generatedTariffFile=tariffGeneratorService.GenerateTargetFile(sourceFileName,sourceSheetName,targetFileName,targetSheetName)
        if generatedTariffFile:
            fileUrl=f"/files/{targetFileName}"
            return jsonify({"success":True,"message":f"File generated successfully","url":f"{fileUrl}"})
        else:
            return jsonify({"success":False,f"message":"Error: Target file could not be generated"})
    except Exception as e:
        return jsonify({"success":False,"message":f"Error: {e}"})

@tariffGeneratorBlueprint.route("/files/<fileName>",methods=["GET"])
def DownloadFile(fileName:str):
    return send_from_directory(FILES_DIRECTORY,fileName)