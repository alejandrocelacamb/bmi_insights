const username = localStorage.getItem("username");
const weight = localStorage.getItem("Weight");
const height = localStorage.getItem("Height");
const bmi = localStorage.getItem("userBmi");

function greet() {

    //const parsedBmi = parseFloat(bmi);
    const parsedHeight = parseFloat(height);
    const parsedWeight = parseFloat(weight);
    let message = "";
    if (isNaN(parsedWeight) || isNaN(parsedHeight)) {
        message = "Please, introduce correct values"; //just greeting the user if the values are  realistic and properly filled 
    } else  {
        message = "Thank you, " + username + ", your data was successfully stored in our database!";
    }
    return alert(message);
}

document.addEventListener("DOMContentLoaded", greet);