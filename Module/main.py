from fastapi import FastAPI
from typing import Optional


app = FastAPI()

#Path parameters

@app.get("/add/{x}/{y}")
def add(x:float,y:float)-> float:
    return x+y

#Query paramters
@app.get("/increment/{x}")
def increment(x:int,y:int,z:Optional[str] =None)-> int:
    print(z or "hello!")
    return x+y

@app.get("/")
async def root():
    return {"message": "Hello World"}