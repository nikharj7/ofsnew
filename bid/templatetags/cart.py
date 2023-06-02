from django import template


register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(prod , cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == prod.id:
            return True
    return False

@register.filter(name='cart_quantity')
def cart_quantity(prod , cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == prod.id:
            return cart.get(id)
    return 0

@register.filter(name='price_total')
def price_total(prod , cart):
    return prod.price * cart_quantity(prod, cart)

@register.filter(name='GST')
def GST(prod , cart):
    return prod.price * cart_quantity(prod, cart) * prod.GST / 100



@register.filter(name='grand_total')
def grand_total(prod, cart):
    sum = 0
    for p in prod:
        sum += price_total(p, cart)
    return sum

@register.filter(name='gst_total')
def gst_total(prod, cart):
    sum = 0
    for p in prod:
        sum += price_total(p, cart) + GST(p, cart)
    return sum




