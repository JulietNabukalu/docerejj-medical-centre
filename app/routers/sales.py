from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas, database
from . import oauth2

router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_sale(
    sale: schemas.SaleCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    # Create the sale
    new_sale = models.Sale(
        patient_id=sale.patient_id,
        user_id=current_user.id,
        payment_method=sale.payment_method,
        total_amount=0
    )

    db.add(new_sale)
    db.flush()

    total_amount = 0

    # Process each drug
    for item in sale.items:

        drug = db.query(models.Drug).filter(
            models.Drug.id == item.drug_id
        ).first()

        if not drug:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Drug with ID {item.drug_id} not found"
            )

        if item.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be greater than zero"
            )

        if drug.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock for {drug.name}"
            )

        item_total = drug.price * item.quantity

        sale_item = models.SaleItem(
            sale_id=new_sale.id,
            drug_id=drug.id,
            quantity=item.quantity,
            unit_price=drug.price,
            total=item_total
        )

        db.add(sale_item)

        # Reduce stock
        drug.stock_quantity -= item.quantity

        total_amount += item_total

    # Update total sale amount
    new_sale.total_amount = total_amount

    db.commit()
    db.refresh(new_sale)

    return new_sale

@router.get("/")
def get_sales(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    sales = db.query(models.Sale).all()

    return sales

@router.get("/{sale_id}")
def get_sale(
    sale_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    sale = db.query(models.Sale).filter(
        models.Sale.id == sale_id
    ).first()

    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )

    items = db.query(models.SaleItem).filter(
        models.SaleItem.sale_id == sale_id
    ).all()

    sale_items = []

    for item in items:
        drug = db.query(models.Drug).filter(
            models.Drug.id == item.drug_id
        ).first()

        sale_items.append({
            "id": item.id,
            "drug_id": item.drug_id,
            "drug_name": drug.name if drug else "Unknown drug",
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "total": item.total
        })

    return {
        "sale": sale,
        "items": sale_items
    }