# BMI Application (work in progress)

## Overview
This web application allows users to input their height, weight, and name. The app stores this information in a MySQL database and performs several operations to calculate the Body Mass Index (BMI) for each user. Additionally, the app provides visualizations of the users' BMI statistics, including a pie chart representing the distribution of health statuses (underweight, normal, overweight, obese) based on their BMI values.

## Features
- **User Registration**: Users can enter their name, weight, and height.
- **BMI Calculation**: The app calculates BMI based on the input weight and height using the standard formula.
- **Health Status**: After calculating the BMI, the app provides health status messages (e.g., underweight, normal, overweight, obese).
- **MySQL Database**: All user data (name, weight, height, and BMI) is stored in a MySQL database for future use.
- **Statistics Visualization**: The app generates a dynamic pie chart displaying the distribution of users' health statuses and the average BMI.
- **Responsive Design**: The app is built to be user-friendly and works well on different screen sizes.

## Requirements
To run this app locally, you'll need:

- Python 3.6+
- Flask: Web framework to build the app.
- MySQL: For storing user data.
- Plotly: For generating visualizations.
- Pandas & NumPy: For data manipulation and calculation.

## Usage
- Visit the homepage to enter your name, weight, and height.
- Upon submitting the form, the app will calculate your BMI and provide feedback on your health status.
- The app will save your data to the database, and you can view the statistics on the `/statistics` page.
- On the statistics page, a pie chart will visualize the health distribution of all registered users, and the average BMI will be displayed.

## Example
**Enter data:**
- Name: John Doe
- Weight: 70 kg
- Height: 175 cm

**Output:**
- Your BMI: 22.9
- Health Status: Normal

**Statistics:**
- The pie chart shows the distribution of health statuses across all users, and the average BMI is calculated.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Author
Created by Alejandro Cela Camba
