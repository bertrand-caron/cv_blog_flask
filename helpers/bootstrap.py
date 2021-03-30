from typing import Optional, Tuple
from flask import Markup

MFIZZ, FONT_AWESOME = 'icon', 'fa'

def icon_tag(icon_name: str, icon_type: Optional[str] = None, style: str = '') -> Markup:
    assert '"' not in style, style

    if not icon_name:
        return Markup('')
    else:
        if icon_type is None:
            if 'fa-' in icon_name:
                icon_name = icon_name.replace('fa-', '')
                icon_type = FONT_AWESOME
            elif 'icon-' in icon_name:
                icon_name = icon_name.replace('icon-', '')
                icon_type = MFIZZ
            else:
                raise Exception('Unrecognised icon_type')

        assert icon_type in [MFIZZ, FONT_AWESOME], icon_type

        return Markup(
            '<i class="{icon_prefix}-{icon_name}" aria="hidden" style="{style}"></i>'.format(
                icon_name=icon_name,
                icon_prefix='fa fa' if icon_type == FONT_AWESOME else 'icon',
                style=style,
            ),
        )

def rating_tag(rating: int, scale: Tuple[int, int] = (0, 5)) -> str:
    try:
        min_rating, max_rating = scale
    except TypeError as e:
        raise Exception('Invalid scale: {0}'.format(scale)) from e

    assert rating in range(min_rating, max_rating + 1), (rating, scale)

    return ''.join(
        [icon_tag('fa-star')] * rating
        +
        [icon_tag('fa-star-o')] * (max_rating - rating)
    )
