from django import template

register = template.Library()

# Tablela zebrada
@register.filter(name='is_par')
def is_par(value):
    if value % 2 == 0:
        return True

    return False


@register.filter
def get_value(dict, key):
    return dict.get(key)

# Criar indice pra tabela
@register.filter
def get_id(value,num_page):
    id_page = num_page - 1  
    id = (id_page * 10) + value
   
    return id

@register.filter
def get_never(value):
    if '2033' in value:
        return 'ESTÁTICO'

    return value