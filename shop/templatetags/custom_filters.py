from django import template

register = template.Library()

@register.filter
def get_dict_value(dictionary, key):
    """Возвращает значение из словаря по ключу"""
    return dictionary.get(key)

@register.filter
def price_format(value):
    try:
        # Преобразуем значение в строку с двумя знаками после запятой
        formatted_value = f"{value:,.2f}"
        # Заменяем запятую на пробел для разделения тысяч
        return formatted_value.replace(",", " ")
    except (ValueError, TypeError):
        return value  # Если произошла ошибка преобразования, возвращаем исходное значение