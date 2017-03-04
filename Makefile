init: requirements

install:
	python setup.py install --record files.txt

develop:
	python setup.py develop

lint:
	pylint hop

requirements:
	pip install -r requirements.txt
	pip install -r test-requirements.txt

test: lint
	nosetests --with-coverage --cover-package=hop --cover-branches --cover-xml --with-xunit

debug:
	nosetests -s

clean:
	rm -rf build/ dist/ *.egg-info/ **/*.pyc
	cat files.txt | xargs rm -rf 
