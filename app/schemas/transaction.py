from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class OperationType(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class Currency(StrEnum):
    ARS = "ARS"
    USD = "USD"


class TransactionPreviewRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "operation_type": "BUY",
                    "symbol": "AAPL",
                    "quantity": "10",
                    "unit_price": "180.25",
                    "currency": "USD",
                }
            ]
        }
    )

    operation_type: OperationType
    symbol: str = Field(min_length=1, max_length=10, pattern=r"^[A-Z0-9.]+$")
    quantity: Decimal = Field(gt=0, max_digits=18, decimal_places=8)
    unit_price: Decimal = Field(gt=0, max_digits=18, decimal_places=4)
    currency: Currency

    @field_validator("symbol", mode="before")
    @classmethod
    def normalize_symbol(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip().upper()
        return value


class TransactionPreviewResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "operation_type": "BUY",
                    "symbol": "AAPL",
                    "quantity": "10",
                    "unit_price": "180.25",
                    "currency": "USD",
                    "gross_amount": "1802.50",
                }
            ]
        }
    )

    operation_type: OperationType
    symbol: str
    quantity: Decimal
    unit_price: Decimal
    currency: Currency
    gross_amount: Decimal
