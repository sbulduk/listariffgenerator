from flask import Blueprint,request,jsonify,current_app as app,send_from_directory
from ..Services.ExcelService import ExcelService as es
from ..Services.TariffGeneratorService import TariffGeneratorService as tgs
import os

tariffGeneratorBlueprint=Blueprint("tariffGeneratorBlueprint",__name__,url_prefix="/api/tariff")

UPLOAD_FOLDER = os.path.join(os.getcwd(), "App\Files")
ALLOWED_EXTENSIONS = {"xlsx"}

def AllowedFile(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

@tariffGeneratorBlueprint.route("/upload",methods=["POST"])
def UploadFile():
    print(f"A")
    if "sourceFile" not in request.files:
        return jsonify({"success":False,"message":"No file part"}),400
    else:
        print(f"B")
    file=request.files["sourceFile"]
    print(f"C {file}")
    print(f"------------------------------------------------------------")
    print(f"D {file.filename}")
    if file.filename=="":
        return jsonify({"success":False,"message":"No selected file"}),400

    if file and AllowedFile(file.filename):
        print(f"E")
        filename=file.filename
        print(f"F")
        file.save(os.path.join(UPLOAD_FOLDER,filename))
        print(f"G -: {UPLOAD_FOLDER}")
        return jsonify({"success":True,"fileName":filename}),200
    print(f"H")
    return jsonify({"success":False,"message":"File type not allowed"}),400

@tariffGeneratorBlueprint.route("/generatetargetfile",methods=["POST"])
def GenerateTargetFile():
    sourceFileName=request.json.get("sourceFile")
    sourceSheetName=request.json.get("sourceSheet")
    if sourceSheetName=="":
        sourceSheetName="Sheet1"
    targetFileName=request.json.get("targetFile")
    if not targetFileName.endswith((".xlsx",".xls",".csv")):
        targetFileName+=".xlsx"
    targetSheetName=request.json.get("targetSheet")
    if targetSheetName=="":
        targetSheetName="Sheet1"

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