from django import template
register = template.Library()


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


@register.filter(name="nazo_red")
def time_display(name):
    if "謎" in name:
        return "text-red-600"

    return "text-gray-800 group-hover:text-gray-600 dark:text-gray-300 dark:group-hover:text-white"