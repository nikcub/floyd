VERSION=$(shell python -c "import floyd; print 'v%s' % floyd.get_version()")
DATE=$(shell DATE)
README=./docs/src/README.md

all: clean test docs build deploy dist

test:
	python run_tests.py

docs:
	echo "Buildings docs";

build:
	@@sed -e 's/@VERSION/'"${VERSION}"'/' -e 's/@DATE/'"${DATE}"'/' < ${README} > README.md; \
	echo "Release ${VERSION} ${DATE} built";

deploy:
	git commit -am 'version ${VERSION}'
	git tag ${VERSION}
	git push origin ${VERSION}
	git push origin master

dist:
	python setup.py publish

clean:
	rm -rf build
	find . -name '*.py[c|o]' -exec rm -f {} +
	
.PHONY: clean test dist
