from app.totals import invoice_total


def test_a_single_line_is_its_price_times_its_quantity(make_invoice):
    assert invoice_total(make_invoice([(10.0, 2)])) == 2000


def test_lines_add_up(make_invoice):
    assert invoice_total(make_invoice([(10.0, 2), (5.5, 1), (20.0, 3)])) == 8550


def test_tax_is_added_to_the_total(make_invoice):
    assert invoice_total(make_invoice([(100.0, 1)], tax_rate=0.25)) == 12500


def test_tax_applies_to_every_line(make_invoice):
    assert invoice_total(make_invoice([(40.0, 1), (60.0, 2)], tax_rate=0.25)) == 20000


def test_an_invoice_without_lines_comes_to_nothing(make_invoice):
    assert invoice_total(make_invoice([])) == 0
