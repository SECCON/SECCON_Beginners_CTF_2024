.PHONY: build
build:
	python gen.py > construct.c
	gcc -Wall -Wextra -o construct construct.c

.PHONY: check
check:
	python check_angr.py
