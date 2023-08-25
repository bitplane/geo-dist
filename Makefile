# the things that don't have output files or run every time
.PHONY: help all install test dev coverage clean \
		pre-commit update-pre-commit

GEOTREE_SRC := $(find geo-dist-prep/src/geo_dist_prep/geonode -type f -name '*.py')

# SOURCE_FILES := $(shell find . -type f -name '*.py')

all: .cache/data.tsv

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

.cache/tree.pkl: .cache/filtered-geonames.tsv build/build-tree.sh geo-dist-prep/src/geo_dist_prep/build_tree.py $(GEOTREE_SRC)
	build/build-tree.sh

.cache/pairs.tsv: .cache/tree.pkl build/create-pairs.sh geo-dist-prep/src/geo_dist_prep/create_pairs.py $(GEOTREE_SRC)
	build/create-pairs.sh

.cache/data.tsv: .cache/pairs.tsv build/create-data.sh geo-dist-prep/src/geo_dist_prep/create_data.py
	build/create-data.sh


help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
