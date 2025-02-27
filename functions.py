
import mysql.connector
import plotly.express as px
import numpy as np
import plotly.io as pio
from flask import render_template

#Here I am setting the values for accesing the database
db_config = {
    "host" : "localhost",
    "user" : "root",
    "password" : "root",
    "database" : "database_bmi"}

def get_html(file_name): #just declaring the get_html function
    html = open("templates/" + file_name + ".html")
    content = html.read()
    html.close()
    return content 


#Declaring all functions and classes. First the one that get the numbers from the database:

def get_numbers():
    try:
        database = mysql.connector.connect(**db_config)
        cursor = database.cursor()
        
        cursor.execute("SELECT bmi FROM users")
        results = cursor.fetchall() 
        
        database.close()  # Closes the connection after fetching the data
        
        if results:
            return [round(float(row[0]), 2) for row in results]
            
        else:
            return []
    except mysql.connector.Error as err:
        print(f"Error in get_numbers: {err}")
        return []


arraz = get_numbers()#just controlling
print("arraz:")
print(arraz)
print("average:")
print(np.mean(arraz))


#this is the piechart function:

def piechartpx():
    users_bmi = get_numbers()
    total = len(users_bmi)
    if total == 0:
        return "No data available for the chart."
    count_underweight = sum(1 for bmi in users_bmi if bmi < 18.5)
    count_normal = sum(1 for bmi in users_bmi if 18.5 <= bmi < 24.9)
    count_overweight = sum(1 for bmi in users_bmi if 25 <= bmi < 29.9 )
    count_obese = sum(1 for bmi in users_bmi if bmi >= 30)
   
    sizes = [count_underweight / total, count_normal / total, count_overweight / total, count_obese / total]
    labels = ["underweight","normal","overweight","obese "]
    fig = px.pie(values=sizes, names=labels, 
                 title="Users' health by bmi", 
                 color_discrete_map={"Underweight": "#92C5F9", "Normal":"#AFDC8F","Overweight":"#B6A6E9","Obese":"#21134D"},
                 hole = 0.7,
                 )
    fig.update_traces(textposition="outside", textinfo="percent+label")
    #trying to export to html:
    #plot_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
    return pio.to_html(fig, full_html=True, include_plotlyjs='cdn') #BOTH WORKING





#this is the user class
class User: 
    def __init__(self,name,bmi):
        self.name = name
        self.bmi = bmi
    
    def storing_data(self): #it has a storing method, that stores the user name and the bmi in the database
        try:
            database = mysql.connector.connect(**db_config)
            cursor = database.cursor()
            
            sql = "INSERT INTO users (username, bmi) VALUES (%s, %s)"
            values = (self.name, self.bmi)
            cursor.execute(sql, values)
            database.commit()

            database.close()  # Closes the connection after storing the data
            print("Data inserted successfully")
        except mysql.connector.Error as err:
            print(f"Error inserting data: {err}") 


