from django.db import models
from django.utils import timezone

class PedidoEstado(models.TextChoices):
    PENDIENTE   = 'pendiente',   'Pendiente'
    CONFIRMADO  = 'confirmado',  'Confirmado'
    ENTREGADO   = 'entregado',   'Entregado'
    CANCELADO   = 'cancelado',   'Cancelado'

class MetodoPago(models.TextChoices):
    EFECTIVO      = 'efectivo',     'Efectivo'
    TARJETA       = 'tarjeta',      'Tarjeta'
    TRANSFERENCIA = 'transferencia','Transferencia'


class Cliente(models.Model):
    nombre         = models.CharField(max_length=100)
    email          = models.EmailField(unique=True)
    telefono       = models.CharField(max_length=20, blank=True, null=True)
    direccion      = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre


class CategoriaInventario(models.Model):
    nombre      = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class CategoriaProducto(models.Model):
    nombre      = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre                 = models.CharField(max_length=100)
    categoria_inventario   = models.ForeignKey(CategoriaInventario,
                                               on_delete=models.PROTECT)
    categoria_producto     = models.ForeignKey(CategoriaProducto,
                                               on_delete=models.PROTECT)
    unidad_medida          = models.CharField(max_length=20)
    precio_unitario        = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual           = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


class PlatoEspecial(models.Model):
    nombre      = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio      = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre


class Receta(models.Model):
    plato               = models.ForeignKey(PlatoEspecial,
                                            on_delete=models.CASCADE)
    producto            = models.ForeignKey(Producto,
                                            on_delete=models.CASCADE)
    cantidad_necesaria  = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('plato', 'producto')


class Combo(models.Model):
    nombre      = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio      = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre


class ComboPlato(models.Model):
    combo     = models.ForeignKey(Combo, on_delete=models.CASCADE)
    plato     = models.ForeignKey(PlatoEspecial, on_delete=models.CASCADE)
    cantidad  = models.IntegerField()


class ComboProducto(models.Model):
    combo     = models.ForeignKey(Combo, on_delete=models.CASCADE)
    producto  = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad  = models.IntegerField()


class Decoracion(models.Model):
    nombre           = models.CharField(max_length=100)
    tema             = models.CharField(max_length=50, blank=True, null=True)
    precio_alquiler  = models.DecimalField(max_digits=10, decimal_places=2)
    stock_disponible = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    cliente       = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha_pedido  = models.DateTimeField(default=timezone.now)
    fecha_evento  = models.DateField()
    estado        = models.CharField(max_length=12,
                                     choices=PedidoEstado.choices,
                                     default=PedidoEstado.PENDIENTE)

    def __str__(self):
        return f'Pedido #{self.pk} – {self.cliente}'


class PedidoPlato(models.Model):
    pedido          = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    plato           = models.ForeignKey(PlatoEspecial, on_delete=models.PROTECT)
    cantidad        = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)


class PedidoCombo(models.Model):
    pedido          = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    combo           = models.ForeignKey(Combo, on_delete=models.PROTECT)
    cantidad        = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)


class PedidoDecoracion(models.Model):
    pedido          = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    decoracion      = models.ForeignKey(Decoracion, on_delete=models.PROTECT)
    cantidad        = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)


class Venta(models.Model):
    pedido        = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    fecha_venta   = models.DateTimeField(default=timezone.now)
    monto_total   = models.DecimalField(max_digits=12, decimal_places=2)
    metodo_pago   = models.CharField(max_length=15,
                                     choices=MetodoPago.choices)
    boleta_numero = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f'Venta #{self.pk}'


class MovimientoInventario(models.Model):
    producto         = models.ForeignKey(Producto, on_delete=models.PROTECT)
    fecha            = models.DateTimeField(default=timezone.now)
    tipo_movimiento  = models.BooleanField()  # True=ingreso, False=salida
    cantidad         = models.IntegerField()
    motivo           = models.TextField(blank=True, null=True)
    pedido_plato     = models.ForeignKey(PedidoPlato,
                                         on_delete=models.SET_NULL,
                                         blank=True,
                                         null=True)
    pedido_combo     = models.ForeignKey(PedidoCombo,
                                         on_delete=models.SET_NULL,
                                         blank=True,
                                         null=True)


class MovimientoDecoracion(models.Model):
    decoracion       = models.ForeignKey(Decoracion, on_delete=models.PROTECT)
    fecha            = models.DateTimeField(default=timezone.now)
    tipo_movimiento  = models.BooleanField()  # True=devolución, False=reserva
    cantidad         = models.IntegerField()
    motivo           = models.TextField(blank=True, null=True)
    pedido_decor     = models.ForeignKey(PedidoDecoracion,
                                         on_delete=models.SET_NULL,
                                         blank=True,
                                         null=True)


class Reporte(models.Model):
    fecha_generacion = models.DateTimeField(default=timezone.now)
    tipo_reporte     = models.CharField(max_length=20,
                                        choices=[
                                          ('inventario','Inventario'),
                                          ('ventas','Ventas'),
                                          ('pedidos','Pedidos'),
                                        ])
    parametros       = models.JSONField()
    ruta_archivo     = models.CharField(max_length=200)
