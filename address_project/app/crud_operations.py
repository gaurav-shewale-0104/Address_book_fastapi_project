from sqlalchemy.orm import Session
from . import models, schemas

def create_address(db: Session, data: schemas.AddressCreate):
    address = models.Address(**data.dict())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address

def get_address(db: Session, id: int):
    return db.query(models.Address).filter(models.Address.id == id).first()

def get_all_addresses(db: Session):
    return db.query(models.Address).all()

def update_address(db: Session, db_obj: models.Address, updates: schemas.AddressUpdate):
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_address(db: Session, id: int):
    obj = get_address(db, id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj