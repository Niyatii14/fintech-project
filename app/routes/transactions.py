from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transaction_service import create_transaction, delete_transaction, update_transaction
from app.core.dependencies import get_current_user
from app.models.transaction import Transaction

router = APIRouter()
@router.post("/transactions", response_model=TransactionResponse)
def create_new_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_transaction(db, transaction, current_user.id)

@router.get("/transactions", response_model = list[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    ).all()
    return transactions

@router.delete("/transactions/{id}")
def delete_user_transaction(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = delete_transaction(db, id, current_user.id)

    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="Not allowed")
    if not result:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return {"message": "Transaction deleted"}

@router.put("/transactions/{id}",response_model=TransactionResponse)
def update_user_transaction(
    id: int,
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = update_transaction(db, id, current_user.id, data)
    if result == "unauthorized":
        raise HTTPException(status_code=403, detail = "Not allowed")
    
    if not result:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return result

