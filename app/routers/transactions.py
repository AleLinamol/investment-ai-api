from decimal import Decimal, ROUND_HALF_UP

from fastapi import APIRouter

from app.schemas.transaction import (
    TransactionPreviewRequest,
    TransactionPreviewResponse,
)


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/preview", response_model=TransactionPreviewResponse)
def preview_transaction(
    transaction: TransactionPreviewRequest,
) -> TransactionPreviewResponse:
    gross_amount = (transaction.quantity * transaction.unit_price).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    return TransactionPreviewResponse(
        operation_type=transaction.operation_type,
        symbol=transaction.symbol,
        quantity=transaction.quantity,
        unit_price=transaction.unit_price,
        currency=transaction.currency,
        gross_amount=gross_amount,
    )
