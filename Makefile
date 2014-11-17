test:
	venv/bin/nosetests --with-specplugin tests/

pep8:
	pep8 --max-line-length=119 --show-source planner/
	pep8 --max-line-length=119 --show-source tests/

pyflakes:
	pylama -l pyflakes planner/
	pylama -l pyflakes tests/

lint:
	make pep8
	make pyflakes