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
    

@app.post("/create_account")
async def create_account(account: BankAccount):
    try:
        query = "INSERT INTO accounts (name_customer, account_id, balance) VALUES (%s, %s, %s)"
        values = (account.name_customer, account.account_id, account.balance)
        mycursor.execute(query, values)
        mydb.commit()
        return {"Successfully Created"}
    except SQL.Error as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")
        
@app.put("/deposit/{id}/{amount}")
async def deposit(id:int, amount:int):
    try:
        query = "UPDATE accounts SET balance = balance + %s WHERE account_id = %s"
        values = (amount, id)
        mycursor.execute(query, values)
        mydb.commit()
        return {"Successfully deposited"}
    except SQL.Error as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")

@app.put("/withdraw")
async def withdraw(w: amt):
    try:
        if not w.account_id:
            query = "UPDATE accounts SET balance = balance - %s WHERE account_id = %s"
            values = (w.amount, w.account_id)
            mycursor.execute(query, values)
            mydb.commit()
            return {"message": "Withdrawal successful"}
    except SQL.Error as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")

@app.get("/get_balance")
async def get_balance(account_id: int):
    try:
        query = "SELECT balance FROM accounts WHERE account_id = %s"
        values = (account_id,)
        mycursor.execute(query, values)
        result = mycursor.fetchone()
        if result:
            return {"balance": result[0]}
    except SQL.Error as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")
    
@app.delete("/delete")
async def delete(account_id:int):
    try:
        query = "DELETE FROM accounts WHERE account_id = %s"
        values = (account_id,)
        mycursor.execute(query, values)
        mydb.commit()
        return {"message": "Delete successful"}
    except SQL.Error as err:
        raise HTTPException(status_code= 500, detail = f"Error: {err}")