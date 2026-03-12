from fastapi import APIRouter, Depends
import uuid
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_session import get_db
from app.models.models_wallets import Wallet

router = APIRouter()


class AddWallet(BaseModel):
    balance: int = Field(ge=0)


class AddWalletResponse(BaseModel):
    balance: int
    uuid: uuid.UUID


@router.post("/add", response_model=AddWalletResponse, status_code=201)
async def add_wallet(payload: AddWallet, db: AsyncSession = Depends(get_db)):
    new_wallet = Wallet(balance=payload.balance)
    db.add(new_wallet)
    await db.commit()
    await db.refresh(new_wallet)
    return {"uuid": new_wallet.uuid, "balance": new_wallet.balance}
