livehtml:
	poetry shell && $(MAKE) -C docs livehtml

html:
	poetry shell && $(MAKE) -C docs html

doc: html

install:
	python3 -m pip install --user .[docs,dev]

build:
	poetry build

test:
	rm -f .coverage coverage.xml
	poetry shell && pytest metamorph

commit: 
	-git add .
	-git commit

push: commit
	git push

pull: commit
	git pull

clean-all: clean
	find source/example/ -type f -name '*.ipynb' | xargs jupyter nbconvert --clear-output --inplace


release: push html
	git tag $(shell git describe --tags --abbrev=0 | perl -lpe 'BEGIN { sub inc { my ($$num) = @_; ++$$num } } s/(\d+\.\d+\.)(\d+)/$$1 . (inc($$2))/eg')
	git push --tags