import requests
import json
import os.path
import csv as reader
import time
import streamlit as st
from bs4 import BeautifulSoup

from email_sender import send_email_with_attachment

header = ["VesselName", "time", "LAT", "LON"]
def getHtmlFromUrl(url):
    request = requests.get(url).text
    return request

def getJsonFromHtml(htmlText):
    return json.loads(htmlText)

def getVesselsArrayFromHtml():
    url = "https://control.effettoventuri.eu/bz/marks?coursecode=Chris"
    htmlText = getHtmlFromUrl(url)
    if htmlText is not None:
        jsonFromHtml = getJsonFromHtml(htmlText)
        return jsonFromHtml["features"]

def writeInformationToFiles(names, stop_event):
    counter = 0
    while not stop_event.is_set():
        features = getVesselsArrayFromHtml()
        # get elements that match the ids list in the json
        for obj in features:
            geometry = obj["geometry"]
            properties = obj["properties"]
            objName = properties["name"]
            t = str(properties["time"])

            coords = geometry["coordinates"]
            LAT = str(coords[0])
            LON = str(coords[1])
            if objName in names:
                row = [objName, t, LAT, LON]
                print(row)
                writeToFile(objName, row)
        counter += 5
        time.sleep(5)
        if(counter % 1800 == 0):
            counter = 0
            attachmentPaths = [f"{id}.csv" for id in names]
            send_email_with_attachment("vesseltracker1@gmail.com", str(names), "vessel tracking", attachmentPaths)

def writeToFile(id, row):
    path = f"{id}.csv"
    with open(path, "a") as file:
        path_existed = os.path.exists(path)
        csv_reader = reader.writer(file)
        if not path_existed:
            csv_reader.writerow(header)
        csv_reader.writerow(row)