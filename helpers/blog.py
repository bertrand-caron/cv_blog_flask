from flask import Flask, render_template, url_for, Markup
from yaml import load
from typing import List, Any
from glob import glob

from helpers.sections import Item, should_include_item

def all_posts() -> List[Item]:
    post_files = glob('data/posts/*.yml')
    return list(
        filter(
            should_include_item,
            [
                load(open(post_file).read())
                for post_file in post_files
            ],
        ),
    )

def rendered_all_posts() -> Any:
    from application import config

    return render_template(
        'blog_body.html',
        posts=Markup(
            ''.join(
                [
                    render_template('blog_post.html', post=post)
                    for post in all_posts()
                ]
            ),
        ),
        config=config,
    )
