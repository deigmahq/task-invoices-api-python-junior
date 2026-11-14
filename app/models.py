"""The records the service handles."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Line:
    """One line of an invoice. Prices arrive from the order system in the invoice's currency, as
    plain numbers: 4.95 euros, 645 yen."""

    description: str
    unit_price: float
    quantity: int


@dataclass(frozen=True)
class Invoice:
    number: str
    customer: str
    issued_on: date
    currency: str
    tax_rate: float  # 0.19 for 19 %
    lines: tuple[Line, ...]
