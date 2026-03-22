from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate

def create_transaction(db: Session, transaction_data: TransactionCreate, user_id: int):
    new_transaction = Transaction(
        amount = transaction_data.amount,
        category = transaction_data.category,
        description = transaction_data.description,
        type = transaction_data.type,
        user_id = user_id
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction

def delete_transaction(db: Session, transaction_id: int, user_id: int):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()

    if not transaction:
        return None
    if transaction.user_id != user_id:
        return "unauthorized"
    db.delete(transaction)
    db.commit()

    return transaction

def update_transaction(db: Session, transaction_id: int, user_id: int, data: TransactionCreate):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()

    if not transaction:
        return None
    if transaction.user_id != user_id:
        return "unauthorized"
    
    transaction.amount = data.amount
    transaction.category = data.category
    transaction.description = data.description
    transaction.type = data.type

    db.commit()
    db.refresh(transaction)

    return transaction

