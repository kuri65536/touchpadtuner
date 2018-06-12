.PHONY: all test check lint launch

mypy := venv/bin/mypy
src2 := touchpadtuner2.py
test3 := test.py
path_typeshed := venv/lib/mypytypeshed
flake8_3 := flake8

all: lint check test
	echo "done."

launch:
	python $(src2)

test: .test3
.test3: $(src3) $(test3)
	python3 test.py
	if [ x$$? = x0 ]; then touch $@; fi

check: .check2

.check2: $(src2)
	$(mypy) --strict --py2 touchpadtuner2.py
	if [ x$$? = x0 ]; then touch $@; fi

lint: .lint2 .lint3

.lint2: $(src2)
	$(flake8_3) touchpadtuner2.py
	if [ x$$? = x0 ]; then touch $@; fi

install_typeshed:
	cp typeshed/2/* $(path_typeshed)/stdlib/2
	cp typeshed/3/* $(path_typeshed)/stdlib/3
