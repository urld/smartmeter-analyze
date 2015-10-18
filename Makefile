# Original source: https://github.com/mfellner/DockerFlaskExample

CONTAINER_IMAGE_NAME = smartmeter-util
DOCKER_ERROR := $(shell docker info 2>&1 | grep -i 'cannot connect')
OS := $(shell uname)

PKG_NAME := $(shell python setup.py --fullname)

all: boot2docker clean build run

.PHONY: boot2docker
boot2docker:
ifneq ($(DOCKER_ERROR),)
ifeq ($(OS),Darwin)
		@boot2docker start
		@echo "boot2docker started"
		@$(boot2docker shellinit)
else
		@echo $(DOCKER_ERROR)
endif
else
		@echo "docker is running"
endif


.PHONY: stop
stop:
		@if [[ -f .container ]]; \
		then \
			echo "stopping docker container..."; \
			cat .container | xargs docker stop; \
		fi;
		@if [[ -f .container ]]; \
		then \
			echo "deleting docker container..."; \
			cat .container | xargs docker rm; \
			rm -f .container; \
		fi;


.PHONY: clean
clean:
		rm -rf dist/


.PHONY: clean-all
clean-all: clean
		@echo "removing old docker images"
		@docker images --no-trunc | grep '$(CONTAINER_IMAGE_NAME)' | awk '{print $3}' | xargs docker rmi


# build python sdist:
dist/smartmeter-analyze:
		python setup.py sdist
		tar -xf dist/$(PKG_NAME).tar.gz -C dist/
		mv dist/$(PKG_NAME) dist/smartmeter-analyze
		

.PHONY: build
build: dist/smartmeter-analyze
		@echo "building image..."
		docker build -t $(CONTAINER_IMAGE_NAME) .


.container: build
		@echo "creating container..."
		@CONTAINER_ID="$(shell docker create -p 80:80 -p 443:443 $(CONTAINER_IMAGE_NAME))"; \
		echo $$CONTAINER_ID >> .container; \
		echo $$CONTAINER_ID


.PHONY: run
run: .container
		@echo "starting container..."
		@tail -n 1 .container | xargs docker start


.PHONY: test
test:
ifeq ($(OS),Darwin)
		curl -IL --insecure https://$(shell boot2docker ip)
else
		curl -IL --insecure https://localhost
endif


.PHONY: attach
attach:
		docker exec -it $(shell tail -n 1 .container) /bin/bash

