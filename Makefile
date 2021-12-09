APP=weblog_helper

.PHONY: run
run:
	chmod +x weblog_helper.py && ./weblog_helper.py

.PHONY: test
test:
	chmod +x test_main.py && ./test_main.py
