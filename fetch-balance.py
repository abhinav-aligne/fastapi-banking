from banking import * 

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