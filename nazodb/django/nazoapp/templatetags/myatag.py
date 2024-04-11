from django import template
register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    """GETパラメータを一部を置き換える"""

    url_dict = request.GET.copy()
    url_dict[field] = str(value)  # Django2.1の一部対策。通常はvalueだけでOK
    return url_dict.urlencode()


@register.simple_tag
def three_judge(value):
    if value >= 3:
        return {
            'title': "難しいよ",
            'description': "初心者は帰ってください。"
        }
    else:
        return {
            'title': "簡単です",
            'description': "初心者歓迎"
        }

@register.filter(name="rating_color")
def rating_color(value):
    if value >= 3.5:
        return "text-red-300"
    else:
        return "text-gray-300"
