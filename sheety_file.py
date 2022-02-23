#Calculating the calories of the exercise and putting it into a spreadsheet
import requests
import datetime as dt
import os

#Set Ups
now_time = dt.datetime.now()
today_date = now_time.strftime("%d/%m/%Y")
today_hour = now_time.strftime("%X")

GENDER = os.environ.get("GENDER")
WEIGHT_KG = os.environ.get("WEIGHT_KG")
HEIGHT_CM = os.environ.get("HEIGHT_CM")
AGE = os.environ.get("AGE")

API_ID = os.environ.get("API_ID")
API_KEY = os.environ.get("API_KEY")


#The Exercis
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

query = input("Tell me which exercise you did:")

params = {
    "query": query,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

headers = {
    "x-app-id": API_ID,
    "x-app-key": API_KEY,
}

response = requests.post(url=exercise_endpoint, json=params, headers=headers).json()

exercise = response["exercises"][0]["name"].title()
duration = response["exercises"][0]["duration_min"]
calories = response["exercises"][0]["nf_calories"]

#Put the results in a google sheet using sheety
sheety_endpoint = os.environ.get("SHEETY_ENDPOINT")

SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")

sheety_params = {
    "workout": {
        "date": today_date,
        "time": today_hour,
        "exercise": exercise,
        "duration": duration,
        "calories": calories
    }
}

sheety_headers = {
    "Authorization": SHEETY_TOKEN
}

sheety_response = requests.post(url=sheety_endpoint, json=sheety_params, headers=sheety_headers)
