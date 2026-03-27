# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from pydantic import BaseModel, Field, field_validator, ConfigDict

# Base schema with validation
class AddressBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    # Clean whitespace in name
    @field_validator("name")
    def clean_name(cls, value):
        return value.strip()

# Schema for create request
class AddressCreate(AddressBase):
    pass

# Schema for update request (allow partial updates)
class AddressUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)

    @field_validator("name")
    def clean_name(cls, value):
        if value is not None:
            return value.strip()
        return value

# Schema for response (ORM -> JSON), safe for Pydantic v2 + SQLAlchemy
class AddressResponse(AddressBase):
    id: int
    # This is Pydantic v2 ORM mode
    model_config = ConfigDict(from_attributes=True)
