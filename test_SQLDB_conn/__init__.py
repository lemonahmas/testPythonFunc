import logging
from typing import Container

import azure.functions as func
import pyodbc
from azure.storage.blob import BlobServiceClient
import json
from . import new_module

def main(req:func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    #demo starts here

    new_module.new_func()#shows custom module import

    action = req.params["action"]
    if action == "SQL":
        server = "tcp:dotnet-core-linux.database.windows.net"
        database = "testPythonFuncDB"
        username = "aa"
        password = "root@1234"
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        #logging.info(cursor)
        cursor.execute("select * from testTable")
        row = cursor.fetchone()
        json_array = []
        for i in row:
            json_array.append(i)
        json_result = json.dumps({"data":json_array})
        return func.HttpResponse(json_result)
    elif action == "blob":
        #blob test
        logging.info("blob action")
        credential = "qiCTKFU0ikIRk1yr2tA1w4idrt7hD5S1MatW69yoQhU8GN/V+7kf81c/VVX1ROBFjRIXo2Ap/oZo6O4P2FY58A=="
        service = BlobServiceClient(account_url="https://storageaccountlinux8c6d.blob.core.windows.net", credential=credential)
        container_names = next(service.list_containers())
        #logging.info(container_names)
        container = service.get_container_client("testblobbinding")
        blob_names = next(container.list_blobs())
        #logging.info(blob_names)
        blob = container.get_blob_client("新建文本文档.txt")
        dl_stream = blob.download_blob()
        #logging.info(dl_stream.content_as_text())
        return func.HttpResponse(dl_stream.content_as_text())
    else:
        return func.HttpResponse("### WRONG ACTION, CHECK API. ###")
    

    
