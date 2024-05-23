from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaultfilters import date
from django.utils import timezone
from datetime import datetime

register = template.Library()

def moneda(valor):
    valor = round(float(valor), 2)
    valor_entero = int(valor)
    parte_decimal = ("%0.2f" % valor)[-3:]
    parte_entera_formateada = intcomma(valor_entero, use_l10n=False)
    return "%s%s" % (parte_entera_formateada, parte_decimal)

def decimal(valor):
    valor = round(float(valor), 2)
    return "%s.%s" % (intcomma(int(valor)), ("%0.2f" % valor)[-3:])

def decimal3(valor):
    valor = round(float(valor), 3)
    return "%s.%s" % (intcomma(int(valor)), ("%0.3f" % valor)[-3:])

def fecha(fecha, formato='d/m/Y'):
    return date(fecha, formato)

def fechaHora(fecha, formato='%d/%m/%Y %H:%M'):
    local_fecha = timezone.localtime(fecha)
    return local_fecha.strftime(formato)

register.filter('moneda', moneda)
register.filter('decimal', decimal)
register.filter('decimal3', decimal3)
register.filter('fecha', fecha)
register.filter('fechaHora', fechaHora)