"""What an invoice comes to.

A total is kept in the smallest unit of the invoice's currency: whole cents for euros, whole yen
for yen.
"""

from __future__ import annotations

from app.models import Invoice, Line
from app.money import exponent_of


def line_total(line: Line, tax_rate: float, exponent: int) -> float:
    """One line with its tax, rounded to the currency's decimals."""
    return round(line.unit_price * line.quantity * (1 + tax_rate), exponent)


def invoice_total(invoice: Invoice) -> int:
    """The invoice's total, tax included, in the smallest unit of its currency."""
    exponent = exponent_of(invoice.currency)
    total = sum(line_total(line, invoice.tax_rate, exponent) for line in invoice.lines)
    return round(total * 10**exponent)
