from flask import Blueprint, render_template, redirect, url_for, request, session, flash, current_app
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Product, Order, OrderItem, Coupon, InventoryMovement
from ..utils.pricing import Line, quote

bp = Blueprint("orders", __name__, url_prefix="/orders")

def _cart():
    return session.get("cart", {})

def _coupon_lookup(code):
    return Coupon.query.filter_by(code=code).first()

@bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    c = _cart()
    if not c:
        flash("Your cart is empty", "warning")
        return redirect(url_for("cart.view_cart"))

    lines = []
    products = {}
    for pid, qty in c.items():
        p = Product.query.get(int(pid))
        if not p or not p.is_active:
            continue
        lines.append(Line(sku=p.sku, name=p.name, unit_price=p.price, qty=qty))
        products[p.id] = (p, qty)

    q = quote(lines, session.get("coupon"), _coupon_lookup)

    if request.method == "POST":
        # Reserve stock
        for pid, (p, qty) in products.items():
            if p.stock < qty:
                flash(f"Insufficient stock for {p.name}", "danger")
                return redirect(url_for("cart.view_cart"))

        order = Order(user_id=current_user.id, subtotal=q.subtotal, discount=q.discount,
                      tax=q.tax, shipping=q.shipping, total=q.total, coupon_code=session.get("coupon"))
        db.session.add(order)
        db.session.flush()

        for pid, (p, qty) in products.items():
            oi = OrderItem(order_id=order.id, product_id=p.id, product_name=p.name, sku=p.sku,
                           unit_price=p.price, quantity=qty, line_total=p.price * qty)
            db.session.add(oi)
            # Decrement stock + inventory movement
            p.stock -= qty
            db.session.add(InventoryMovement(product_id=p.id, delta=-qty, reason="purchase"))

        # Increment coupon usage
        if order.coupon_code:
            cpn = Coupon.query.filter_by(code=order.coupon_code).first()
            if cpn:
                cpn.times_used += 1

        db.session.commit()
        session.pop("cart", None)
        session.pop("coupon", None)
        flash("Order placed! (mock payment success)", "success")
        return redirect(url_for("orders.detail", order_id=order.id))

    return render_template("orders/checkout.html", quote=q, lines=lines)

@bp.route("/<int:order_id>")
@login_required
def detail(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash("Not authorized", "danger")
        return redirect(url_for("shop.index"))
    return render_template("orders/detail.html", order=order)
