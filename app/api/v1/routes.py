from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, database, utils, logger

router = APIRouter(prefix="/api/v1")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/addresses", response_model=schemas.AddressResponse)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    logger.logger.info("Create request received")

    try:
        result = crud.create_address(db, address)
        logger.logger.info("Address created successfully")
        return result
    except Exception as e:
        logger.logger.error(f"DB Error: {e}")
        raise HTTPException(status_code=500, detail="Database error")

@router.get("/addresses")
def get_all_addresses(db: Session = Depends(get_db)):
    return crud.get_addresses(db)

@router.delete("/addresses/{id}")
def delete_address(id: int, db: Session = Depends(get_db)):
    result = crud.delete_address(db, id)
    if not result:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Deleted successfully"}

@router.get("/addresses/nearby")
def get_nearby(lat: float, lon: float, distance: float, db: Session = Depends(get_db)):
    all_addresses = crud.get_addresses(db)

    nearby = []
    for addr in all_addresses:
        dist = utils.haversine(lat, lon, addr.latitude, addr.longitude)
        if dist <= distance:
            nearby.append(addr)

    return nearby


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
