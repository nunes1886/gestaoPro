from django import template
import re

register = template.Library()

@register.filter(name='formatar_telefone')
def formatar_telefone(value):
    if not value: return ""
    v = re.sub(r'\D', '', str(value)) # Remove tudo que não é dígito
    if len(v) == 11:
        return f"({v[:2]}) {v[2:7]}-{v[7:]}"
    elif len(v) == 10:
        return f"({v[:2]}) {v[2:6]}-{v[6:]}"
    return value

@register.filter(name='formatar_cnpj')
def formatar_cnpj(value):
    if not value: return ""
    v = re.sub(r'\D', '', str(value))
    if len(v) == 14:
        return f"{v[:2]}.{v[2:5]}.{v[5:8]}/{v[8:12]}-{v[12:]}"
    return value

@register.filter(name='formatar_cpf')
def formatar_cpf(value):
    if not value: return ""
    v = re.sub(r'\D', '', str(value))
    if len(v) == 11:
        return f"{v[:3]}.{v[3:6]}.{v[6:9]}-{v[9:]}"
    return value

@register.filter(name='formatar_cep')
def formatar_cep(value):
    if not value: return ""
    v = re.sub(r'\D', '', str(value))
    if len(v) == 8:
        return f"{v[:5]}-{v[5:]}"
    return value