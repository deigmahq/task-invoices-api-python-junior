import pytest

from app.money import exponent_of, format_amount


def test_euros_have_two_decimals_and_yen_have_none():
    assert exponent_of("EUR") == 2
    assert exponent_of("JPY") == 0


def test_an_unknown_currency_is_refused():
    with pytest.raises(ValueError, match="unknown currency"):
        exponent_of("XYZ")


@pytest.mark.parametrize(
    ("minor", "currency", "written"),
    [
        (12345, "EUR", "123.45"),
        (5, "EUR", "0.05"),
        (1099, "JPY", "1099"),
        (1234, "KWD", "1.234"),
        (-250, "USD", "-2.50"),
        (0, "USD", "0.00"),
    ],
)
def test_amounts_are_written_in_their_currency(minor, currency, written):
    assert format_amount(minor, currency) == written
