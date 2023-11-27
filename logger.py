import threading
import datetime
import csv
import os
import requests
import time
from flask import Flask, jsonify

debug = True

urlCurr = "http://dataservice.accuweather.com/currentconditions/v1/274087/historical/24?apikey= ZuWR33RUX4BQXt6awK8jOoucnaqLwZ10 &details=True"
class Logger(object):

    def __init__(self, port='/dev/ttyACM0', filename='data.csv'):
        self.filename = filename
        self.clb = None
        self.thr = threading.Thread(target=self.read_data_Curr)
        self.thr.daemon = True
        self.thr.start()
    
    def read_data_Curr(self):
        if debug:
            responseCurr = requests.get(urlCurr)
            api_responseCurr = responseCurr.json()

            info ={
                "Humidity": api_responseCurr[0]["RelativeHumidity"],
                "Temperature": api_responseCurr[0]["RealFeelTemperature"]["Metric"]["Value"],
                "TemperatureUnit": api_responseCurr[0]["RealFeelTemperature"]["Metric"]["Unit"],
                "Pressure": api_responseCurr[0]["Pressure"]["Metric"]["Value"],
                "PressureUnit": api_responseCurr[0]["Pressure"]["Metric"]["Unit"],
                "InstDirection": api_responseCurr[0]["Wind"]["Direction"]["Degrees"],
                "InstSpeed": api_responseCurr[0]["Wind"]["Speed"]["Metric"]["Value"],
                "InstSpeedUnit": api_responseCurr[0]["Wind"]["Speed"]["Metric"]["Unit"],
                "LastHour": api_responseCurr[0]["PrecipitationSummary"]["PastHour"]["Metric"]["Value"],
                "Last24Hours": api_responseCurr[0]["PrecipitationSummary"]["Past24Hours"]["Metric"]["Value"]    
            }
        else:
            info = {}
        return info


    def store_data(self, data):
        file_exists = os.path.isfile(self.filename)
        with open(self.filename, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

    def on_data_updated(self, clb):
        self.clb = clb
