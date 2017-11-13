from flask import Markup, render_template, url_for
from yaml import load
from typing import Any, List, Dict, Union, Tuple

from helpers.bootstrap import rating_tag, icon_tag
from helpers.iterables import str_merge

Item = Dict[Any, Any]

ITEM_TEMPLATE_FOR = {
    'education': 'item.html',
    'skills': 'item_skill.html',
    'publications': 'item_publication.html',
    'teaching': 'item.html',
    'awards': 'item_award.html',
    'referees': 'item_referee.html',
    'experience': 'item_experience.html',
}

ALL_SECTIONS = ['experience', 'education', 'skills', 'publications', 'teaching', 'awards', 'referees']

assert set(ALL_SECTIONS) == set(ITEM_TEMPLATE_FOR), 'ERROR: Missing item templates or sections: {0}'.format(set(ALL_SECTIONS) ^ set(ITEM_TEMPLATE_FOR))

def should_include_item(item: Item) -> bool:
    if isinstance(item, dict):
        return ('publish' not in item) or ('publish' in item and bool(item['publish']))
    else:
        return True

def data_for_section(section_name: str) -> List[Item]:
    assert section_name is not 'Skills', section_name

    items = load(open('data/{0}.yml'.format(section_name)).read())
    return [
        item
        for item in items
        if should_include_item(item)
    ]

def data_for_skills_section() -> List[Tuple[str, List[Item]]]:
    section_name = 'skills'
    data = load(open('data/{0}.yml'.format(section_name)).read())

    return [
        (subsection['type'], subsection['skills'])
        for subsection in data
    ]

def rendered_data_for_section(section_name: str) -> Markup:
    render_item = lambda item: render_template(
        ITEM_TEMPLATE_FOR[section_name],
        item=item,
        rating_tag=rating_tag,
        icon_tag=icon_tag,
        img_url_for=img_url_for,
    )

    if section_name in ['skills']:
        return Markup(
            str_merge(
                '<h3 class="subsection-title">{subsection_name}</h3>'.format(subsection_name=subsection_name) + str_merge(
                    render_item(item)
                    for item in items
                )
                for (subsection_name, items) in data_for_skills_section()
            )
        )
    else:
        return Markup(
            str_merge(
                render_item(item)
                for item in data_for_section(section_name)
            )
        )

def rendered_section(section_name: str) -> Markup:
    return Markup(
        render_template(
            'section.html',
            section_name=section_name,
            section_content=rendered_data_for_section(section_name),
        ),
    )

def img_url_for(img_url: str) -> str:
    if img_url.startswith('http'):
        return img_url
    elif img_url == '':
        return ''
    else:
        return url_for('static', filename=img_url)
