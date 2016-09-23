from flask import Flask, render_template, url_for, Markup
from yaml import load

def all_posts():
    from glob import glob
    post_files = glob('data/posts/*.yml')
    return [
        load(open(post_file).read())
        for post_file in post_files
    ]

def rendered_all_posts():
    return ''.join(
        [
            Markup(render_template('blog_post.html', post=post))
            for post in all_posts()
        ]
    )
