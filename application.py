from flask import Flask, render_template, url_for, Markup, request

from helpers.sections import rendered_section, ALL_SECTIONS
from helpers.blog import rendered_all_posts
from helpers.email import obfuscate_email
from helpers.bootstrap import icon_tag
from helpers.db import log_access
from helpers.config import CONFIG

application = Flask(__name__)

def main_layout(body: str) -> str:
    log_access(request)
    return render_template(
        'main.html',
        url_for=url_for,
        config=CONFIG,
        body = Markup(body),
        footer = Markup(render_template('footer.html')),
    )

@application.route('/')
def home() -> str:
    return main_layout(
        render_template(
            'cv_header.html',
            config=CONFIG,
            url_for=url_for,
            icon_tag=icon_tag,
        )
        +
        ''.join([
            rendered_section(section_name)
            for section_name in ALL_SECTIONS
        ]),
    )

@application.route('/cv')
def cv() -> str:
    return ''

@application.route('/blog')
def blog() -> str:
    return main_layout(
        body=(
            render_template(
                'blog_author_side.html',
                icon_tag=icon_tag,
                config=CONFIG,
            )
            +
            rendered_all_posts()
        ),
    )

@application.route('/contact')
def contact() -> str:
    return main_layout(
        body=render_template(
            'contact.html',
            email=obfuscate_email(CONFIG['social']['email']),
        ),
    )

@application.route('/data')
def data() -> str:
    return main_layout(
        body=render_template(
            'data.html',
            config=CONFIG,
        ),
    )

if __name__ == "__main__":
    application.run()
