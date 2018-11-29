# `cv_blog_flask`: A CV/Blog content management system written in Python3 and Flask

[![Build Status](https://travis-ci.org/bertrand-caron/cv_blog_flask.svg?branch=master)](https://travis-ci.org/bertrand-caron/cv_blog_flask)
[![Coverage Status](https://coveralls.io/repos/github/bertrand-caron/cv_blog_flask/badge.svg?branch=master)](https://coveralls.io/github/bertrand-caron/cv_blog_flask?branch=master)

## Author: Bertrand Caron

## What this is

I needed a static-website generator.
[Jekyll](https://jekyllrb.com) works great for blogs but getting it to do anything else is a great pain, so I wrote my own using [Python3](https://docs.python.org/3/) and [Flask](http://flask.pocoo.org).

## Getting started

The project comes battery-included with a Makefile.

Try running `make serve` to download the required `pip` packages and run the flask server locally.
This will also copy a bunch of example data files to `data/`.
Edit those to update your CV and restart the web server to update those changes.
Also edit the config in `config/config.yml` to change the parameters of the CV and blog.

Once this is working, you can look into getting a web server (I provide an Nginx configuration file in `nginx.conf`) to serve your Flask application.
You WILL need to update all the paths in there, and obtain SSL certificate (I use [Let's Encrypt](https://letsencrypt.org)'s `certbot`) to get it to work over HTTPS.
I used `uwsgi` as my gateway interface, I included the UWSGI config I used (`uwsgi.ini`) as well as an example `systemd` service (`cv_flask.conf`).

# Project Structure

* `data/`: Contains the CV and blog
    * `data/posts`: Contains blog posts
* `static/`: Contains assets (images, style sheets, etc.)
* `application.py`: Main Flask app
* `templates/`: Contains all the views (Jinja2 templates)
* `helpers/`: Contains the rest of the code
* `config/`: Contains the config
    * `config/config.yml`: Contains the main config

# FAQ

## I don't have a web server, but have an Amazon Web Service (AWS) account, can I host my CV on an S3 bucket?

You sure can!
First, you'll need to create an S3 bucket, which should match the content of the `BUCKET_NAME` variable in `tasks/S3_manager.py`.
Then, configure your S3 bucket for Static Website Hosting (see AWS docs).
Make sure that the index document you choose matches the `INDEX_FILENAME` variable in `tasks/S3_manager.py` (I recommend using `cv.html`).
Finally, give public read access to your bucket!

Then, set your `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variable to allow authentification.
Finally, run `python3 tasks/S3_manager.py --upload` to upload all the static files to your S3 bucket,
as well as render a static version of your CV, and upload that HTML document to become the index of your S3 bucket website.
