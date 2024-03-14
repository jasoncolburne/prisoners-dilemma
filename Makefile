venv:
	@python3 -m venv venv

remove-venv:
	@rm -rf venv

dependencies: venv
	@source venv/bin/activate && pip install -r requirements.pip

update: remove-venv venv
	@source venv/bin/activate && pip install -r requirements.thawed && pip freeze > requirements.pip

simulate: dependencies
	@source venv/bin/activate && python main.py ${rounds}
