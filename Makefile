# Original source: https://github.com/mfellner/DockerFlaskExample

CONTAINER_IMAGE_NAME = smartmeter-util
DOCKER_ERROR := $(shell docker info 2>&1 | grep -i 'cannot connect')
OS := $(shell uname)

PKG_NAME := $(shell python setup.py --fullname)

all: boot2docker clean build run
		@echo "done"


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


.PHONY: clean
clean:
		@if [[ -f .containers ]]; \
		then \
			echo "stopping docker container"; \
			cat .containers | xargs docker stop; \
			cat .containers | xargs docker rm; \
			rm -f .containers; \
		fi;
		@rm -rf dist/

.PHONY: clean-all
clean-all: clean
		@echo "removing old docker images"
		@docker images --no-trunc | grep '$(CONTAINER_IMAGE_NAME)' | awk '{print $3}' | xargs docker rmi


.PHONY: build
build: clean
		@python setup.py sdist
		@tar -xf dist/$(PKG_NAME).tar.gz -C dist/
		@mv dist/$(PKG_NAME) dist/smartmeter-analyze
		@echo "building image..."
		@docker build -t $(CONTAINER_IMAGE_NAME) .
		@rm -rf dist/smartmeter-analyze


.PHONY: run
run: build
		@echo "starting container..."
		@CONTAINER_ID="$(shell docker run -p 80:5000 -dti $(CONTAINER_IMAGE_NAME))"; \
		echo $$CONTAINER_ID >> .containers;


.PHONY: test
test:
ifeq ($(OS),Darwin)
		@curl -IL $(shell boot2docker ip):80
else
		@curl -IL localhost:80
endif
