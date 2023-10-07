import uvicorn
from fastapi import FastAPI
from src.api.decoder.routers import decode_router
from src.api.vehicles.routers import vehicles_router


app = FastAPI(
    title = "Microservice that will accept a VIN number from the exposed REST API endpoint, and return the following vehicle details by decoding the provided VIN",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(decode_router)
app.include_router(vehicles_router)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="localhost",
        port=8000,
    )