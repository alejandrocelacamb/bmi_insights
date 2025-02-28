
//creating the user info class (with the store methods to save data in localstorage):
class userInfo {
    constructor(userName, bmi, weight, height) {
        this.userName = userName;
        this.bmi = bmi;
        this.weight = weight;
        this.height = height;
    }

    storeUsername() {
        return localStorage.setItem("username", this.userName);
    }
    storeBmi() {
        return localStorage.setItem("userBmi", this.bmi)
    }
    storeWeight(){
        return localStorage.setItem("Weight", this.weight)
    }
    storeHeight(){
        return localStorage.setItem("Height", this.height)
    }
}

//At this point we create the functions. 

// First the bmi formula:

function bmiFormula(a, b) {
    return parseFloat(a) / ((parseFloat(b) / 100) * (parseFloat(b) / 100))
}

//now the function that gets the info from the user by the moment he submits:
function onSubmit() {
    
        //document.getelementbyId consts:
        const weight = document.getElementById("weight_input");
        const height = document.getElementById("height_input");
        const nameInput = document.getElementById("username");

        //value consts:
        const userWeight = weight.value;
        const userHeight = height.value;
        const userName = nameInput.value;
        const userBmi = bmiFormula(userWeight, userHeight);//we enclose the bmi formula funtion to pass it as a parameter of the object method .store



        const user = new userInfo(userName, userBmi, userWeight, userHeight); //creating the object


        user.storeUsername();
        user.storeBmi();
        user.storeWeight();
        user.storeHeight();//calling the object's methods to store the data
    
}


//now we create an event listener with the submit button and assign the onSubmit function to it:
const submit = document.getElementById("submit_bmi");


document.addEventListener("DOMContentLoaded", onSubmit) 
submit.addEventListener("click", onSubmit);