import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_session import get_db
from app.models.models_wallets import Wallet
from app.schemas.schemas_wallets import ResponseWallet

router = APIRouter()


@router.get("/wallets/{WALLET_UUID}", response_model=ResponseWallet, status_code=200)
async def get_wallet(WALLET_UUID: uuid.UUID, db: AsyncSession = Depends(get_db)):
    wallet = await db.get(Wallet, WALLET_UUID)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return {"balance": wallet.balance}
