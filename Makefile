APP=weblog_helper

.PHONY: run
run:
	. ./env/bin/activate && chmod +x ./set-env-vars.sh && . ./set-env-vars.sh && python main.py

.PHONY: test
test:
	. ./env/bin/activate && chmod +x ./set-env-vars.sh && . ./set-env-vars.sh && python test_main.py