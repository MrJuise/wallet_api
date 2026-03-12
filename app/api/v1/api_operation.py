import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.db_session import get_db
from app.models.models_wallets import Wallet
from app.schemas.schemas_wallets import RequestWallet, OperationEnum, ResponseWallet

router = APIRouter()


@router.post("/wallets/{WALLET_UUID}/operation", response_model=ResponseWallet, status_code=200)
async def operation_wallet(payload: RequestWallet, WALLET_UUID: uuid.UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(Wallet).where(Wallet.uuid == WALLET_UUID).with_for_update()
    result = await db.execute(stmt)
    wallet = result.scalar_one_or_none()

    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if payload.operation_type == OperationEnum.DEPOSIT:
        wallet.balance += payload.amount

    elif payload.operation_type == OperationEnum.WITHDRAW:

        if wallet.balance < payload.amount:
            raise HTTPException(status_code=400, detail="Wallet balance too low")
        wallet.balance -= payload.amount

    await db.commit()
    await db.refresh(wallet)
    return {"balance": wallet.balance}
