# `cv_blog_flask`: A CV/Blog content management system written in Python3 and Flask

[![Build Status](https://travis-ci.org/bertrand-caron/cv_blog_flask.svg?branch=master)](https://travis-ci.org/bertrand-caron/cv_blog_flask)

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
