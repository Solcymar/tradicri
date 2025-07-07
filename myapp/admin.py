from django.contrib import admin
from .models import Cliente, Combo, PlatoEspecial, Receta, ComboPlato, Pedido, Decoracion, PedidoPlato, PedidoCombo, PedidoDecoracion

# ✅ Permite editar los platos de un combo directamente desde el admin
class ComboPlatoInline(admin.StackedInline):
    model = ComboPlato
    extra = 1
    filter_horizontal = ('platos',)

class ComboAdmin(admin.ModelAdmin):
    inlines = [ComboPlatoInline]

# Registro de modelos en el admin
admin.site.register(Cliente)
admin.site.register(Combo, ComboAdmin)  # Usa el ComboAdmin con Inline
admin.site.register(PlatoEspecial)
admin.site.register(Receta)
admin.site.register(Pedido)
admin.site.register(Decoracion)
admin.site.register(PedidoPlato)
admin.site.register(PedidoCombo)
admin.site.register(PedidoDecoracion)