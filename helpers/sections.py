from flask import Markup, render_template, url_for
from yaml import load

ITEM_TEMPLATE_FOR = {
    'education': 'item.html',
    'skills': 'item_skill.html',
    'publications': 'item_publication.html',
    'teaching': 'item.html',
    'awards': 'item_award.html',
    'referees': 'item_referee.html',
}

ALL_SECTIONS = ['education', 'skills', 'publications', 'teaching', 'awards', 'referees']

assert set(ALL_SECTIONS) == set(ITEM_TEMPLATE_FOR), 'ERROR: Missing item templates or sections.'

def data_for_section(section_name):
    return load(open('data/{0}.yml'.format(section_name)).read())

def rendered_data_for_section(section_name):
    render_item = lambda item: render_template(
        ITEM_TEMPLATE_FOR[section_name],
        item=item,
    )

    return Markup(
        ''.join([
            render_item(item)
            for item in data_for_section(section_name)
        ])
    )

def rendered_section(section_name):
    return Markup(
        render_template(
            'section.html',
            section_name=section_name,
            section_content=rendered_data_for_section(section_name),
        ),
    )
