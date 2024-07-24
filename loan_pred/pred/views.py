from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder


from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import pandas as pd
import numpy as np
# Create your views here.


def home(request):
     return render(request,"home.html")


def login(request):
    if request.method=="POST":
        u=request.POST['uname']
        p=request.POST['psw']
        user=auth.authenticate(username=u,password=p)
        if user is not None:
            auth.login(request,user)
            return render(request,"pred.html")
        else:
            return render(request,"login.html")
    return render(request,"login.html")


# def login(request):
#     return render(request,'login.html')



def register(request):
    return  render(request,'register.html')

def saveuser(request):
    username=request.POST['uname']
    password = request.POST['psw']
    # name = request.POST['name']
    # email = request.POST['email']
    # phone = request.POST['phone']
    # address = request.POST['address']

    newusers=User(username=username,password=password)
    newusers.save()
    return render(request, 'login.html')
def verifyuser(request):
    username = request.POST.get('uname')
    password = request.POST.get('psw')

    user= User.objects.filter(username=username)

    for u in user:
        if u.password==password:
            return render(request,'pred.html')
        else:
            return render(request,'login.html')
        

def pred(request):
    return  render(request,'pred.html')


def result(request):
    Loan_ID = request.POST["Loan_ID"]
    gender = request.POST["Enter Gender"]
    married = request.POST["Married"]
    dependents = request.POST["Dependents"]
    education = request.POST["Education"]
    self_employed = request.POST["Self_Employed"]
    applicant_income = request.POST["Applicant_Income"]
    coapplicant_income =request.POST["Coapplicant_Income"]
    loan_amount = request.POST["Loan Amount"]
    loan_amount_term =request.POST["Loan_Amount_Term"]
    credit_history =request.POST["Credit_History"]
    property_area = request.POST["Property_Area"]

    
    
    data = pd.read_csv('train.csv')
    data['Dependents'] = data['Dependents'].replace('3+', '3')  # Replace '3+' with '3'
    data['Dependents'] = pd.to_numeric(data['Dependents'])     # Convert to numeric
    data = data.dropna()                                       # Drop rows with missing values

    label_encoders = {}
    categorical_cols = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area']
    for col in categorical_cols:
        label_encoders[col] = LabelEncoder()
        data[col] = label_encoders[col].fit_transform(data[col])
    X = data.drop(['Loan_ID', 'Loan_Status'], axis=1)
    y = data['Loan_Status']

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X, y)
    # try:
    #     loan_id = input("Enter Loan_ID: ")
    #     gender = input("Enter Gender (Male/Female): ")
    #     married = input("Married? (Yes/No): ")
    #     dependents = int(input("Number of Dependents: "))
    #     education = input("Education (Graduate/Not Graduate): ")
    #     self_employed = input("Self Employed? (Yes/No): ")
    #     applicant_income = float(input("Applicant Income: "))
    #     coapplicant_income = float(input("Coapplicant Income: "))
    #     loan_amount = float(input("Loan Amount: "))
    #     loan_amount_term = float(input("Loan Amount Term (in months): "))
    #     credit_history = float(input("Credit History (1 for Yes, 0 for No): "))
    #     property_area = input("Property Area (Urban/Semiurban/Rural): ")
    # except ValueError:
    #         print("Invalid input. Please enter valid numeric values for income, loan amount, and credit history.")
    # except KeyError:
    #      print("Invalid input. Please enter valid values for gender, married, education, self-employed, and property area.")
    # except Exception as e:
    #      print("An error occurred:", e)

    

       
    # except MultiValueDictKeyError:
    #         # Handle the case where 'Loan_ID' is missing
    #      Loan_ID = None  # or provide a default value

    
    gender_encoded = label_encoders['Gender'].transform([gender])[0]
    married_encoded = label_encoders['Married'].transform([married])[0]
    education_encoded = label_encoders['Education'].transform([education])[0]
    self_employed_encoded = label_encoders['Self_Employed'].transform([self_employed])[0]
    property_area_encoded = label_encoders['Property_Area'].transform([property_area])[0]

    result = model.predict([[gender_encoded, married_encoded, dependents, education_encoded,
                                  self_employed_encoded, applicant_income, coapplicant_income,
                                  loan_amount, loan_amount_term, credit_history, property_area_encoded]])
    result=result[0]
    # if result[0] == 1:
    #    print(result)
    #    result="Congratulations! You are eligible for the loan."
        
    # else:
    #     print(result)
    #     result="Sorry, you are not eligible for the loan."
         
    print(result)
    
    return render(request,'result.html',{'result':result})



    