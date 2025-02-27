import flask
import pandas as pd
import numpy as np
import functions 
from flask import render_template


app = flask.Flask("bmi")
   


@app.route("/")
def homepage():
    return functions.get_html("bmi")


@app.route("/result")
def bmi_formula():
    try: #preventing errors
        user_weight = flask.request.args.get("weight_input")
        user_height = flask.request.args.get("height_input")
        user_name = flask.request.args.get("username") #until here we take the values itslef, not yet part of an object
        if len(user_weight) < 1 or len(user_height) < 1 or len(user_name) < 1: #just making sure that the user fills all the fields
            route = functions.get_html("/result")
            route = route.replace("$BMIRESULT$", "Please, introduce correct values")
            route = route.replace("$HEALTHRESULT$","")
            return route
            
        user_bmi = float(user_weight) / ((int(user_height) / 100) * (float(user_height) / 100)) #simply the formula with the values from the user
        if user_bmi > 100 or user_bmi < 10:
            route = functions.get_html("/result")
            route = route.replace("$BMIRESULT$", "Please, introduce correct values")
            route = route.replace("$HEALTHRESULT$","")
            return route
        rounded_bmi = round(user_bmi,2)#rounding to 2 decimals the result

        user_object = functions.User(user_name, rounded_bmi) #creating the object from class user
        object_bmi = float(user_object.bmi)  #enclosing the bmi of the object in a value
        
        user_object.storing_data() #calling the storing_data method to store the data in the db

        #now the conditional logic for the health message:
        health_message = ""
        if int(user_bmi) < 18.5:
            health_message = "You are underweight"
        elif int(user_bmi) > 18.5 and int(user_bmi) < 24.9:
            health_message = "Your weight is normal"
        elif int(user_bmi) > 24.9 and int(user_bmi) < 29.9:
            health_message = "You are in overweight"
        elif int(user_bmi) > 30:
            health_message = "You are obese"
        
        
        route = functions.get_html("/result")
        route = route.replace("$BMIRESULT$", "Your BMI is: " + str(object_bmi)) #displaying the bmi
        route = route.replace("$HEALTHRESULT$",health_message) #displaying the health message
        return route
    except: #if there are wrong or empty values, here is the path:
            route = functions.get_html("/result")
            route = route.replace("$BMIRESULT$", "Please, introduce correct values")
            route = route.replace("$HEALTHRESULT$","")
            return route



@app.route("/statistics")
def statistics_page():  
    users_bmi = functions.get_numbers() #enclosing the users bmi array in a value
    piechart = functions.piechartpx()
    
    try:
        if len(users_bmi) == 0:
            message = "The database is empty"
            route = functions.get_html("statistics")
            route = route.replace("{{ plot_html | safe }}", "")
            route = route.replace("{{ usersdata }}",message)
            return route
        
        users_average = round(np.mean(users_bmi),2) #calling np to get the average

        health_status = "" #initializating empty string and again, conditional logic:

        if users_average < 18.5:
            health_status = "underweight"
        elif users_average > 18.5 and users_average < 24.9:
            health_status = "normal"
        elif users_average > 24.9 and users_average < 29.9:
            health_status = "overweight"
        else:
            health_status = "obese"
        users_data = "The average of the users of this app is " + str(users_average) + " , which is " + health_status 
        route = functions.get_html("statistics")
        route = route.replace("{{ plot_html | safe }}", piechart) 
        route = route.replace("{{ usersdata }}", users_data)
        return route

    except: #if the database is empty, this is the path:
        users_bmi = 0 
        route = functions.get_html("statistics")
        route = route.replace("{{ usersdata }}","There are no users yet in our database")
        return route



