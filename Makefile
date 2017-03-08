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

test: lint unit integration
	nosetests --with-coverage --cover-package=hop --cover-branches --cover-xml --with-xunit

unit:
	nosetests -w test/unit/

integration:
	nosetests -w test/integration/

debug-unit:
	nosetests -w test/unit/ -s

debug-integration:
	nosetests -w test/integration/ -s

clean:
	rm -rf build/ dist/ *.egg-info/ **/*.pyc
	cat files.txt | xargs rm -rf 
	
cleandocker:
	docker kill `docker ps -a -q` && docker rm `docker ps -a -q` && docker network prune -f

