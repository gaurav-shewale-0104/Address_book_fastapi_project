from pydantic import BaseModel, Field

class AddressBase(BaseModel):
    title: str = Field(..., min_length=2)
    description: str | None = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class AddressCreate(AddressBase):
    pass

class AddressUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    latitude: float | None = None
    longitude: float | None = None

class AddressResponse(AddressBase):
    id: int

    class Config:
        orm_mode = True