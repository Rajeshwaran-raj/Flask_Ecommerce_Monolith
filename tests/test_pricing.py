import types
from app.utils.pricing import Line, quote

class DummyCoupon:
    def __init__(self, pct): self.discount_percent = pct; self.active = True

def lookup_ok(code):
    return DummyCoupon(0.10) if code == "SAVE10" else None

def test_quote_no_coupon(app_context):
    lines = [Line(sku="A", name="A", unit_price=100.0, qty=2)]
    q = quote(lines, None, lookup_ok)
    assert q.subtotal == 200.0
    assert q.discount == 0.0
    assert q.total > 0

def test_quote_with_coupon(app_context):
    lines = [Line(sku="A", name="A", unit_price=100.0, qty=1)]
    q = quote(lines, "SAVE10", lookup_ok)
    assert q.discount == 10.0
