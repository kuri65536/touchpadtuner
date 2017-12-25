.PHONY: all test check lint

mypy := venv/bin/mypy
src3 := touchpadtuner.py
src2 := touchpadtuner2.py
path_typeshed := venv/lib/mypytypeshed

all: lint check test
	echo "done."

test: .test2 .test3
.test3: $(src3)
	python3 test.py
	if [ x$$? = x0 ]; then touch $@; fi
.test2: $(src2)
	python test.py
	if [ x$$? = x0 ]; then touch $@; fi

check: .check2 .check3

.check3: $(src3)
	$(mypy) --strict touchpadtuner.py
	if [ x$$? = x0 ]; then touch $@; fi
.check2: $(src2)
	$(mypy) --strict --py2 touchpadtuner2.py
	if [ x$$? = x0 ]; then touch $@; fi

lint: .lint2 .lint3

.lint3: $(src3)
	flake8 touchpadtuner.py
	if [ x$$? = x0 ]; then touch $@; fi
.lint2: $(src2)
	flake8 touchpadtuner2.py
	if [ x$$? = x0 ]; then touch $@; fi

install_typeshed:
	cp typeshed/2/* $(path_typeshed)/stdlib/2
	cp typeshed/3/* $(path_typeshed)/stdlib/3
