from django import template
from ..models import ComboPlato

register = template.Library()

@register.filter
def get_platos_del_combo(combo):
    return ComboPlato.objects.filter(combo=combo)
