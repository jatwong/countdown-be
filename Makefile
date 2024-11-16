.PHONY: pipinstall

install-local:
	@pip install -r requirements.txt

pip-install:
	@pip install --upgrade $(package)
	@pip freeze > requirements.txt
	@echo "requirements.txt has been updated."
