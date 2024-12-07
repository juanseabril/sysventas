from django.db import models

class Cliente(models.Model):
    cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    valor_venta = models.DecimalField(max_digits=10, decimal_places=2)
    maneja_iva = models.BooleanField(default=False)
    porcentaje_iva = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    consecutivo = models.CharField(max_length=50, unique=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Venta {self.consecutivo}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    valor_producto = models.DecimalField(max_digits=10, decimal_places=2)
    iva_calculado = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField(default=0)

    def __str__(self):
        return f"Detalle de {self.venta}"
