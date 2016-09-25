from flask import Markup

def fa_icon(icon_name, style=''):
    assert '"' not in style

    return Markup(
        '<i class="fa fa-{icon_name}" aria="hidden" style="{style}"></i>'.format(
            icon_name=icon_name,
            style=style,
        ),
    )

def rating_tag(rating):
    assert rating in range(0, 6)

    return ''.join(
        [fa_icon('star')] * rating
        +
        [fa_icon('star-o')] * (5 - rating)
    )
