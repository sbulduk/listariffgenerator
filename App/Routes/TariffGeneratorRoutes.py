from flask import Blueprint,request,jsonify,current_app as app,send_from_directory
from ..Services.ExcelService import ExcelService as es
from ..Services.TariffGeneratorService import TariffGeneratorService as tgs
import os

tariffGeneratorBlueprint=Blueprint("tariffGeneratorBlueprint",__name__,url_prefix="/api/tariff")
    
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
            fileUrl=f"{request.host_url}/api/tariff/files/{targetFileName}"
            return jsonify({
                "success":True,
                "message":f"File generated successfully",
                "url":fileUrl
            }),200
        else:
            return jsonify({"success":False,f"message":"Error: Target file could not be generated"}),400
    except Exception as e:
        return jsonify({"success":False,"message":f"Error: {e}"}),500

@tariffGeneratorBlueprint.route("/files/<path:fileName>",methods=["GET"])
def DownloadFile(fileName:str):
    try:
        localDirectory=os.path.join(app.root_path,"Files")
        if not os.path.exists(os.path.join(localDirectory,fileName)):
            return jsonify({"success":False,"message":f"Error: {fileName} not found in directory {localDirectory}"})
        return send_from_directory(directory=localDirectory,path=fileName,as_attachment=True),200
    except FileNotFoundError:
        return jsonify({"success":False,"message":f"Error: File not found"}),404