port = 8000
tester_version = 0.7.1
python = python3
npm_bin = $(shell npm bin)
integration_test = $(npm_bin)/take-home-integration-test

$(integration_test):
	npm install --no-save ./assets/c1-code-test-take-home-tester-$(tester_version).tgz

install:
	$(python) -m pip install --user -r requirements.txt
	chmod u+x run.py

test: $(integration_test)
	$(integration_test) \
	features \
	--command "./run.py" \
	--port $(port) \
	-- \
	--tags 'not @skip'

.PHONY: install test