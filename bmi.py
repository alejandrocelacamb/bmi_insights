
import flask
import pandas as pd
import numpy as np
import functions 
from flask import render_template

app = flask.Flask("bmi")
   
# Constants for BMI ranges
BMI_RANGES = {
    (0, 18.5): "You are underweight",
    (18.5, 24.9): "Your weight is normal",
    (24.9, 29.9): "You are in overweight",
    (30, float('inf')): "You are obese"
}

def get_health_message(bmi):#no entiendo la logica del loop y no entiendo cuando has definido message
    """Helper function to determine health message based on BMI"""
    for (lower, upper), message in BMI_RANGES.items():
        if lower <= bmi < upper:
            return message
    return "Please, introduce correct values"

@app.route("/")
def homepage():
    return functions.get_html("bmi")

@app.route("/result")
def bmi_formula():
    try:
        user_weight = flask.request.args.get("weight_input", "")
        user_height = flask.request.args.get("height_input", "")
        user_name = flask.request.args.get("username", "")

        # Input validation
        if not all([user_weight, user_height, user_name]): 
            raise ValueError("Missing required fields")

        # Convert and validate numeric inputs
        weight = float(user_weight)
        height = float(user_height)
        
        # Calculate BMI
        height_meters = height / 100
        user_bmi = weight / (height_meters * height_meters)

        # Validate BMI range
        if not 10 <= user_bmi <= 100:
            raise ValueError("BMI out of realistic range")

        rounded_bmi = round(user_bmi, 2)
        
        # Create and store user data
        user_object = functions.User(user_name, rounded_bmi)
        user_object.storing_data()

        # Get health message
        health_message = get_health_message(user_bmi)
        
        # Prepare response
        route = functions.get_html("/result")
        route = route.replace("$BMIRESULT$", f"Your BMI is: {rounded_bmi}")
        route = route.replace("$HEALTHRESULT$", health_message)
        return route

    except (ValueError, TypeError) as e: #por que especificar tipo de error?
        route = functions.get_html("/result")
        route = route.replace("$BMIRESULT$", "Please, introduce correct values")
        route = route.replace("$HEALTHRESULT$", "")
        return route

@app.route("/statistics")
def statistics_page():  
    try:
        users_bmi = functions.get_numbers()
        piechart = functions.piechartpx()
        
        if not users_bmi:
            route = functions.get_html("statistics")
            route = route.replace("{{ plot_html | safe }}", "")
            route = route.replace("{{ usersdata }}", "The database is empty")
            return route
        
        users_average = round(np.mean(users_bmi), 2)
        health_status = get_health_message(users_average).lower().split()[-1]
        
        users_data = f"The average of the users of this app is {users_average}, which is {health_status}"
        
        route = functions.get_html("statistics")
        route = route.replace("{{ plot_html | safe }}", piechart)
        route = route.replace("{{ usersdata }}", users_data)
        return route

    except Exception:
        route = functions.get_html("statistics")
        route = route.replace("{{ usersdata }}", "There are no users yet in our database")
        return route



