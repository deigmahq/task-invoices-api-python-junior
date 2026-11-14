from __future__ import annotations

from collections.abc import Callable, Sequence
from datetime import date

import pytest

from app.models import Invoice, Line

Build = Callable[..., Invoice]


@pytest.fixture
def make_invoice() -> Build:
    """An invoice from (unit price, quantity) pairs, in dollars unless told otherwise."""

    def build(
        lines: Sequence[tuple[float, int]],
        *,
        currency: str = "USD",
        tax_rate: float = 0.0,
        number: str = "INV-0001",
        customer: str = "Acme Ltd",
    ) -> Invoice:
        return Invoice(
            number=number,
            customer=customer,
            issued_on=date(2026, 3, 9),
            currency=currency,
            tax_rate=tax_rate,
            lines=tuple(Line(f"Item {k}", price, qty) for k, (price, qty) in enumerate(lines, 1)),
        )

    return build
