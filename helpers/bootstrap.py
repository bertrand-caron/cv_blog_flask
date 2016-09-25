from flask import Markup

def mfizz_icon():
    assert '"' not in style

    return Markup(
        '<i class="icon-{icon_name}" aria="hidden" style="{style}"></i>'.format(
            icon_name=icon_name.replace('-fa', ''),
            style=style,
        ),
    )

MFIZZ, FONT_AWESOME = 'icon', 'fa'

def icon_tag(icon_name, icon_type=None, style=''):
    assert '"' not in style

    if icon_type is None:
        if 'fa-' in icon_name:
            icon_name = icon_name.replace('fa-', '')
            icon_type = FONT_AWESOME
        elif 'icon-' in icon_name:
            icon_name = icon_name.replace('icon-', '')
            icon_type = MFIZZ
        else:
            raise Exception('Unrecognised icon_type')

    assert icon_type in [MFIZZ, FONT_AWESOME]

    return Markup(
        '<i class="{icon_prefix}-{icon_name}" aria="hidden" style="{style}"></i>'.format(
            icon_name=icon_name,
            icon_prefix='fa fa' if icon_type == FONT_AWESOME else 'icon',
            style=style,
        ),
    )

def rating_tag(rating):
    assert rating in range(0, 6)

    return ''.join(
        [icon_tag('fa-star')] * rating
        +
        [icon_tag('fa-star-o')] * (5 - rating)
    )
