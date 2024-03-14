venv:
	@python3 -m venv venv

remove-venv:
	@rm -rf venv

dependencies: venv
	@source venv/bin/activate && pip install -r requirements.pip

update: remove-venv venv
	@source venv/bin/activate && pip install -r requirements.thawed && pip freeze > requirements.pip

dev-dependencies: venv
	@source venv/bin/activate && pip install black && pip install pylint

black: dev-dependencies
	@source venv/bin/activate && black -t py312 --check .

format: dev-dependencies
	@source venv/bin/activate && black -t py312 .

pylint: dev-dependencies
	@source venv/bin/activate && pylint $(shell git ls-files '*.py')

preflight: black pylint

simulate: dependencies
	@source venv/bin/activate && python main.py ${rounds}
