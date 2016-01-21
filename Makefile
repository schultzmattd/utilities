#Stole template from here:
#http://www.itnotes.de/docker/development/tools/2014/08/31/speed-up-your-docker-workflow-with-a-makefile/
TAG = 0.1
VERSION = 1

BASENAME = dev-env
IPYTHON_NOTEBOOKS = $(HOME)/ipython_notebooks/
.PHONY: all
all: build

build:
	docker build -f $(BASENAME).dockerfile -t $(BASENAME):$(TAG) ./
#run:
#	docker run -v $(HOME)/.aws:$(HOME)/.aws -v $(HOME):$(HOME) --rm -it $(BASENAME):$(TAG)
shell:
	docker run -v $(HOME)/.aws:$(HOME)/.aws --rm -it $(BASENAME):$(TAG)
ipython:
	docker run --net=host -v $(IPYTHON_NOTEBOOKS):$(IPYTHON_NOTEBOOKS) -v $(HOME)/.aws:$(HOME)/.aws --rm -it $(BASENAME):$(TAG) sh -c '/opt/anaconda2/bin/ipython notebook --ip="*" --port=9000 --no-browser'
	
