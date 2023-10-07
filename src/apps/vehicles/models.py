from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from src.db import get_async_session
from src.apps.vehicles.schemas import VINRequest, VINResponse
from sqlalchemy.sql import text
from fastapi import Depends, HTTPException, status
from fastapi_pagination import Page
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.exc import DatabaseError, IntegrityError, InternalError
from sqlalchemy.ext.asyncio import AsyncSession


Base = declarative_base()

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String, unique=True, index=True)
    year = Column(Integer)
    make = Column(String)
    model = Column(String)
    type_vehicle = Column(String, nullable=True)
    color = Column(String, nullable=True)
    dimensions = Column(String, nullable=True)  
    weight = Column(Integer, nullable=True) 
    
    
    @staticmethod
    async def get_vehicles(
        session: AsyncSession = Depends(get_async_session),
    ) -> Page[VINRequest]:
        query = text(
            """
            SELECT * 
            FROM vehicles
            """
        )
        rows: CursorResult = await session.execute(query)
        try:
            return rows.mappings().fetchall()
        except (IntegrityError, DatabaseError, InternalError) as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @staticmethod
    async def get_vehicles_by_vin(
        vin: str, session: AsyncSession = Depends(get_async_session)
    ) -> VINRequest:
        query = text(
            """
            SELECT *
            FROM vehicles WHERE vin=:vin
            """
        ).bindparams(vin=vin)
        try:
            row: CursorResult = await session.execute(query)
        except (IntegrityError, DatabaseError, InternalError) as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        try:
            return row.mappings().fetchone()
        except AttributeError as e:
            raise HTTPException(status_code=404, detail="This vin not found")
