VERSION=$(shell python -c "import floyd; print 'v%s' % floyd.get_version()")
STATUS=$(shell python -c "import floyd; print floyd.get_status()")
DATE=$(shell DATE)
README=./docs/src/README.md

all: clean test docs build deploy dist

test:
	python run_tests.py

docs:
	echo "Buildings docs";

build:
	@@sed -e 's/@VERSION/'"${VERSION}"'/' -e 's/@DATE/'"${DATE}"'/' -e 's/@STATUS/'"${STATUS}"'/' < ${README} > README.md; 
	@@echo "\n[![Build Status](https://secure.travis-ci.org/nikcub/floyd.png)](http://travis-ci.org/nikcub/floyd)\n" >> README.md;
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
