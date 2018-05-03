from typing import List, Any
from glob import glob
from datetime import datetime
from markdown import markdown
from flask import render_template, Markup
from yaml import load

from helpers.sections import Item, should_include_item

def read_post(post_filepath: str) -> str:
    with open(post_filepath) as fh:
        return load(fh.read())

def all_posts(sorted_on: str = 'date', order: str = 'DESC') -> List[Item]:
    ORDER_DICT = {
        'ASC': False,
        'DESC': True
    }

    post_files = glob('data/posts/*.yml')
    return sorted(
        filter(
            should_include_item,
            [
                read_post(post_file)
                for post_file in post_files
            ],
        ),
        key=lambda item: datetime.strptime(item[sorted_on], '%Y-%m-%d'),
        reverse=ORDER_DICT[order],
    )

def rendered_all_posts() -> Any:
    from application import CONFIG

    return render_template(
        'blog_body.html',
        posts=Markup(
            ''.join(
                [
                    render_template('blog_post.html', post=post, markdown=markdown)
                    for post in all_posts()
                ]
            ),
        ),
        config=CONFIG,
    )
