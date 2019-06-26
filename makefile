#
# Makefile: Commands to simplify the release process
#
# Usage:
#
#     make clean
#     make test
#     make (patch | minor | major) release
#

current := `cat .make.current`
version := `cat .make.version`
today := `date +%Y-%m-%d`

version_file = ebird/api/__init__.py

release_branch = master
gpg_key = `git config --global --get user.signingkey`

.PHONY: clean patch minor major release test unit acceptance

clean:
	python setup.py clean --dist --eggs --pycache
	# remove state files
	rm -f .make.*
	# remove coverage files
	rm -rf coverage
	rm -f .coverage

.make.current:
    # Extract version number from python code
	grep ^__version__ ${version_file} | cut -d \' -f 2 > $@

patch: .make.current
	# Bump the patch release number and update the python code
	awk -F. '{$$3+=1; OFS="."; print $$1, $$2, $$3}' .make.current > .make.version
	sed -i "s/__version__ = .*/__version__ = '${version}'/" ${version_file}

minor: .make.current
	# Bump the minor release number and update the python code
	awk -F. '{$$2+=1; OFS="."; print $$1, $$2, 0}' .make.current > .make.version
	sed -i "s/__version__ = .*/__version__ = '${version}'/" ${version_file}

major: .make.current
	# Bump the major release number and update the python code
	awk -F. '{$$1+=1; OFS="."; print $$1, 0, 0}' .make.current > .make.version
	sed -i "s/__version__ = .*/__version__ = '${version}'/" ${version_file}

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

release: CHANGELOG.md
	git add @^ ${version_file}
	git commit -S -m "Updated for release ${version}"
	git push origin ${release_branch}

	git tag -s ${version} -m ${version}
	git push --tags

	python setup.py sdist bdist_wheel

	twine upload --sign --identity ${gpg_key} dist/*

unit:
	python setup.py test

acceptance:
	python -m tests.acceptance.client

test: unit acceptance

coverage:
	# Run coverage for the unit tests
	coverage run setup.py test
	# Run coverage for acceptance tests and add it to the unit test coverage
	coverage run --append -m tests.acceptance.client
	# Show a quick summary
	coverage report
	# Generate a full report in HTML
	coverage html
