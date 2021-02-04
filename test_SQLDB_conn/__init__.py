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
        server = "<SECRET>"
        database = "<SECRET>"
        username = "<SECRET>"
        password = "<SECRET>"
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
        credential = "<SECRET>"
        service = BlobServiceClient(account_url="<SECRET>", credential=credential)
        container_names = next(service.list_containers())
        #logging.info(container_names)
        container = service.get_container_client("<SECRET>")
        blob_names = next(container.list_blobs())
        #logging.info(blob_names)
        blob = container.get_blob_client("<SECRET>")
        dl_stream = blob.download_blob()
        #logging.info(dl_stream.content_as_text())
        return func.HttpResponse(dl_stream.content_as_text())
    else:
        return func.HttpResponse("### WRONG ACTION, CHECK API. ###")
    

    
