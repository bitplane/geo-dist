# the things that don't have output files or run every time
.PHONY: help all install test dev coverage clean \
		pre-commit update-pre-commit

# SOURCE_FILES := $(shell find . -type f -name '*.py')

all: .cache/location-tree.pkl

install: .venv/.installed  ## installs the venv and the project packages

dev: .venv/.installed pre-commit  ## prepare local repo and venv for dev

test: .venv/.installed  ## run the project's tests
	build/test.sh

coverage: .venv/.installed build/coverage.sh  ## build the html coverage report
	build/coverage.sh

clean:  ## delete caches and the venv
	build/clean.sh

pre-commit: .git/hooks/pre-commit  ## install pre-commit into the git repo

update-pre-commit: build/update-pre-commit.sh  ## autoupdate pre-commit
	build/update-pre-commit.sh

# Caching doesn't work if we depend on PHONY targets

.venv/.installed: */pyproject.toml .venv/bin/activate build/install.sh
	build/install.sh

.venv/bin/activate:
	build/venv.sh

.git/hooks/pre-commit: build/install-pre-commit.sh
	build/install-pre-commit.sh

.cache/geonames.tsv.gz.done: build/download-geonames.sh
	build/download-geonames.sh

.cache/filtered-geonames.tsv: .cache/geonames.tsv.gz.done build/filter-geonames.sh geo-dist-prep/src/geo_dist_prep/filter_geonames.py
	build/filter-geonames.sh

GEOTREE_FILES := $(find geo-dist-prep/src/geo_dist_prep/geonode -type f -name '*.py')
.cache/location-tree.pkl: .cache/filtered-geonames.tsv build/build-tree.sh geo-dist-prep/src/geo_dist_prep/node_tree.py $(GEOTREE_FILES)
	build/build-tree.sh

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
