from flask import Flask, render_template, url_for, Markup
from yaml import load

app = Flask(__name__)
config = load(open('config/config.yml').read())

ITEM_TEMPLATE_FOR = {
    'education': 'item.html',
    'skills': 'item_skill.html',
    'publications': 'item_publication.html',
    'teaching': 'item.html',
    'awards': 'item_award.html',
}

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

@app.route('/')
def home():
    return render_template(
        'main.html',
        url_for=url_for,
        config=config,
        sections = [
            rendered_section(section_name)
            for section_name in ['education', 'skills', 'publications', 'teaching', 'awards']
        ],
    )

@app.route('/cv')
def cv():
    return ''
