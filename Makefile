

doctest:  		##@Test perform doctests, add ./docrender after big refactor
	python -m pytest --doctest-modules dashtable


pytest:
	python -m pytest \
		./tests/test.py \
		./tests/test_in_out.py 


test: doctest pytest


amend:
	git commit --amend


prof:
	LINE_PROFILE=1 python examples/just-data2rst-enhanced.py
