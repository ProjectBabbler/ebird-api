#
# Makefile: Commands to simplify the release process
#
# Usage:
#
#     make clean
#     make test
#     make (patch | minor | major) release
#

# .make.current contains the currenct release.
current := `cat .make.current`
# .make.version contains the next release.
version := `cat .make.version`
# Release date to be added to the changelog .
today := `date +%Y-%m-%d`
# Where the version string can be found.
version_file = ebird/api/__init__.py
# Repository branch which is used for releases
release_branch = master
# Get the public ID for the GPG key from the git config - added previously
gpg_key = `git config --global --get user.signingkey`

# Targets which are not actual files or directories
.PHONY: clean lint patch minor major release test unit acceptance

help : makefile
    # Show all ## comments
	@sed -n 's/^##//p' $<

##
## clean          : Remove all the auto-generated files.
clean:
    # Use the setup plugin, janitor to remove all build products
	python setup.py clean --dist --eggs --pycache
	# remove state files
	rm -f .make.*
	# remove files generated when running acceptance tests
	rm -rf tests/results
	# remove coverage files
	rm -rf coverage
	rm -f .coverage

## lint           : Run flake8 on the API code and tests.
lint:
	flake8 ebird test

.make.current:
    # Extract version number from python code
	grep ^__version__ ${version_file} | cut -d \' -f 2 > $@

## patch          : Bump the release number.
patch: .make.current
	# Bump the patch release number and update the python code
	awk -F. '{$$3+=1; OFS="."; print $$1, $$2, $$3}' .make.current > .make.version
	sed -i "s/__version__ = .*/__version__ = '${version}'/" ${version_file}

## minor          : Bump the minor version number.
minor: .make.current
	# Bump the minor release number and update the python code
	awk -F. '{$$2+=1; OFS="."; print $$1, $$2, 0}' .make.current > .make.version
	sed -i "s/__version__ = .*/__version__ = '${version}'/" ${version_file}

## major          : Bump the major version number.
major: .make.current
	# Bump the major release number and update the python code
	awk -F. '{$$1+=1; OFS="."; print $$1, 0, 0}' .make.current > .make.version
	sed -i "s/__version__ = .*/__version__ = '${version}'/" ${version_file}

.make.version:
    # dummy target to silence an "unresolved prerequisit" warning for the
    # CHANGLOG.md target. It's not need for the makefile to work.
	[ -f .make.version ]

CHANGELOG.md: .make.version
    # Update latest (unreleased) entry to add the release number and a date stamp
	sed -i "s/## \[Unreleased\]/## [${version}] - ${today}/" $@
	# Update the list of releass at the end of the file:
	# 1. Duplicate the unreleased line, add delimeters to differnetiate the second
	# 2. Update the version number for the difference to the current HEAD
	# 3. Replace "unreleased' on the second line with the release number
	# 4. Replace "HEAD" on the second line with the release number
	sed -i $@ \
	       -e "s/\(\[Unreleased\].*\)/\1\n-\1-/" \
		   -e "s/${current}...HEAD/${version}...HEAD/" \
		   -e "s/-\[Unreleased\]/[${version}]/" \
		   -e "s/HEAD-/${version}/"

## release        : Build and upload a new release to PyPi.
release: lint CHANGELOG.md
    # Add the updated __init__.py and CHANGELOG.md
	git add @^ ${version_file}
	# Sign the comment
	git commit -S -m "Updated for release ${version}"
	git push origin ${release_branch}
    # Add the version number as a tag and sign it
	git tag -s ${version} -m ${version}
	git push --tags
    # Build the source and binary files
	python setup.py sdist bdist_wheel
    # Upload to PyPI
	twine upload --sign --identity ${gpg_key} dist/*

unit:
    # The test runner in setup.py is configured to run the unit tests.
	python setup.py test

acceptance:
    # Acceptance tests are regular python scripts
	python -m 	tests.acceptance.client

## test           : Run the unit and acceptance tests.
test: unit acceptance

## coverage       : Generate a coverage report from the tests.
coverage:
	# Run coverage for the unit tests
	coverage run setup.py test
	# Run coverage for acceptance tests and add it to the unit test coverage
	coverage run --append -m tests.acceptance.client
	# Show a quick summary
	coverage report
	# Generate a full report in HTML
	coverage html

##
