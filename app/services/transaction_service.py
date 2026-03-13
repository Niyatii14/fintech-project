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
