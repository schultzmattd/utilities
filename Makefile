#Stole template from here:
#http://www.itnotes.de/docker/development/tools/2014/08/31/speed-up-your-docker-workflow-with-a-makefile/
TAG = 0.1
VERSION = 1

BASENAME = dev-env

.PHONY: all
all: build

build:
	docker build -f $(BASENAME).dockerfile -t $(BASENAME):$(TAG) ./
