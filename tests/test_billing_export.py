from datetime import date

from app.models import Invoice, Line
from app.store import InvoiceStore
from billing.export import build_statements, export_csv, upload_request
from config import settings


def _book() -> InvoiceStore:
    def invoice(number: str, customer: str, *lines: tuple[float, int]) -> Invoice:
        return Invoice(
            number=number,
            customer=customer,
            issued_on=date(2026, 3, 2),
            currency="USD",
            tax_rate=0.0,
            lines=tuple(Line("Item", price, qty) for price, qty in lines),
        )

    return InvoiceStore(
        [
            invoice("INV-0001", "Cobalt GmbH", (100.0, 1)),
            invoice("INV-0002", "Acme Ltd", (20.0, 2), (10.0, 1)),
            invoice("INV-0003", "Cobalt GmbH", (50.0, 3)),
            invoice("INV-0004", "Acme Ltd", (75.5, 2)),
        ]
    )


def test_one_statement_per_customer_in_alphabetical_order():
    statements = build_statements(_book())
    assert [(s.customer, s.currency, s.invoices, s.total) for s in statements] == [
        ("Acme Ltd", "USD", 2, 20_100),
        ("Cobalt GmbH", "USD", 2, 25_000),
    ]


def test_the_csv_has_one_row_per_statement():
    assert export_csv(_book()) == (
        "customer,currency,invoices,total\nAcme Ltd,USD,2,201.00\nCobalt GmbH,USD,2,250.00\n"
    )


def test_the_upload_carries_the_csv_and_the_provider_credentials():
    request = upload_request(_book())
    assert request["method"] == "POST"
    assert str(request["url"]).startswith(settings.INVOICE_PROVIDER_URL)
    assert request["headers"] == {
        "Authorization": f"Bearer {settings.INVOICE_PROVIDER_KEY}",
        "Content-Type": "text/csv",
    }
    assert request["body"] == export_csv(_book())
