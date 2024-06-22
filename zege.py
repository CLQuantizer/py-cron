from fastapi import FastAPI

app = FastAPI()


@app.get("/name/{name}")
async def greeting(name):
    return {"greeting": "hello!" + name}

@app.get("/even/{num}")
async def isEven(num):
    # convert the string to integer
    num = int(num)
    # if even output yes
    # if odd output no
    if num % 2 == 0:
        return {"even": "yes"}
    else:
        return {"even": "no"}

@app.get("/divide/{num1}/{num2}")
async def add(num1, num2):
    num1 = int(num1)
    num2 = int(num2)
    if num2 == 0:
        return {"error": "cannot divide by zero"}
    # convert the string to integer
    # add the two numbers
    return {"divide": num1 / num2}