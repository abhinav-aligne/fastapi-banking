# Import necessary libraries
from fastapi import FastAPI
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
class Account(BaseModel):
    account_id: int
    balance: float

# Routes for banking system
@app.post("/create_account/")
async def create_account(account: Account):
    query = "INSERT INTO accounts (account_id, balance) VALUES (%s, %s)"
    values = (account.account_id, account.balance)
    mycursor.execute(query, values)
    mydb.commit()
    return {"message": "Account created successfully"}

@app.put("/deposit/")
async def deposit(account_id: int, amount: float):
    query = "UPDATE accounts SET balance = balance + %s WHERE account_id = %s"
    values = (amount, account_id)
    mycursor.execute(query, values)
    mydb.commit()
    return {"message": "Deposit successful"}

@app.put("/withdraw/")
async def withdraw(account_id: int, amount: float):
    query = "UPDATE accounts SET balance = balance - %s WHERE account_id = %s"
    values = (amount, account_id)
    mycursor.execute(query, values)
    mydb.commit()
    return {"message": "Withdrawal successful"}

@app.get("/get_balance/")
async def get_balance(account_id: int):
    query = "SELECT balance FROM accounts WHERE account_id = %s"
    values = (account_id,)
    mycursor.execute(query, values)
    result = mycursor.fetchone()
    if result:
        return {"balance": result[0]}
    else:
        return {"message": "Account not found"}
