from django import template


register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(prod , cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == prod.id:
            return True
    return False