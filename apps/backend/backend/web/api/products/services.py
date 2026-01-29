"""Product API services."""

from decimal import ROUND_HALF_UP, Decimal

from backend.web.api.products.schemas import ProductCreate


def check_and_set_gross_price(payload: ProductCreate) -> ProductCreate:
    """
    Check if the gross price is set, and calculate it.

    :param payload: The data for creating a new product record.
    :return: Payload object
    """
    if not payload.gross_price or payload.gross_price == 0:
        net_price = Decimal(payload.net_price)
        tax_rate = Decimal(payload.tax_rate)

        payload.gross_price = (
            net_price * (Decimal("1") + tax_rate / Decimal("100"))
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return payload
