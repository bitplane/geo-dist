# the things that don't have output files or run every time
.PHONY: help all install test dev coverage clean \
		pre-commit update-pre-commit

GEOTREE_SRC := $(shell find geo-dist-prep/src/geo_dist_prep/geotree -type f -name '*.py')

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



#--- Targets for processing steps here ---#



# 1. download the geonames file
.cache/geonames.tsv.gz.done: build/download-geonames.sh
	build/download-geonames.sh

# 2. filter out names we don't want
.cache/filtered-geonames.tsv: .cache/geonames.tsv.gz.done build/filter-geonames.sh geo-dist-prep/src/geo_dist_prep/filter_geonames.py
	build/filter-geonames.sh

# 3. Build it into a quad-tree
.cache/tree.pkl: .cache/filtered-geonames.tsv build/build-tree.sh geo-dist-prep/src/geo_dist_prep/build_tree.py $(GEOTREE_SRC)
	build/build-tree.sh

# 4. Use the tree to find nearby nodes
.cache/pairs.tsv: .cache/tree.pkl build/create-pairs.sh geo-dist-prep/src/geo_dist_prep/create_pairs.py $(GEOTREE_SRC)
	build/create-pairs.sh

# 5. Create the training data using the openrouteservice
.cache/data.tsv: .cache/pairs.tsv build/create-data.sh geo-dist-prep/src/geo_dist_prep/create_data.py
	build/create-data.sh

# 6. Train the model

# 7. Test the model

# 8. Start the web service!



help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
