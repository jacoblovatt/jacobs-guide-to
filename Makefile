.DEFAULT_GOAL := help
GUIDE ?= calculus
export GUIDE
.PHONY: help setup doctor preview html pdf public check regression serve
help:
	@echo 'make setup | doctor | preview GUIDE=calculus | html GUIDE=calculus'
	@echo 'make pdf GUIDE=calculus | public | check | regression | serve'
setup:
	bash tools/install-quarto.sh
doctor preview html pdf public serve:
	python3 tools/guides.py $@
check:
	python3 tools/check_site.py
regression:
	python3 tools/check_publication.py
