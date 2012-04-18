VERSION=$(shell python -c "import floyd; print floyd.get_version()")
DATE=$(shell DATE)
README=./docs/src/README.md

all: clean test docs build deploy dist

test:
	python run_tests.py

docs:
	echo "Buildings docs";

build:
	@@sed -e 's/@VERSION/'"v${VERSION}"'/' -e 's/@DATE/'"${DATE}"'/' < ${README} > README.md; \
	echo "Release v${VERSION} ${DATE} built";

deploy:
	git commit -am 'version ${VERSION}'
	git tag  ${VERSION}
	git push origin

dist:
	python setup.py publish

clean:
	rm -rf build
	find . -name '*.py[c|o]' -exec rm -f {} +
	
.PHONY: clean test dist
