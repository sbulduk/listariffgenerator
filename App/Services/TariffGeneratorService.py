from .ExcelService import ExcelService
from typing import Optional,Dict,List,Union,Tuple
import pandas as pd

class TariffGeneratorService(object):
    def __init__(self,excelService:ExcelService)->None:
        self.excelService=excelService

    def CheckCellContains(self,fileName:str,sheetName:str,cellAddress:str,data:str)->bool:
        cellAddressValue=self.excelService.ReadCell(fileName,sheetName,cellAddress)
        if(str(cellAddressValue)==str(data)):
            return True
        return False

    def GetPLZZonePairs(self,fileName:str,sheetName:str)->Optional[Union[List[Tuple[str,str]],str]]:
        listofPLZZonePairs=[]
        plzAddresses=self.excelService.GetCellAddress(fileName,sheetName,"PLZ")
        if not plzAddresses:
            return f"PLZ value not found in: {fileName}-{sheetName}"
        for plzAddress in plzAddresses:
            plzRow,plzColumn=self.excelService.ExcelReferencetoIndex(plzAddress)
            instantPLZRow,instantPLZColumn=plzRow+1,plzColumn
            instantPLZAddress=self.excelService.IndextoExcelReference(instantPLZRow,instantPLZColumn)
            while self.excelService.CheckInstantCell(fileName,sheetName,instantPLZAddress):
                preProcessedPLZString=self.PreProcessPLZString(self.excelService.ReadCell(fileName,sheetName,instantPLZAddress))
                zoneValue=self.excelService.ReadCell(fileName,sheetName,self.excelService.IndextoExcelReference(instantPLZRow,instantPLZColumn+1))
                keyValuePair=(preProcessedPLZString,zoneValue)
                listofPLZZonePairs.append(keyValuePair)
                instantPLZRow,instantPLZColumn=instantPLZRow+1,instantPLZColumn
                instantPLZAddress=self.excelService.IndextoExcelReference(instantPLZRow,instantPLZColumn)
        return listofPLZZonePairs

    def PreProcessPLZString(self,plzString:str)->List[str]:
        plzString=plzString.replace(" ","").replace(",-","&").replace("+","&").replace(", -","&").replace(",","&").replace("--","&")
        if("-" in plzString and plzString.count("-")==1):
            return plzString
        else:
            plzString=plzString.replace("-","&")
            return plzString

    def ParsePLZValues(self,plzValueString:str)->List[int]:
        plzValueString=self.PreProcessPLZString(plzValueString)
        if "-" in plzValueString:
            startValue,endValue=map(int,plzValueString.split("-"))
            return list(range(startValue,endValue+1))
        elif "&" in plzValueString:
            return list(map(int,plzValueString.split("&")))
        else:
            return [int(plzValueString)]

    def GetSelectedZoneRange(self,fileName:str,sheetName:str,zoneColumnNumber:str)->Optional[Union[List[int],str]]:
        try:
            selectedZoneRange=[]
            zoneRangeHeader=str(f"Zone {zoneColumnNumber}")
            zoneRangeHeaderAddress=self.excelService.GetCellAddress(fileName,sheetName,zoneRangeHeader)
            zoneRangeHeaderRow,zoneRangeHeaderColumn=self.excelService.ExcelReferencetoIndex(zoneRangeHeaderAddress[0])
            currentZoneRangeRow,currentZoneRangeColumn=zoneRangeHeaderRow+1,zoneRangeHeaderColumn
            currentZoneRangeAddress=self.excelService.IndextoExcelReference(currentZoneRangeRow,currentZoneRangeColumn)
            while self.excelService.CheckInstantCell(fileName,sheetName,currentZoneRangeAddress):
                selectedZoneRange.append(str(self.excelService.ReadCell(fileName,sheetName,currentZoneRangeAddress)))
                currentZoneRangeRow,currentZoneRangeColumn=currentZoneRangeRow+1,currentZoneRangeColumn
                currentZoneRangeAddress=self.excelService.IndextoExcelReference(currentZoneRangeRow,currentZoneRangeColumn)
            return selectedZoneRange
        except Exception as e:
            return f"{e}"
        
    def GenerateLeftMenuItems(self,dataFrame:pd.DataFrame)->None:
        leftMenuItemList={
            "A6":"50","A7":"75","A8":"100","A9":"150",
            "A10":"200","A11":"250","A12":"300","A13":"350","A14":"400","A15":"450","A16":"500","A17":"600","A18":"700","A19":"800",
            "A20":"900","A21":"1000","A22":"1250","A23":"1500","A24":"1750","A25":"2000","A26":"2500","A27":"3000","A28":"3500","A29":"4000",
            "A30":"4250","A31":"4500","A32":"5000","A33":"5500","A34":"6000","A35":"6500"
            }
        for cellAddress,cellValue in leftMenuItemList.items():
            row,col=self.excelService.ExcelReferencetoIndex(cellAddress)
            # print(f"{row} - {col}")
            dataFrame.iloc[row,col]=cellValue

    def TargetValueAddress(self,plzValueAddress:str)->str:
        targetZoneValues={
            "0":"B6","1":"C6","2":"D6","3":"E6","4":"F6","5":"G6","6":"H6","7":"I6","8":"J6","9":"K6","10":"L6","11":"M6","12":"N6","13":"O6","14":"P6","15":"Q6","16":"R6","17":"S6","18":"T6","19":"U6",
            "20":"V6","21":"W6","22":"X6","23":"Y6","24":"Z6","25":"AA6","26":"AB6","27":"AC6","28":"AD6","29":"AE6","30":"AF6","31":"AG6","32":"AH6","33":"AI6","34":"AJ6","35":"AK6","36":"AL6","37":"AM6","38":"AN6","39":"AO6",
            "40":"AP6","41":"AQ6","42":"AR6","43":"AS6","44":"AT6","45":"AU6","46":"AV6","47":"AW6","48":"AX6","49":"AY6","50":"AZ6","51":"BA6","52":"BB6","53":"BC6","54":"BD6","55":"BE6","56":"BF6","57":"BG6","58":"BH6","59":"BI6",
            "60":"BJ6","61":"BK6","62":"BL6","63":"BM6","64":"BN6","65":"BO6","66":"BP6","67":"BQ6","68":"BR6","69":"BS6","70":"BT6","71":"BU6","72":"BV6","73":"BW6","74":"BX6","75":"BY6","76":"BZ6","77":"CA6","78":"CB6","79":"CC6",
            "80":"CD6","81":"CE6","82":"CF6","83":"CG6","84":"CH6","85":"CI6","86":"CJ6","87":"CK6","88":"CL6","89":"CM6","90":"CN6","91":"CO6","92":"CP6","93":"CQ6","94":"CR6","95":"CS6","96":"CT6","97":"CU6","98":"CV6","99":"CW6"
            }
        return targetZoneValues.get(plzValueAddress,"Key not found")

    def GenerateTargetFile(self,sourceFileName:str="Source.xlsx",sourceSheetName:str="Sheet1",targetFileName:str="Target.xlsx",targetSheetName:str="Sheet1")->Optional[Union[bool,str]]:
        try:
            plzZonePairList=self.GetPLZZonePairs(sourceFileName,sourceSheetName)
            dataFrame=pd.DataFrame(index=range(128),columns=range(128))
            
            A1Cell=self.excelService.WriteDatatoDataFrame(dataFrame,"A1","Tariff Name: ERVIN_BE_TAT")
            A2Cell=self.excelService.WriteDatatoDataFrame(dataFrame,"A2","Valid From: 01.12.2023 00:00:00")
            A3Cell=self.excelService.WriteDatatoDataFrame(dataFrame,"A3","Valid Till: ")
            B4Cell=self.excelService.WriteDatatoDataFrame(dataFrame,"B4","Entlade-PLZ zweistellig")
            A5Cell=self.excelService.WriteDatatoDataFrame(dataFrame,"A5","(bis)tats. Gewicht")

            self.GenerateLeftMenuItems(dataFrame)

            headerStartCell="B5"
            headerRow,headerColumn=self.excelService.ExcelReferencetoIndex(headerStartCell)
            twoDigitHeaders=[f"{num:02}" for num in range(0,100)]
            for header in twoDigitHeaders:
                dataFrame.iloc[headerRow,headerColumn]=header
                headerColumn+=1

            for plz,zone in plzZonePairList:
                plzValues=self.ParsePLZValues(plz)
                copyAddress=zone
                for plzValue in plzValues:
                    copiedColumnValues=self.GetSelectedZoneRange(sourceFileName,sourceSheetName,copyAddress)
                    targetValueAddress=self.TargetValueAddress(str(plzValue))
                    targetValueRow,targetValueColumn=self.excelService.ExcelReferencetoIndex(targetValueAddress)
                    for value in copiedColumnValues:
                        # if targetValueColumn>=len(dataFrame.columns):
                        #     missingColumns=targetValueColumn-len(dataFrame.columns)+1
                        #     dataFrame=pd.concat([dataFrame,pd.DataFrame(columns=[None]*missingColumns)],axis=1)
                        dataFrame.at[int(targetValueRow),int(targetValueColumn)]="{:.2f}".format(float(value))
                        targetValueRow+=1
            dataFrame=dataFrame.sort_index(axis=1)
            fileGenerationResult=self.excelService.WriteExcel(targetFileName,targetSheetName,dataFrame)
            if fileGenerationResult:
                return True
            else:
                return False
        except Exception as e:
            return f"Error {e}"
        
    def TestWrite(self,fileName:str="Target.xlsx",sheetName:str="Sheet1",row:int=0,col:int=0):
        dataFrame=pd.DataFrame(index=range(row+1),columns=range(col+1))
        if row<0 or col<0:
            raise ValueError("Row and column indices must be positive integers")
        print(f"DataFrame Shape[0]: {dataFrame.shape[0]}")
        print(f"DataFrame Shape[1]: {dataFrame.shape[1]}")
        if row>dataFrame.shape[0] or col>dataFrame.shape[1]:
            raise IndexError("Row or column index is out of bounds.")
        dataFrame.iloc[row,col]="Serdar"
        result=self.excelService.WriteExcel(fileName,sheetName,dataFrame)
        if result:
            return True
        return False