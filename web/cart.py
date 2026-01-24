class Cart:
    def __init__(self,request):
        self.request = request
        self.session = request.session

        cart = self.session.get("cart")
        amountTotal = self.session.get("amountTotal")
        if not cart:
            cart = self.session['cart'] = {}
            amountTotal = self.session['amountTotal'] = "0"

        self.cart = cart
        self.amountTotal = float(amountTotal)

    def add(self, product, amount):

        if str(product.id) not in self.cart.keys():
            self.cart[product.id] = {
                "product_id": product.id,
                "name": product.name,
                "amount": amount,
                "price": str(product.price),
                "image": product.image.url,
                "category": str(product.category.name),
                "subtotal": str(product.price * amount)
            }

        else:
            for key,value in self.cart.items():
                if key == str(product.id):
                    value['amount'] = str(int(value['amount']) + amount)
                    value['subtotal'] = str(float(value['amount']) * float(value['price']))
                    break

        self.save()

    def delete(self, product_id):
        product_id = str(product_id.id)
        if product_id and product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session["cart"] = {}
        self.session["amountTotal"] = 0

    def save(self):
        """ GUARDA CAMBIOS EN EL CARRITO DE COMPRAS """
        amountTotal= 0
        for key, value in self.cart.items():
            amountTotal +=float(value['subtotal'])

        self.session['cart'] = self.cart
        self.session['amountTotal'] = amountTotal
        self.session.modified = True # es modificable esta variable de sessión