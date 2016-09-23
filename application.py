from flask import Flask, render_template, url_for, Markup
from yaml import load

from helpers.sections import rendered_section, ALL_SECTIONS
from helpers.blog import rendered_all_posts

app = Flask(__name__)

try:
    config = load(open('config/config.yml').read())
except:
    raise Exception('ERROR: Missing config/config.yml file.')

def main_layout(body):
    return render_template(
        'main.html',
        url_for=url_for,
        config=config,
        body = Markup(body),
    )

@app.route('/')
def home():
    return main_layout(
        ''.join([
            rendered_section(section_name)
            for section_name in ALL_SECTIONS
        ]),
    )

@app.route('/cv')
def cv():
    return ''

@app.route('/blog')
def blog():
    return main_layout(
        body=rendered_all_posts(),
    )
