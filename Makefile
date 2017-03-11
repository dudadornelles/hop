init: requirements develop

install:
	python setup.py install --record files.txt

develop:
	python setup.py develop

lint:
	pylint hop

pip:
	pip install -r requirements.txt
	pip install -r test-requirements.txt

dockerimages:
	docker pull gocd/gocd-server:latest
	docker pull gocd/gocd-agent:latest

requirements: pip dockerimages

test: clean pip develop lint
	nosetests --with-coverage --cover-package=hop --cover-branches --cover-xml --with-xunit

unit:
	nosetests -w test/testunit/

integration:
	nosetests -w test/testintegration/

debug-unit:
	nosetests -w test/testunit/ -s

debug-integration:
	nosetests -w test/testintegration/ -s

clean:
	rm -rf build/ dist/ *.egg-info/ **/*.pyc
	cat files.txt | xargs rm -rf 
	
cleandocker:
	docker kill `docker ps -q`
	docker rm `docker ps -a -q`
	docker network prune -f

