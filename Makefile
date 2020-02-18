# --------------------------------------------------------------------
# There should be no need to change this
# --------------------------------------------------------------------

# SERVICE_TARGET := pyshipper

# If you see pwd_unknown showing up, this is why. Re-calibrate your system.
PWD ?= pwd_unknown

# retrieve NAME from /variables file
MODULE_NAME = \
	$(shell awk -F= '/^NAME\ ?=/{gsub(/\47|"/, "", $$NF);print $$NF;exit}' variables)
MODULE_VERSION = \
	$(shell awk -F' = ' '$1 == "__version__" {gsub(/"/, "", $2); print $2}' module/main/release.py)

# export such that its passed to shell functions for Docker to pick up.
export MODULE_NAME
export MODULE_VERSION

.PHONY: fork
FILES = \
	module files Makefile setup.py MANIFEST.in variables .gitignore .pylintrc
DEST ?= $(dest)
fork:
ifeq ($(DEST),)
	@echo 'MISSING "dest=" PARAMETER'
	@echo 'RUN: make fork dest=$${DIRECTORY}'
else
	@# copy when either directory does not exist, or is empty
	@# skip if a non-empty directory exist
	@# Note this excludes README.md and LICENSE -- you own your own project ;)
	@(([ ! -d "$(DEST)" ] || find "$(DEST)" -prune -type d -empty |grep -q .) \
	  && mkdir -p "$(DEST)" \
      && cp -R $(FILES) "$(DEST)/" \
	  && touch $(DEST)/README.md \
      || echo "SKIPPING FORK, WON'T OVERWRITE EXISTING DIRECTORY")
endif

.PHONY: module
module:
	@# ensure there is a symlink from MODULE_NAME to module directory
	@# then run regular setup.py to build the module
	find ./ -type l -maxdepth 1 |xargs rm -f \
		&& ln -sf module "$(MODULE_NAME)" \
		&& python3 setup.py sdist

.PHONY: pylint
pylint:
	cd ./module \
		&& pylint --output-format=text --ignore-imports=yes * -f parseable

.PHONY: upload
upload:
	echo $(MODULE_VERSION)
	twine upload --config-file .pypirc ./dist/$(MODULE_NAME)-$(MODULE_VERSION)*

.PHONY: clean
clean:
	rm -rf ./build ./dist ./*.egg-info \
		&& find ./ -type l -maxdepth 1 |xargs rm -f \
		&& find ./$(MODULE) -type d -name '__pycache__' |xargs rm -rf
