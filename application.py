from flask import Flask, render_template, url_for, Markup
from yaml import load

from helpers.sections import rendered_section, ALL_SECTIONS

app = Flask(__name__)

try:
    config = load(open('config/config.yml').read())
except:
    raise Exception('ERROR: Missing config/config.yml file.')

@app.route('/')
def home():
    return render_template(
        'main.html',
        url_for=url_for,
        config=config,
        sections = [
            rendered_section(section_name)
            for section_name in ALL_SECTIONS
        ],
    )

@app.route('/cv')
def cv():
    return ''
