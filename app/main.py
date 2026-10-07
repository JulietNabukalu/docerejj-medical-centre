from fastapi.staticfiles import StaticFiles
from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from . config import settings
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models,schemas,utils
from.database import engine,get_db
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from.routers import users,drugs,patients,auth,admin,sales

#models.Base.metadata.create_all(bind=engine)
print("TABLES FOUND:", models.Base.metadata.tables.keys())

models.Base.metadata.create_all(bind=engine)

print("TABLE CREATION FINISHED")

from sqlalchemy import text

with engine.connect() as connection:
    result = connection.execute(text("SELECT current_database()"))
    print("CURRENT DATABASE:", result.scalar())

app=FastAPI()
#@app.get("/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

try:
  conn=psycopg2.connect(host='localhost',database='docerejjapi',user='postgres',password='DMC2024',cursor_factory=RealDictCursor)
  cursor=conn.cursor()
  print('Database connection established')

except  Exception as error:
  print(error)


async def root():
  return{"message":"This is Docerejj Pharmacy POS"}

#@app.post("/enterdrugs")
#def enter_drugs(pos:dict = Body(...)):
  #print(drugs)
  #return{"message":"entered drugs"}

@app.get("/sqlalchemy")
def test_drugs(db:Session =Depends(get_db)):
  return{"status":"success"}

app.include_router(users.router)
app.include_router(auth.router)

app.include_router(drugs.router)

app.include_router(admin.router)

app.include_router(sales.router)