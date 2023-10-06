import uvicorn
from fastapi import FastAPI


from fastapi import FastAPI


app = FastAPI(
    title = "Microservice that will accept a VIN number from the exposed REST API endpoint, and return the following vehicle details by decoding the provided VIN",
    docs_url="/docs",
    redoc_url="/redoc",
)



if __name__ == "__main__":
    uvicorn.run(
        app,
        host="localhost",
        port=8000,
    )