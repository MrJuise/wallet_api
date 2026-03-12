from enum import Enum
from pydantic import BaseModel, Field


class OperationEnum(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class RequestWallet(BaseModel):
    operation_type: OperationEnum
    amount: int = Field(gt=0)


class ResponseWallet(BaseModel):
    balance: int
