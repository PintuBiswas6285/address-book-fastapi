from sqlalchemy.orm import Session
from . import models

# Create a new address
def create_address(db: Session, address):
    db_address = models.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

# Fetch all addresses
def get_addresses(db: Session):
    return db.query(models.Address).all()

# Delete address by ID
def delete_address(db: Session, address_id: int):
    address = db.query(models.Address).filter(models.Address.id == address_id).first()

    if not address:
        return None  # not found case

    db.delete(address)
    db.commit()
    return address

# Update existing address
def update_address(db: Session, address_id: int, updated_data):
    address = db.query(models.Address).filter(models.Address.id == address_id).first()

    if not address:
        return None

    # Update only provided fields
    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(address, key, value)

    db.commit()
    db.refresh(address)

    return address