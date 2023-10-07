from fastapi import APIRouter, status, Depends
from src.db import get_async_session
from src.apps.vehicles.schemas import VINRequest
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.vehicles.models import Vehicle
from src.apps.vehicles.schemas import VINRequest
from typing import List



vehicles_router = APIRouter(
    tags=["vehicles"],
    prefix="/vehicles",
)


@vehicles_router.get("/", response_model=List[VINRequest], status_code=status.HTTP_200_OK)
async def get_vehicles(session: AsyncSession = Depends(get_async_session)):
    """
    Получить список всех транспортных средств из базы данных.
    """
    vehicles = await Vehicle.get_vehicles(session=session)
    return (vehicles)


@vehicles_router.get("/{vin}/", response_model=VINRequest, status_code=status.HTTP_200_OK)
async def get_vehicles_by_vin(vin: str, session: AsyncSession = Depends(get_async_session)):
    """
    Получить информацию о транспортном средстве по его VIN-коду.
    """
    return await Vehicle.get_vehicles_by_vin(vin=vin, session=session)