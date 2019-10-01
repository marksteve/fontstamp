.PHONY: deps
deps: venv/bin/pip-sync requirements.txt
	venv/bin/pip-sync
venv:
	python3 -m venv venv
venv/bin/pip-compile venv/bin/pip-sync: venv
	venv/bin/pip install pip-tools
requirements.txt: requirements.in
	venv/bin/pip-compile \
	--no-index \
	--no-emit-trusted-host \
	requirements.in > requirements.txt