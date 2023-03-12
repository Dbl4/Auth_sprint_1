WORKDIR = .

lint: 
	black -S -l 79 $(WORKDIR)
	isort $(WORKDIR)
	flake8 --inline-quotes 'double' $(WORKDIR)
	PYTHONPATH=${PYTHONPATH}:${PWD}/$(WORKDIR)
	mypy $(WORKDIR)
