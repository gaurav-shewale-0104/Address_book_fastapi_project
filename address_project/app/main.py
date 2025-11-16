from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from . import schemas, crud_operations, models
from .utils import haversine
import logging
import os

app = FastAPI()

# ---------------------------- Logging Setup ------------------------------
log_dir = "/logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=f"{log_dir}/log",
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    level=logging.INFO)

# ---------------------------- Database Init ------------------------------
Base.metadata.create_all(bind=engine)

# ---------------------------- Dependency ---------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------- CRUD Operations Routes --------------------------------

@app.post("/addresses/", response_model=schemas.AddressResponse)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    logging.info("Creating address: %s", address.title)
    return crud_operations.create_address(db, address)


@app.get("/addresses/{id}", response_model=schemas.AddressResponse)
def get_address(id: int, db: Session = Depends(get_db)):
    obj = crud_operations.get_address(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Address not found")
    return obj


@app.get("/addresses/", response_model=list[schemas.AddressResponse])
def list_addresses(db: Session = Depends(get_db)):
    return crud_operations.get_all_addresses(db)


@app.put("/addresses/{id}", response_model=schemas.AddressResponse)
def update_address(id: int, updates: schemas.AddressUpdate, db: Session = Depends(get_db)):
    obj = crud_operations.get_address(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Address not found")
    
    logging.info("Updating address ID %s", id)
    return crud_operations.update_address(db, obj, updates)


@app.delete("/addresses/{id}")
def delete_address(id: int, db: Session = Depends(get_db)):
    deleted = crud_operations.delete_address(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Address not found")
    logging.info("Deleted address ID %s", id)
    return {"message": "Deleted successfully"}


# ---------------------------- Radius Search -------------------------------
@app.get("/addresses/nearby/", response_model=list[schemas.AddressResponse])
def get_addresses_within(
    latitude: float,
    longitude: float,
    distance_km: float,
    db: Session = Depends(get_db)
):
    all_addresses = crud_operations.get_all_addresses(db)
    result = []

    for addr in all_addresses:
        d = haversine(latitude, longitude, addr.latitude, addr.longitude)
        if d <= distance_km:
            result.append(addr)

    return result