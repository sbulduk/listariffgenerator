from flask import Blueprint,request,jsonify,current_app as app
from ..Services.ExcelService import ExcelService as es
from ..Services.TariffGeneratorService import TariffGeneratorService as tgs

tariffGeneratorBlueprint=Blueprint("tariffGeneratorBlueprint",__name__,url_prefix="/api/tariff")

# TODO: Will be removed!
@tariffGeneratorBlueprint.route("/getcelladdress",methods=["POST"])
def GetCellAddress():
    fileName=request.json.get("fileName")
    sheetName=request.json.get("sheetName")
    searchString=request.json.get("searchString")

    excelService=es(app.root_path)
    tariffGeneratorService=tgs(excelService)
    try:
        resultCellAddress=tariffGeneratorService.GetCellAddress(fileName,sheetName,searchString)
        return jsonify({"success":True,"message":f"{resultCellAddress}"}),200
    except Exception as e:
        return jsonify({"success":False,"message":f"Error: {e}"}),400
    
@tariffGeneratorBlueprint.route("/getplzzonepairs",methods=["POST"])
def GetPLZZonePairs():
    fileName=request.json.get("fileName")
    sheetName=request.json.get("sheetName")

    excelService=es(app.root_path)
    tariffGeneratorService=tgs(excelService)
    try:
        return jsonify({"success":True,"message":f"{tariffGeneratorService.GetPLZZonePairs(fileName,sheetName)}"}),200
    except Exception as e:
        return jsonify({"success":False,"message":f"Error: {e}"}),400
    
@tariffGeneratorBlueprint.route("/getselectedzonerange",methods=["POST"])
def GetSelectedZoneRange():
    fileName=request.json.get("fileName")
    sheetName=request.json.get("sheetName")
    zoneColumnNumber=request.json.get("zoneColumnNumber")

    excelService=es(app.root_path)
    tariffGeneratorService=tgs(excelService)
    try:
        return jsonify({"success":True,"message":f"{tariffGeneratorService.GetSelectedZoneRange(fileName,sheetName,zoneColumnNumber)}"}),200
    except Exception as e:
        return jsonify({"success":False,"message":f"Error: {e}"}),400
    
@tariffGeneratorBlueprint.route("/generatetargetfile",methods=["POST"])
def GenerateTargetFile():
    sourceFileName=request.json.get("sourceFileName")
    sourceSheetName=request.json.get("sourceSheetName")
    targetFileName=request.json.get("targetFileName")
    targetSheetName=request.json.get("targetSheetName")

    excelService=es(app.root_path)
    tariffGeneratorService=tgs(excelService)
    try:
        return jsonify({"success":True,"message":f"{tariffGeneratorService.GenerateTargetFile(sourceFileName,sourceSheetName,targetFileName,targetSheetName)}"})
    except Exception as e:
        return jsonify({"success":False,"message":f"Error: {e}"})

# TODO: Will be removed!
@tariffGeneratorBlueprint.route("/getaddresswrtindices",methods=["GET"])
def GetAddressWrtIndices():
    excelService=es(app.root_path)
    row=int(request.args.get("row"))
    col=int(request.args.get("col"))
    return excelService.IndextoExcelReference(row,col)

# TODO: Will be removed!
@tariffGeneratorBlueprint.route("/getindiceswrtaddress",methods=["GET"])
def GetIndicesWrtAddress():
    excelService=es(app.root_path)
    addressValue=str(request.args.get("addressValue"))
    row,col=excelService.ExcelReferencetoIndex(addressValue)
    return f"{row} - {col}"

# TODO: Will be removed!
@tariffGeneratorBlueprint.route("/parseplzvalues",methods=["POST"])
def ParsePLZValues():
    excelService=es(app.root_path)
    tariffGeneratorService=tgs(excelService)
    testString=request.json.get("testString")
    return tariffGeneratorService.ParsePLZValues(testString)