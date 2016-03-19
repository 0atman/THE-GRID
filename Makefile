play:
	docker-compose run grid python grid.py
build:
	docker-compose build
test:
	docker-compose run grid py.test test.py