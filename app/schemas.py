from pydantic import BaseModel, Field, field_validator

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
        
        
# Optional update schema (allows partial updates if needed later)
class AddressUpdate(BaseModel):
    name: str | None = None
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)