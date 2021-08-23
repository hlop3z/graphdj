.PHONY: all clean build upload

all: clean build

clean:
	@echo "Cleaning up..."
	rm -rf dist
	@echo ""

build:
	@echo "Building package..."
	python -m build

upload:
	@echo "Uploading with twine..."
	python -m twine upload dist/*