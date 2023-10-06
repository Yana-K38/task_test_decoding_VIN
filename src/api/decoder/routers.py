from fastapi import APIRouter
import httpx
from src.apps.vehicles.models import Vehicle
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import engine

decode_router = APIRouter()

@decode_router.post("/decode_vin/{vin}/")
async def decode_vin(vin: str):
    """
    Декодирует VIN и сохраняет информацию о транспортном средстве в базе данных.
    Args:
        vin (str): VIN-код, который нужно декодировать и сохранить.
    Returns:
        dict: JSON-данные, полученные после декодирования VIN.
    """
    vin_service_url = "https://auto.dev/api/vin/"
    # vin_service_url = "http://18.202.200.86:9099/private/vin/decodes/"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{vin_service_url}{vin}")
            response.raise_for_status()
            vin_data = response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при запросе к сервису декодирования VIN: {e}")
    async with AsyncSession(engine) as db:
        async with db.begin():
            try:
                vehicle = Vehicle(
                    vin=vin_data['squishVin'],
                    year=vin_data['years'][0]['year'],
                    make=vin_data['make']['name'],
                    model=vin_data['model']['name'],
                    type_vehicle=vin_data['categories']['vehicleStyle'],
                    color=vin_data['colors'][0]['options'][0]['name'],
                    dimensions=vin_data.get('dimensions'),
                    weight=vin_data.get('weight')
                    )
                db.add(vehicle)
                await db.commit()
                db.refresh(vehicle)
            except (IntegrityError) as e:
                db.rollback()
                raise HTTPException(
                    status_code=400,
                    detail="VIN уже существует в базе данных",
                )
            finally:
                db.close()
    return vin_data