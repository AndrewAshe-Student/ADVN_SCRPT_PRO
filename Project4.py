#!/usr/bin/env python
# coding: utf-8

# Imports.
import requests
import sys
import json
import pandas as pd
import pytest
import webbrowser as wb
from pytest import ExitCode
import time

# API.
# https://carapi.app/api#/Models/makemodels%3Aindex%3Aget
auth = "https://car-api2.p.rapidapi.com/api/"
makes = "https://car-api2.p.rapidapi.com/api/makes"
years = "https://car-api2.p.rapidapi.com/api/years"
models = "https://car-api2.p.rapidapi.com/api/models"
engines = "https://car-api2.p.rapidapi.com/api/engines"
colours = "https://car-api2.p.rapidapi.com/api/exterior-colors"
carAttributes = "https://car-api2.p.rapidapi.com/api/vehicle-attributes"

df = pd.DataFrame()

# Header paramaters for api-tokens.
headers = {
    "X-RapidAPI-Key": "a128349cd3msha07615f87e1be36p146ca1jsn2b1dce4fe9d3",
    "X-RapidAPI-Host": "car-api2.p.rapidapi.com",
    "api-token": "c5ce0fd6-f034-4845-9f2b-040c78cb8671",
    "api-secret": "cb7358847d500853619ac096e80f735d"
}

# Function to test the API endpoint,
# as to determine if the data is readable or not.
def testApiEndpoint(url):
    response = requests.request("GET", makes, headers=headers)
    if response.status_code == 200:
        return 1
    elif response.status_code == 401:
            print("Unauthorized Request.")
            return 2
    elif response.status_code == 11001:
            print("Network Connection Error.")
            return 2
    else:
        return 2

# Function to return {Manufacturers} that released cars
# in the inputted {year}.
def getMakesByYear():
    year = input("Please enter the year of the car you wish to find: ") or "2020"
    params = {"year": year}
    response = requests.request("GET", makes, headers=headers, params=params)
    #Response 200, successful query
    car_data = response.json()
    car_data = car_data["data"]
    print(f"Here is a list of manufacturers that released cars in the year: {year}")
    for item in car_data:
        print(item["name"])
    return year

# Function that takes the inputted {year} and
# returns {Models} by selected {Manufacturer} in {year}.
def getCarModelsByMake(year):
    make = input("Please enter the make you wish to find: ") or "Volvo"
    print(f"You selected: {make}")
    params = {
        "year": year,
        "make": make
    }
    response = requests.request("GET", models, headers=headers, params=params)
    #Response 200, successful query
    car_data = response.json()
    data = car_data["data"]
    try:
        for item in data:
            print(f"{make}, Model: " + item["name"])
    except TypeError:
        pass
    return make

# Function to select the {Model} of {Manufacturer} in {year}.
def getModel(year, make):
    model_select = input("Please select a model from the list for more details: ") or "XC90"
    print(f"You selected the: {year}, {make}, {model_select}")
    model = model_select
    return model

# Function to return statistics by {Model} of {Manufacturer} in {year}.
def getEnginesByModel(year, make, model):
    params = {
        "year": year,
        "verbose": "yes",
        "make": make,
        "model": model
    }
    count = 0
    notGasPower = []
    allEngines = []
    response = requests.request("GET", engines, headers=headers, params=params)
    car_data = response.json()
    for item in car_data["data"]:
        count += 1
        data = (item["engine_type"], item["fuel_type"], item["size"], item["cylinders"],
                item["horsepower_hp"], item["horsepower_rpm"], item["torque_ft_lbs"], item["torque_rpm"],
                item["valves"], item["valve_timing"],item["cam_type"], item["drive_type"], item["transmission"])
        if data[0] != "gas":
            notGasPower.append(data)
            allEngines.append(data)
        else:
            allEngines.append(data)
    try:
        return(allEngines)
    except TypeError:
        pass

# Function to select the Engine of {Model} by {Manufacturer} in {year}.
def engineSelect(engineList):
    for idx, engine in enumerate(engineList, start=1):
        print(idx, engine)
    engine_select = int(input("Please select an engine from the list for more details: ")) or int(1)
    print(f"You selected engine: {engine_select}")
    return engineList[engine_select - 1]

# Function to select the Engine of {Model} by {Manufacturer} in {year}.
# Ask the user if that is the correct choice.
def engineSelect2(engineList):
    for idx, engine in enumerate(engineList, start=1):
        print(idx, engine)
    while True:
        engine_select = int(input("Please select an engine from the list for more details: ")) or int(1)
        print(f"You selected engine: {engine_select}")
        decision = input("Is this your selection? ").upper
        if decision == "N":
            pass
        elif decision == "Y":
            return engineList[engine_select - 1]
        
# Function to select the Engine of {Model} by {Manufacturer} in {year}.
# Ask the user if that is the correct choice.
def engineSelect3(engineList):
    # for idx, engine in enumerate(engineList, start=1):
    #     print(idx, engine)
    engine_select = int(input("Please select an engine from the list: ") or 1)
    decision = input(f"You selected engine: {engine_select} \n Is this your selection? [Y/N]: ").upper() or "Y"
    if decision == "Y":
        return engine_select
    else:
        return engineSelect3(engineList)

def getTransmissionByModel(year, make, model):
    params = {
        "year": year,
        "verbose": "yes",
        "make": make,
        "model": model
    }
    count = 0
    response = requests.request("GET", engines, headers=headers, params=params)
    car_data = response.json()
    # print(car_data)
    # 'https://carapi.app/api/interior-colors?year=2008&make=audi&model=a4'
    # 'https://carapi.app/api/vehicle-attributes?attribute=engines.transmission'

# Generate pandas data frame
def generateDataFrame(year, make, model):
    params = {
        "year": year,
        "verbose": "yes",
        "make": make,
        "model": model
    }
    count = 0
    rows = pd.DataFrame()
    response = requests.request("GET", engines, headers=headers, params=params)
    car_data = response.json()
    for item in car_data["data"]:
        count += 1
        metrics = (item["engine_type"], item["fuel_type"], item["size"], item["cylinders"],
                item["horsepower_hp"], item["horsepower_rpm"], item["torque_ft_lbs"], item["torque_rpm"],
                item["valves"], item["valve_timing"], item["cam_type"], item["drive_type"], item["transmission"])
        
        (
        pdEngine, pdFuel, pdSize, pdCylinders, pdHp, pdHpRpm,
        pdTorque, pdTorqueRpm, pdValves, pdValveTiming,
        pdCamType, pdDriveType, pdTransmission
        ) = metrics
    
        row = {'count': count, 'engine_type': pdEngine, 'fuel_type': pdFuel, 'size': pdSize,
            'cylinders': pdCylinders, 'horsepower_hp': pdHp, 'horsepower_rpm': pdHpRpm,
                'torque_ft_lbs': pdTorque, 'torque_rpm':pdTorqueRpm, 'valves':pdValves, 'valve_timing': pdValveTiming,
                'cam_type': pdCamType , 'drive_type': pdDriveType, 'transmission_type': pdTransmission}
        rows = rows._append(row, ignore_index=True)
    return rows 

# Function to generate the url of the search.
def generateURL(year, make, model):
    url = ("https://google.com/search?q=" + year + " " + make + " " + model + " " + "&tbm=isch")
    return url

# Prompt the user for continuation.
def prompt(url):
    while True:
        answer = input("Is this the car you were looking for? [Y/N]: ").upper() or "N"
        if answer == "Y":
            wb.open_new(url)
            answerConfOne = input("Would you like to search again? [Y/N]: ").upper() or "N"
            if answerConfOne == "Y":
                break
            elif answerConfOne == "N":
                sys.exit()
        elif answer == "N":
            answerConfTwo = input("Would you like to search again? [Y/N]: ").upper() or "N"
            if answerConfTwo == "Y":
                break
            elif answerConfTwo == "N":
                print("Thank you for using this application!" + "\n" + "Now closing.")
                time.sleep(3)
                sys.exit()

if __name__ == "__main__":
    while True:
        toggle = testApiEndpoint(auth)
        if toggle == 1:
            year = getMakesByYear()
            make = getCarModelsByMake(year)
            model = getModel(year, make)
            engineList = getEnginesByModel(year, make, model)
            # getTransmissionByModel(year, make, model)
            # exteriorColour = getExteriorColoursByModel(year, make, model)
            
            rows = generateDataFrame(year, make, model)
            df = df._append(rows, ignore_index=True)
            print(df.to_string())
            
            engineSelected = engineSelect3(engineList)
            print(f"{year, make, model, engineSelected}")

            url = generateURL(year, make, model)
            prompt(url)
        else:
            print("Thank you for using this application!" + "\n" + "Now closing.")
            time.sleep(3)
            sys.exit()

        # engineData = getEngineByModel(year, make, model)
        # engine = int(engineSelect())
        # print(make, model, engine) 

        # def getExteriorColoursByModel(year, make, model):
        #     colour = ()
        #     params = {
        #         "year": year,
        #         "make": make,
        #         "model": model
        #     }
        #     response = requests.request("GET", colours, headers=headers, params=params)
        #     #Response 200, successful query
        #     car_data = response.json()
        #     data = car_data["data"]
        #     try:
        #         for item in data:
        #             print(f"{year}, {make}, {model}: " + item["name"])
        #     except TypeError:
        #         pass
        #     return colour

        # def engineSelect():
        #     engine_select = input("Please select an engine from the list for more details: ") or "2"
        #     print(f"You selected: {engine_select}")
        #     engine = engine_select
        #     return engine

        # def searchOptions(year):
        #     search = {}
        #     for i in range(1):
        #         make1 = input("Make: ") or "BMW"
        #         model1 = input("Model: ") or "M4"
        #         engine1 = input("Engine: ") or "5.0"
        #         search = {year, make1, model1, engine1}
        #     return search

        #    def getEngineByCar(model, search):
        #     params = {
        #         "year": "2020",
        #         "verbose": "yes",
        #         "make": "Audi",
        #         "model": model
        #     }
        #     response = requests.request("GET", engines, headers=headers, params=params)
        #     car_data = response.json()
        #     print(model)
        #     print("| Engine type | Engine Size | Horsepower |")

        # def getEnginesByModel(year, make, model):
        #     params = {
        #         "year": year,
        #         "verbose": "yes",
        #         "make": make,
        #         "model": model
        #     }
        #     count = 0
        #     response = requests.request("GET", engines, headers=headers, params=params)
        #     car_data = response.json()
        #     for item in car_data["data"]:
        #         count += 1
        #         data = [count, item["engine_type"], item["size"], item["horsepower_hp"], item["drive_type"]]
        #         print(data)
        #     return(data)

        # Test call to confirm Api is responsive.
        # def testApiCall():
        #     params = {}
        #     response = requests.request("GET", auth, headers=headers, params=params)
        #     data = response.json()
        #     data = data["data"]
        #     print(data)

# PyTest definitions and parameters
# 81 attempts later.
@pytest.fixture
def a2():
    return 1

@pytest.fixture
def b2():
    return 2

def testForPytest(a2, b2):
    c = (a2 + b2)
    assert c == a2 + b2