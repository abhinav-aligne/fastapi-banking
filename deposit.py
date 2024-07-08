from banking import *

@app.put("/deposit/{id}/{amount}")
async def deposit(id:int, amount:int):
    try:
        checking_query = "SELECT * FROM accounts WHERE account_id = %s"
        value_query = (id,)
        mycursor.execute(checking_query, value_query)
        checked_id = mycursor.fetchone()
        if checked_id:
            query = "UPDATE accounts SET balance = balance + %s WHERE account_id = %s"
            values = (amount, id)
            mycursor.execute(query, values)
            mydb.commit()
            return {"Successfully deposited"}
        else:
            raise HTTPException(status_code=404, detail= "Account not Found in the database list")
    except SQL.Error as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")