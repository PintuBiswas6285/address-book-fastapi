# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, database
from app.utils import calculate_distance
from app.logger import logger

router = APIRouter(prefix="/api/v1")

#Dependency to get DB session

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
    

# Update address API
@router.put("/addresses/{id}", response_model=schemas.AddressResponse)
def update_address(id: int, address: schemas.AddressUpdate, db: Session = Depends(get_db)):
    logger.info(f"Update request for ID: {id}")

    try:
        result = crud.update_address(db, id, address)

        if not result:
            raise HTTPException(status_code=404, detail="Address not found")

        logger.info("Address updated successfully")
        return result

    except Exception as e:
        logger.error(f"Update error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    