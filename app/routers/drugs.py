from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,utils
#from ..database import get_db
from .. import database
from typing import Optional,List
from . import oauth2
router=APIRouter(
    prefix="/drugs",
    tags=['drugs']
)

@router.get("/", response_model=List[schemas.DrugResponse])
def get_drugs(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    drugs = db.query(models.Drug).all()

    return drugs

@router.put("/{drug_id}", response_model=schemas.DrugResponse)
def update_drug(
    drug_id: int,
    drug: schemas.DrugUpdate,
    db: Session = Depends(database.get_db),
    admin: models.User = Depends(oauth2.require_admin)
):
    existing_drug = db.query(models.Drug).filter(
        models.Drug.id == drug_id
    ).first()

    if not existing_drug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Drug not found"
        )

    existing_drug.name = drug.name
    existing_drug.price = drug.price
    existing_drug.stock_quantity = drug.stock_quantity

    db.commit()
    db.refresh(existing_drug)

    return existing_drug


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.DrugResponse)
def add_drug(drug:schemas.DrugCreate,db:Session=Depends(database.get_db),admin:models.User=Depends(
    oauth2.require_admin)):

    new_drug=models.Drug(**drug.dict())
    db.add(new_drug)
    db.commit()
    db.refresh(new_drug)
    return new_drug

@router.post("/voice")
def voice_drug_command(
    command: schemas.VoiceDrugCommand,
    db: Session = Depends(database.get_db),
    admin: models.User = Depends(oauth2.require_admin)
):
    import re

    text = command.text.lower()

    # Find price
    price_match = re.search(
        r"price\s*(?:is\s*)?(?:now\s*)?([\d,]+)",
        text
    )

    # Find stock
    stock_match = re.search(
        r"(?:stock\s+(?:is\s+)?(?:now\s+)?|stock\s+to\s+|set\s+stock\s+to\s+|to\s+)(\d+)",
        text
    )
    drug_match = re.search(
        r"add\s+(.+?)\s+(\d+\s*(?:mg|g|ml|mcg))",
        text
    )

    drug_name = drug_match.group(1).strip() if drug_match else None
    dosage = drug_match.group(2).replace(" ", "") if drug_match else None

    price = int(price_match.group(1).replace(",", "")) if price_match else None
    stock = int(stock_match.group(1)) if stock_match else None
    full_drug_name = f"{drug_name} {dosage}"
    print("FULL DRUG NAME:", repr(full_drug_name))
    print("ALL DRUGS:", [(d.id, repr(d.name)) for d in db.query(models.Drug).all()])

    existing_drug = db.query(models.Drug).filter(
        models.Drug.name.ilike(full_drug_name)

    ).first()
    print("MATCHED DRUG:", existing_drug)

    return {


        "message": "Please confirm before saving",
        "original_text": command.text,
        "drug_name": drug_name,
        "dosage": dosage,
        "price": price,
        "stock_quantity": stock,
        "existing_drug": repr(existing_drug.name) if existing_drug else None,
        "confirmation": {
            "drug": f"{drug_name} {dosage}",
            "price": price,
            "stock": stock
        }

    }

@router.post("/voice/save")
def save_voice_drug(
    command: schemas.VoiceDrugCommand,
    db: Session = Depends(database.get_db),
    admin: models.User = Depends(oauth2.require_admin)
):
    import re

    text = command.text.lower()

    # Find price
    price_match = re.search(
        r"price\s*(?:is\s*)?(?:now\s*)?([\d,]+)",
        text
    )

    # Find stock
    stock_match = re.search(
        r"(?:stock\s+(?:is\s+)?(?:now\s+)?|stock\s+to\s+|set\s+stock\s+to\s+|to\s+)(\d+)",
        text
    )

    # Find drug name and dosage
    drug_match = re.search(
        r"add\s+(.+?)\s+(\d+\s*(?:mg|g|ml|mcg))",
        text
    )

    # We must have drug and stock
    if not drug_match or not stock_match:
        raise HTTPException(
            status_code=400,
            detail="Could not understand the drug information."
        )

    drug_name = drug_match.group(1).strip()
    dosage = drug_match.group(2).replace(" ", "")

    # Price is optional
    price = (
        int(price_match.group(1).replace(",", ""))
        if price_match
        else None
    )

    stock = int(stock_match.group(1))

    # Combine drug name and dosage
    full_drug_name = f"{drug_name} {dosage}"

    # Check whether drug already exists
    existing_drug = db.query(models.Drug).filter(
        models.Drug.name.ilike(full_drug_name)
    ).first()

    # --------------------------------
    # EXISTING DRUG → UPDATE
    # --------------------------------

    if existing_drug:

        # Update stock
        existing_drug.stock_quantity = stock

        # Only update price if a new price was provided
        if price is not None:
            existing_drug.price = price

        db.commit()
        db.refresh(existing_drug)

        return {
            "message": "Existing drug updated successfully",
            "action": "updated",
            "drug": {
                "id": existing_drug.id,
                "name": existing_drug.name,
                "price": existing_drug.price,
                "stock_quantity": existing_drug.stock_quantity
            }
        }

    # --------------------------------
    # NEW DRUG → CREATE
    # --------------------------------

    # A new drug still requires a price
    if price is None:
        raise HTTPException(
            status_code=400,
            detail="A price is required when adding a new drug."
        )

    new_drug = models.Drug(
        name=full_drug_name,
        price=price,
        stock_quantity=stock
    )

    db.add(new_drug)
    db.commit()
    db.refresh(new_drug)

    return {
        "message": "Drug saved successfully",
        "action": "created",
        "drug": {
            "id": new_drug.id,
            "name": new_drug.name,
            "price": new_drug.price,
            "stock_quantity": new_drug.stock_quantity
        }
    }