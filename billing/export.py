"""Month-end statements for the accounts team."""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass

from app.money import format_amount
from app.store import InvoiceStore
from app.totals import invoice_total
from config import settings


@dataclass
class Statement:
    customer: str
    currency: str
    invoices: int
    total: int  # in the smallest unit of the currency


def build_statements(store: InvoiceStore) -> list[Statement]:
    """One statement per customer and currency, customers in alphabetical order.

    A statement carries the number of invoices and the sum of their totals.
    """
    statements: dict[tuple[str, str], Statement] = {}
    for invoice in store.all():
        key = (invoice.customer, invoice.currency)
        statement = statements.get(key)
        if statement is None:
            statement = statements[key] = Statement(invoice.customer, invoice.currency, 0, 0)
        statement.invoices += 1
        statement.total += invoice_total(invoice)
    return [statements[key] for key in sorted(statements)]


def export_csv(store: InvoiceStore) -> str:
    """The statements as the CSV the accounts team opens."""
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(["customer", "currency", "invoices", "total"])
    for statement in build_statements(store):
        writer.writerow(
            [
                statement.customer,
                statement.currency,
                statement.invoices,
                format_amount(statement.total, statement.currency),
            ]
        )
    return out.getvalue()


def upload_request(store: InvoiceStore) -> dict[str, object]:
    """The request that hands the statements to the invoice provider.

    Only describes it; sending is the job runner's work.
    """
    return {
        "method": "POST",
        "url": f"{settings.INVOICE_PROVIDER_URL}/statements",
        "headers": {
            "Authorization": f"Bearer {settings.INVOICE_PROVIDER_KEY}",
            "Content-Type": "text/csv",
        },
        "body": export_csv(store),
    }
