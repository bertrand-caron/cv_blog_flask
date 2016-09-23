serve: static/style.css
	FLASK_APP=application.py flask run --host=0.0.0.0

static/style.css: static/style.css.scss
	python compile_scss.py $<
