class Carrito:
    def __init__(self,request):
        self.request = request
        self.session = request.session
        self.total = 0
        carrito = self.session.get('carrito')
        if not carrito:
            self.session['carrito'] = {}
            self.carrito = self.session['carrito']
        else:
            self.carrito = carrito
    
    def agregarProducto(self, producto):
        id = str(producto.idProducto)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                "producto_id" : producto.idProducto,
                "nombre" : producto.nombre,
                "precio" : producto.precio,
                "cantidad" : 1,
            }
        else:
            self.carrito[id]['cantidad'] += 1
            self.carrito[id]['precio'] += producto.precio
            self.total += producto.precio
        self.guardarCarrito()
    
    def guardarCarrito(self):
        self.session['carrito'] = self.carrito
        self.session.modified = True

    def eliminarProducto(self, producto):
        id = str(producto.idProducto)
        if id in self.carrito:
            
            del self.carrito[id]
            
            self.guardarCarrito()
    
    def restarProducto(self,producto):
        id = str(producto.idProducto)
        if id in self.carrito.keys():
            self.carrito[id]['cantidad'] -= 1
            self.carrito[id]['precio'] -= producto.precio
            
            if self.carrito[id]['cantidad'] <= 0: self.eliminarProducto(producto)
            self.guardarCarrito()
    
    def limpiarCarrito(self):
        self.session['carrito'] = {}
        self.session.modified = True

    def totalCarrito(self, request):
        if request.user.is_authenticated:
            if "carrito" in request.session.keys():
                for key, value in request.session['carrito'].items():
                    self.total += int(value['precio'])
        return self.total