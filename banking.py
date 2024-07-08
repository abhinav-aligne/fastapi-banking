# Import necessary libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector as SQL

# Connect to MySQL database
mydb =  SQL.connect(
        user ='root',
        password = "Aligne",
        host = "localhost",
        port = 3306
)
mycursor = mydb.cursor()

sql1 = "USE banking"
mycursor.execute(sql1)

# Initialize FastAPI
app = FastAPI()

# Create models for request and response data
class BankAccount(BaseModel):
    name_customer : str  
    account_id: int
    balance: float

class amt(BaseModel):
    account_id : int
    amount : float 
