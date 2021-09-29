APP_NAME = shnootalk_cc_server

.PHONY: help push clean test lint  typechk push

help:
	@echo "Note: Please make sure you are in pipenv shell"
	@echo ""
	@echo "clean"
	@echo "    Remove generated files"
	@echo "test"
	@echo "    Run tests"
	@echo "lint"
	@echo "    Print pylint score"
	@echo "typechk"
	@echo "    Type check source"
	@echo "push"
	@echo "    Build and push docker image to dockerhub"
	@echo ""

clean:
	rm -f -r $(APP_NAME)/__pycache__
	rm -f -r .pytest_cache/
	find . -type d -name  "__pycache__" -exec rm -r {} +
	rm -f -r build/
	rm -f -r dist/

test:
	pytest tests -vv

lint:
	pylint $(APP_NAME) tests --rcfile ./.pylintrc

typechk:
	mypy --package $(APP_NAME) --package tests --namespace-packages --install-types

push:
	docker build --no-cache . -t shnoo28/shnootalk-cloud-compile-server:0.0.7
	docker push shnoo28/shnootalk-cloud-compile-server:0.0.7

rundev:
	python3 -m shnootalk_cc_server