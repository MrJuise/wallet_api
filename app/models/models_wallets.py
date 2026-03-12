from uuid import UUID, uuid4

from app.db.db_base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Uuid, Integer


class Wallet(Base):
    __tablename__ = 'wallets'

    uuid: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    balance: Mapped[int] = mapped_column(Integer, default=0)
