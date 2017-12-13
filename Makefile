SHELL=/bin/bash

PYTHON_EXEC = python3

UWSGI_EXEC = /usr/local/bin/uwsgi

PIP_EXEC = pip3

PYTHONPATH_VAR = PYTHONPATH=$(PYTHONPATH):$(shell pwd)

FLASK_EXEC = $(PYTHONPATH_VAR) /usr/local/bin/flask

refresh: static/style.css
	sudo service cv_flask restart
.PHONY: refresh

serve: static/style.css copy_missing_example_files data_dump.tar.gz
	sudo FLASK_APP=application.py $(FLASK_EXEC) run --host=0.0.0.0 --port 80
.PHONY: serve

static/style.css: static/style.css.scss
	$(PYTHON_EXEC) compile_scss.py $<

obfuscted_test_data:
	$(PYTHON_EXEC) test/test_data.py
.PHONY: obfuscted_test_data

copy_missing_example_files:
	for file in $$(find . -name '*.example'); do\
	  if [[ ! -f $${file/.example/} ]] ; then\
	    cp $${file} $${file/.example/};\
	  fi;\
	done
.PHONY: copy_missing_example_files

data_dump.tar.gz:
	find . -name '*.yml' > file_to_archive.dat
	find 'static/uploads' -name '*.*' >> file_to_archive.dat
	tar --create --gzip --verbose --file $@ -T file_to_archive.dat
	rm file_to_archive.dat

import_data: data_dump.tar.gz
	mv $< data.tar.gz && tar -xzf $<
.PHONY: import_data

uwsgi:
	sudo $(UWSGI_EXEC) --ini uwsgi.ini
.PHONY: uwsgi

errors:
	pylint -E *.py
.PHONY: errors

pip: requirements.txt 
	$(PIP_EXEC) install -r $<
.PHONY: pip

certs:
	letsencrypt certonly --webroot -w /home/bcaron/cv_flask -d bcaron.me
.PHONY: certs

coverage: copy_missing_example_files
	coverage run test.py
	coverage html
.PHONY: coverage

pylint:
	$@ $$(find . -name '*.py')
.PHONY: pylint
