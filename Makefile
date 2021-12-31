include default.mk
export

build :
	docker-compose build

push : build
	docker-compose push

up :
	docker-compose up -d

down :
	docker-compose down
