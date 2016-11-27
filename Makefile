SHELL=/bin/bash

serve: static/style.css install
	make test
	make data_dump.tar.gz
	FLASK_APP=application.py flask run --host=0.0.0.0
.PHONY: serve

static/style.css: static/style.css.scss
	python compile_scss.py $<

test:
	python test/test_data.py
.PHONY: test

install:
	for file in $$(find . -name '*.example'); do\
	  if [[ ! -f $${file/.example/} ]] ; then\
	    cp $${file} $${file/.example/};\
	  fi;\
	done
.PHONY: install

data_dump.tar.gz:
	find . -name '*.yml' > file_to_archive.dat
	find 'static/uploads' -name '*.*' >> file_to_archive.dat
	tar --create --gzip --verbose --file $@ -T file_to_archive.dat
	rm file_to_archive.dat
.PHONY: data_dump.tar.gz

uwsgi:
	uwsgi --ini uwsgi.ini	
.PHONY: uwsgi
