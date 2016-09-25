from flask import Flask, render_template, url_for, Markup
from yaml import load

from helpers.sections import rendered_section, ALL_SECTIONS
from helpers.blog import rendered_all_posts
from helpers.email import obfuscate_email
from helpers.bootstrap import fa_icon

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
        footer = Markup(render_template('footer.html')),
    )

@app.route('/')
def home():
    return main_layout(
        render_template(
            'cv_header.html',
            config=config,
            url_for=url_for,
            fa_icon=fa_icon,
        )
        +
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
        body=(
            render_template(
                'blog_author_side.html',
                fa_icon=fa_icon,
                config=config,
            )
            +
            rendered_all_posts()
        ),
    )

@app.route('/contact')
def contact():
    return main_layout(
        body=render_template(
            'contact.html',
            email=obfuscate_email(config['social']['email']),
        ),
    )
