start:
	cd ../VirtualEnviroment/bin
	activate
	python manage.py runserver 

runserver:
	python manage.py runserver

migrations:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver

RedisDocker:
	docker pull redis
	docker run --rm --name local-redis -p 6379:6379 -d redis