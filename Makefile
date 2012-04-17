.PHONY: clean

all: clean test

test:
	python run_tests.py

dist:
	python setup.py publish

clean:
	rm -rf build
	find . -name '*.py[c|o]' -exec rm -f {} +