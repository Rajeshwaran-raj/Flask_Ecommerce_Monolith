import pytest
from app.utils.inventory import reserve_stock, release_stock, InventoryError

def test_reserve_ok():
    assert reserve_stock(10, 3) == 7

def test_reserve_insufficient():
    with pytest.raises(InventoryError):
        reserve_stock(2, 3)

def test_release_ok():
    assert release_stock(5, 2) == 7
