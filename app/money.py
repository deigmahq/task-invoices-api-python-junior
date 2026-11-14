"""Currencies and how amounts are written.

Amounts are kept in the smallest unit of their currency: 12345 euro cents are 123.45 euros, 1099 yen
are 1099 yen, 1234 Kuwaiti fils are 1.234 dinars.
"""

from __future__ import annotations

from config.settings import CURRENCY_EXPONENTS


def exponent_of(currency: str) -> int:
    """Decimal places of the currency's smallest unit: 2 for EUR, 0 for JPY."""
    try:
        return CURRENCY_EXPONENTS[currency]
    except KeyError:
        raise ValueError(f"unknown currency: {currency}") from None


def format_amount(minor: int, currency: str) -> str:
    """An amount in the smallest unit, written the way it is printed: 12345 EUR -> '123.45'."""
    exponent = exponent_of(currency)
    sign = "-" if minor < 0 else ""
    whole, fraction = divmod(abs(minor), 10**exponent)
    if exponent == 0:
        return f"{sign}{whole}"
    return f"{sign}{whole}.{fraction:0{exponent}d}"
