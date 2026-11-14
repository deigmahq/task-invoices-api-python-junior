# Invoices API

The invoice totals behind the accounts screen, and the month-end statements the accounts team
sends out.

## Some invoice totals are a few units off

Support ticket #4907. Finance compared the API with the paper invoices for March and found totals
that do not match. Two they sent:

- **INV-2231**, EUR, tax 19 %: Seat licence 4.95 x 3, Storage pack 9.99 x 2, Onboarding call
  12.50 x 1. The paper invoice says 56.32; the API says 56.33.
- **INV-2240**, JPY, tax 10 %: Cable set 315 x 1, Adapter 155 x 1, Monitor stand 645 x 3. The paper
  invoice says 2,646; the API says 2,644.

The paper invoices add up the lines exactly, apply the tax to that sum, and round once, to the
currency's smallest unit, with halves rounded up. Accounts in other currencies show the same kind
of gap.

Expected: the API's total is the paper invoice's.

To see it, from the repository root, in a Python shell:

```python
from datetime import date

from app.models import Invoice, Line
from app.totals import invoice_total

eur = Invoice(
    "INV-2231",
    "Birch & Co",
    date(2026, 3, 9),
    "EUR",
    0.19,
    (
        Line("Seat licence", 4.95, 3),
        Line("Storage pack", 9.99, 2),
        Line("Onboarding call", 12.50, 1),
    ),
)
jpy = Invoice(
    "INV-2240",
    "Kita Trading",
    date(2026, 3, 12),
    "JPY",
    0.10,
    (
        Line("Cable set", 315, 1),
        Line("Adapter", 155, 1),
        Line("Monitor stand", 645, 3),
    ),
)
print(invoice_total(eur), invoice_total(jpy))
```

A total is in the smallest unit of the currency, so this prints `5633 2644`: 56.33 euros and 2,644
yen.

## Running it

Python 3.10 or newer.

```
python -m pip install -r requirements.txt
python -m pytest
```

Totals are computed in `app/totals.py`; the statements are built in `billing/export.py`.
