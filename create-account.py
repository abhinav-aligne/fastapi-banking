from banking import *

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