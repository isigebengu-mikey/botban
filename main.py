from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
import dataset

db = dataset.connect('sqlite:///bans.db')
app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse("/docs")

@app.get("/bans/{userid}")
async def getban(userid:int):
    table = db['bans']
    result = table.find_one(userid=userid)
    if result:
        return dict(result)
    else:
        raise HTTPException(status_code=404,detail="Couldn't find user.")

@app.post("/add")
async def addban(userid:int,reason:str,creator:int,proof:str):
    table = db['bans']
    if table.find_one(userid=userid):
        return {"error":'true','detail':'This user is already banned!'}
    table.insert({'userid':userid,'reason':reason,'creator':creator,'proof':proof})
    db.commit()
    return table.find_one(userid=userid)