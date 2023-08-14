GIT_REV = $(shell git rev-parse --short HEAD)

setup: .env
	@python3 -m venv .venv
	@. .venv/bin/activate && pip install --upgrade pip pip-tools
	@echo ""
	@echo "-------------------------------------------------------------------"
	@echo "-> Remember to \"source .venv/bin/activate\" and run make build"
	@echo "-> Then run \"make build\""
	@echo "-------------------------------------------------------------------"

stack.env: .env
	@cp .env stack.env

.env:
	@cp .env.example .env

build: requirements.txt requirements-dev.txt
	@pip-sync requirements.txt requirements-dev.txt

requirements.txt: requirements.in
	@pip-compile --resolver=backtracking --generate-hashes requirements.in

requirements-dev.txt: requirements-dev.in
	@pip-compile --resolver=backtracking --generate-hashes requirements-dev.in

clean:
	@rm -rf .venv

run:
	@python -m flask --app app run --host 0.0.0.0 --port 1337 --debug

black:
	@black --check --verbose .

flake8:
	@flake8 --exclude=.venv,**/migrations/* --max-line-length=100

lint: black flake8

audit:
	@pip-audit -r requirements.txt

docker:
	@docker build -t passcheck:$(GIT_REV) -t passcheck:latest .
