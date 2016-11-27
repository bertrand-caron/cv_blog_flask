SHELL=/bin/bash

PYTHON_EXEC = python3

FLASK_EXEC = /home/bcaron/.local/bin/flask

UWSGI_EXEC = /home/bcaron/.local/bin/uwsgi

PIP_EXEC = pip3

serve: static/style.css copy_missing_example_files data_dump.tar.gz
	FLASK_APP=application.py $(FLASK_EXEC) run --host=localhost --port 8001
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
.PHONY: data_dump.tar.gz

uwsgi:
	$(UWSGI_EXEC) --ini uwsgi.ini
.PHONY: uwsgi

errors:
	pylint -E *.py
.PHONY: errors

pip:
	$(PIP_EXEC) install sass flask pyyaml uwsgi
.PHONY: pip
