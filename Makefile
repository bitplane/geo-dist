# the things that don't have output files or run every time
.PHONY: help all install test dev coverage clean \
		pre-commit update-pre-commit

# get constants from Python source

SRC_DIR := geo-dist-prep/src/geo_dist_prep/

FILTERED_FILE := $(shell python $(SRC_DIR)geotree/data.py FILTERED_FILE)
TREE_FILE := $(shell python $(SRC_DIR)geotree/data.py TREE_FILE)
NODE_PAIRS := $(shell python $(SRC_DIR)geotree/data.py NODE_PAIRS)
DIST_DATA := $(shell python $(SRC_DIR)geotree/data.py DIST_DATA)
NORMALIZED_DATA := $(shell python $(SRC_DIR)geotree/data.py NORMALIZED_DATA)

GEOTREE_SRC := $(shell find $(SRC_DIR)geotree -type f -name '*.py')

# SOURCE_FILES := $(shell find . -type f -name '*.py')

all: $(NORMALIZED_DATA)

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
$(FILTERED_FILE): .cache/geonames.tsv.gz.done build/data.sh $(SRC_DIR)/data/filter.py
	build/data.sh filter

# 3. Build it into a quad-tree
$(TREE_FILE): $(FILTERED_FILE) $(SRC_DIR)/data/build.py $(GEOTREE_SRC)
	build/data.sh build

# 4. Extract nearby nodes from the tree into pairs
$(NODE_PAIRS): $(TREE_FILE) $(SRC_DIR)/data/extract.py $(GEOTREE_SRC)
	build/data.sh extract

# 5. Add location data using openrouteservice
$(DIST_DATA): $(NODE_PAIRS) $(SRC_DIR)/data/enrich.py
	build/data.sh enrich

# 6. Normalize the data for training
$(NORMALIZED_DATA): $(DIST_DATA) $(SRC_DIR)/data/normalize.py
	build/data.sh normalize

# 7. Train the model


# 8. Start the web service!



help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
