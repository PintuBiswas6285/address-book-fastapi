from pydantic import BaseModel, Field, field_validator

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, database
from app.utils import calculate_distance
from app.logger import logger


# Base schema with validation
class AddressBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    latitude: float = Field(..., ge=-90, le=90)       # valid latitude range
    longitude: float = Field(..., ge=-180, le=180)    # valid longitude range

    @field_validator("name")
    def clean_name(cls, value):
        return value.strip()  # remove extra spaces

# Schema for create request
class AddressCreate(AddressBase):
    pass

# Schema for response (ORM -> JSON)
class AddressResponse(AddressBase):
    id: int

    class Config:
        from_attributes = True  # enables ORM serialization
        


router = APIRouter(prefix="/api/v1")

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create address API
@router.post("/addresses", response_model=schemas.AddressResponse)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    logger.info("Create address request received")

    try:
        result = crud.create_address(db, address)
        logger.info("Address created successfully")
        return result

    except Exception as e:
        logger.error(f"DB error: {e}")
        raise HTTPException(status_code=500, detail="Database error")

# Get all addresses
@router.get("/addresses", response_model=list[schemas.AddressResponse])
def get_all_addresses(db: Session = Depends(get_db)):
    return crud.get_addresses(db)

# Delete address API
@router.delete("/addresses/{id}")
def delete_address(id: int, db: Session = Depends(get_db)):
    result = crud.delete_address(db, id)

    if not result:
        raise HTTPException(status_code=404, detail="Address not found")

    return {"message": "Deleted successfully"}

# Get nearby addresses (core feature)
@router.get("/addresses/nearby", response_model=list[schemas.AddressResponse])
def get_nearby(lat: float, lon: float, distance: float, db: Session = Depends(get_db)):
    logger.info("Nearby search request received")

    try:
        addresses = crud.get_addresses(db)

        nearby = [
            addr for addr in addresses
            if calculate_distance(lat, lon, addr.latitude, addr.longitude) <= distance
        ]

        logger.info(f"{len(nearby)} addresses found within {distance} km")
        return nearby

    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
# Base schema with validation
class AddressBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    latitude: float = Field(..., ge=-90, le=90)       # valid latitude range
    longitude: float = Field(..., ge=-180, le=180)    # valid longitude range

    @field_validator("name")
    def clean_name(cls, value):
        return value.strip()  # remove extra spaces

# Schema for create request
# Schema for update request
class AddressUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)

    @field_validator("name")
    def clean_name(cls, value):
        if value is not None:
            return value.strip()
        return value

# Schema for response (ORM -> JSON)
class AddressResponse(AddressBase):
    id: int

    class Config:
        from_attributes = True  # enables ORM serialization
        

