from fastapi import APIRouter, Response, status, Depends
from src.db import get_async_session
from src.apps.vehicles.schemas import VINRequest
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.vehicles.models import Vehicle
from src.apps.vehicles.schemas import VINRequest, VINResponse
from typing import List



router = APIRouter(
    tags=["vehicles"],
    prefix="/vehicles",
)


@router.get("/", response_model=List[VINRequest], status_code=status.HTTP_200_OK)
async def get_vehicles(session: AsyncSession = Depends(get_async_session)):
    vehicles = await Vehicle.get_vehicles(session=session)
    return (vehicles)


@router.get("/{vin}/", response_model=VINRequest, status_code=status.HTTP_200_OK)
async def get_vehicles_by_vin(vin: str, session: AsyncSession = Depends(get_async_session)):
    return await Vehicle.get_vehicles_by_vin(vin=vin, session=session)