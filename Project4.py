#!/usr/bin/env python
# coding: utf-8

import requests
import json
import pandas as pd

# API
# https://carapi.app/api#/Models/makemodels%3Aindex%3Aget
url = "https://www.carqueryapi.com/api/0.3/"
makes = "https://car-api2.p.rapidapi.com/api/makes"
years = "https://car-api2.p.rapidapi.com/api/years"
models = "https://car-api2.p.rapidapi.com/api/models"
engines = "https://car-api2.p.rapidapi.com/api/engines"

headers = {
    "X-RapidAPI-Key": "a128349cd3msha07615f87e1be36p146ca1jsn2b1dce4fe9d3",
    "X-RapidAPI-Host": "car-api2.p.rapidapi.com"
}

def getMakesByYear():
    year = input("Please enter the year of the car you wish to find: ") or "2020"
    params = {
        "year": year
    }
    
    response = requests.request("GET", makes, headers=headers, params=params)
    #Response 200, successful query
    car_data = response.json()
    car_data = car_data["data"]
    
    print(f"Here is a list of manufacturers that released cars in the year: {year}")
    
    for manufacturer in car_data:
        print(manufacturer["name"])
    return year

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

def getEngineByModel(year, make, model):
    params = {
        "year": year,
        "verbose": "yes",
        "make": make,
        "model": model
    }
    count = 0
    gasPower = []
    response = requests.request("GET", engines, headers=headers, params=params)
    car_data = response.json()
    for item in car_data["data"]:
        count += 1
        data = [count, item["engine_type"], item["size"], item["horsepower_hp"], item["drive_type"]]
        if data[1] == "gas":
            gasPower.append(data)
        else:
            print(data)
    for item in gasPower:
        print(item)

def modelSelect():
    model_select = input("Please select a model from the list for more details: ") or "XC90"
    print(f"You selected: {model_select}")
    model = model_select
    return model

def engineSelect():
    engine_select = input("Please select an engine from the list for more details: ") or "2"
    print(f"You selected: {engine_select}")
    engine = engine_select
    return engine

def searchOptions(year):
    search = {}
    for i in range(1):
        make1 = input("Make: ") or "BMW"
        model1 = input("Model: ") or "M4"
        engine1 = input("Engine: ") or "5.0"
        search = (year, make1, model1, engine1)
    return search

def getEngineByCar(model, search):
    params = {
        "year": "2020",
        "verbose": "yes",
        "make": "Audi",
        "model": model
    }
    response = requests.request("GET", engines, headers=headers, params=params)
    car_data = response.json()
    print(model)
    print("| Engine type | Engine Size | Horsepower |")

def getEngineByModel(year, make, model):
    params = {
        "year": year,
        "verbose": "yes",
        "make": make,
        "model": model
    }
    count = 0
    response = requests.request("GET", engines, headers=headers, params=params)
    car_data = response.json()
    for item in car_data["data"]:
        count += 1
        data = [count, item["engine_type"], item["size"], item["horsepower_hp"], item["drive_type"]]
        print(data)

def engineSelect():
    engine_select = input("Please select an engine from the list for more details: ") or "2"
    print(f"You selected: {engine_select}")
    engineList = getEngineByModel("2020", "Volvo", "XC90")
    for engine in engineList():
        print(engine)
    return engine

if __name__ == "__main__":
    year = getMakesByYear()
    make = getCarModelsByMake(year)
    model = modelSelect()
    # engineData = getEngineByModel(year, make, model)
    # engine = int(engineSelect())
    # print(make, model, engine)