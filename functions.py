
import mysql.connector
import plotly.express as px
import numpy as np
import plotly.io as pio
from flask import render_template
from typing import List, Optional
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv() 

# Database configuration
db_config = {
    "host": os.getenv('DB_HOST', 'localhost'),
    "user": os.getenv('DB_USER', 'root'),
    "password": os.getenv('DB_PASSWORD', 'root'),
    "database": os.getenv('DB_DATABASE', 'database_bmi')
}

# BMI range constants
BMI_RANGES = { 
    "underweight": (0, 18.5),
    "normal": (18.5, 24.9),
    "overweight": (24.9, 29.9),
    "obese": (30, float('inf'))
}

# Color mapping for the pie chart
COLOR_MAP = {
    "underweight": "#92C5F9",
    "normal": "#AFDC8F",
    "overweight": "#B6A6E9",
    "obese": "#21134D"
}

@contextmanager 
def get_db_connection():
    """Context manager for database connections"""
    conn = mysql.connector.connect(**db_config)
    try:
        yield conn 
    finally:
        conn.close()

def get_html(file_name: str) -> str: 
    """Read and return HTML template content"""
    with open(f"templates/{file_name}.html") as html: 
        return html.read()

def get_numbers() -> List[float]: 
    """Retrieve BMI numbers from database"""
    try:
        with get_db_connection() as database:
            cursor = database.cursor()
            cursor.execute("SELECT bmi FROM users")
            results = cursor.fetchall()
            
            return [round(float(row[0]), 2) for row in results] if results else [] 
            
    except mysql.connector.Error as err:
        print(f"Error in get_numbers: {err}")
        return []

def piechartpx() -> str:
    """Generate pie chart of BMI distribution""" 
    users_bmi = get_numbers()
    total = len(users_bmi)
    
    if total == 0:
        return "No data available for the chart."
        
    # Calculate counts for each BMI category
    counts = { 
        category: sum(1 for bmi in users_bmi 
                     if BMI_RANGES["underweight"][0] <= bmi < BMI_RANGES[category][1])
                
        for category in BMI_RANGES
    }
    
    

    
    # Calculate percentages
    sizes = [count / total for count in counts.values()]
    labels = list(counts.keys())
    
    # Create pie chart
    fig = px.pie(
        values=sizes,
        names=labels,
        title="Users' health by BMI",
        color_discrete_map=COLOR_MAP,
        hole=0.7
    )
    
    fig.update_traces(textposition="outside", textinfo="percent+label")
    return pio.to_html(fig, full_html=True, include_plotlyjs='cdn')

class User:
    """Class representing a user with BMI information"""
    
    def __init__(self, name: str, bmi: float):
        self.name = name
        self.bmi = bmi
    
    def storing_data(self) -> bool: 
        """Store user data in database"""
        try:
            with get_db_connection() as database:
                cursor = database.cursor()
                sql = "INSERT INTO users (username, bmi) VALUES (%s, %s)"
                cursor.execute(sql, (self.name, self.bmi))
                database.commit()
                return True
                
        except mysql.connector.Error as err:
            print(f"Error inserting data: {err}")
            return False


