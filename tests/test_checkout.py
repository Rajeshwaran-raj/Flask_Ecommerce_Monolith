import json
from app import create_app
from app.extensions import db
from app.models import User, Product, Category, Coupon

def setup_module(module):
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:", WTF_CSRF_ENABLED=False)
    module.app = app
    with app.app_context():
        db.create_all()
        u = User(email="t@example.com", name="T"); u.set_password("pw"); db.session.add(u)
        c = Category(name="Cat"); db.session.add(c); db.session.flush()
        p = Product(sku="S1", name="Thing", price=100.0, stock=5, category_id=c.id); db.session.add(p)
        db.session.add(Coupon(code="SAVE10", discount_percent=0.10, active=True))
        db.session.commit()

def test_checkout_flow():
    client = app.test_client()
    # login
    client.post("/auth/login", data={"email": "t@example.com", "password": "pw"}, follow_redirects=True)
    # add to cart via API
    client.post("/api/v1/cart/add", json={"product_id": 1, "qty": 2})
    # quote
    r = client.post("/api/v1/quote", json={"lines":[{"sku":"S1","name":"Thing","unit_price":100.0,"qty":2}],"coupon":"SAVE10"})
    assert r.status_code == 200
    # checkout page (GET then POST)
    r = client.get("/orders/checkout")
    assert r.status_code == 200
    r = client.post("/orders/checkout", follow_redirects=True)
    assert r.status_code == 200
