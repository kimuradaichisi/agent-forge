.PHONY: check package

check:
	python3 scripts/validate.py

package: check
	python3 scripts/package.py
