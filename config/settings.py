"""Settings the service reads when it starts."""

import os

# Currencies the service invoices in, with the number of decimal places of each one's smallest unit:
# 2 for euros (cents), 0 for yen, 3 for Kuwaiti dinars (fils).
CURRENCY_EXPONENTS = {
    "USD": 2,
    "EUR": 2,
    "GBP": 2,
    "CHF": 2,
    "DKK": 2,
    "JPY": 0,
    "KRW": 0,
    "KWD": 3,
    "BHD": 3,
}

# Invoice provider (month-end statement uploads)
INVOICE_PROVIDER_URL = os.environ.get(
    "INVOICE_PROVIDER_URL", "https://api.invoice-provider.example/v2"
)
INVOICE_PROVIDER_KEY = "ivp_7a3e91d05bc"
