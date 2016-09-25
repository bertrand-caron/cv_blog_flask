serve: static/style.css
	make test
	FLASK_APP=application.py flask run --host=0.0.0.0
.PHONY: serve

static/style.css: static/style.css.scss
	python compile_scss.py $<

test:
	python test/test_data.py
.PHONY: test

install:
	for file in $$(find . -name '*.example'); do cp $${file} $${file/.example/}; done
.PHONY: install
