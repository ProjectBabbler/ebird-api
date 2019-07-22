# Change Log
All notable changes to this project will be documented in this file.
Only changes for the API functions are described here. Changes made 
to the internals and developing the package are not included. Check 
the git log for details.

The format is based on [Keep a Changelog](http://keepachangelog.com/).
This project adheres to [PEP440](https://www.python.org/dev/peps/pep-0440/)
and by implication, [Semantic Versioning](http://semver.org/).

## Unreleased
### Changed
- Update the functions for fetching observations to use the sppLocale 
  query parameter to match the recent changes made in the eBird API.

## [3.0.3] - 2019-07-16
### Changed
- When fetching observations, the list of area may only contain 10 items.
  Previously more than 10 were allowed but this was a bug and was fixed to 
  limit the load on the server. 

## [3.0.2] - 2019-06-22
### Changed
- Updated the validation check for region codes so it supports ISO 3166-2. 
- Disabled the validation check that limited the number of areas to 10 as 
  the eBird API does not currently enforce this.

## [3.0.1] - 2019-06-15
### Added 
- Added the full list of locales support by eBird (but not necessarily by the API).
- Added a convenience function for saving downloaded records to a file.
### Changed
- Validating the locale now uses the list supported by eBird.

## [3.0.0] - 2019-06-06
### Added 
- Rewritten to support eBird API 2.0

## [2.1.1] - 2019-05-14
### Changed
- Scripts module is now included in the wheel package.

## [2.1.0] - 2017-08-20
### Changed
- Improved the documentation in the README.
- Project now uses the MIT license.

### Added 
- Added scripts so each API call can be made on the command line.

## [2.0.0] - 2017-02-27
### Changed 
- Moved all the functions into the 'api' module and changed the top-level
'ebird' module to be namespaced (PEP420).

## [1.0.2] - 2017-02-23
### Changed 
- Corrected version number in python.

## [1.0.1] - 2017-02-21
### Added 
- Updated docstrings to report exceptions raised.

## [1.0.0] - 2017-02-21
### Added 
- Added function for Google Gadgets showing recent observations.
- Added function for fetching lists of species.
- Added function for fetching nearby hotspots.
- Added function for fetching lists of hotspots for a region.
### Changed
- Renamed list_locations() to list_regions() and find_locations() to 
find_regions() as "locations" refer to specific sites in the functions 
that fetch observations.

## [0.2.0] - 2017-02-18
### Added
- Functions for fetching locations from the eBird API.
### Changed
- Updated setup.py project description and list of languages supported.

## [0.1.1] - 2017-02-14
### Changed
- Coordinates are rounded to 2 decimal places and converted to strings to
avoid any issues with representation.

## [0.1.0] - 2017-02-13
### Added
- Core functions for accessing end-points for fetching observations.

[Unreleased]: https://github.com/ProjectBabbler/ebird-api/compare/3.0.4...HEAD
[3.0.4]: https://github.com/ProjectBabbler/ebird-api/compare/3.0.3...3.0.4
[3.0.3]: https://github.com/ProjectBabbler/ebird-api/compare/3.0.3...3.0.3
[3.0.3]: https://github.com/ProjectBabbler/ebird-api/compare/3.0.2...3.0.3
[3.0.2]: https://github.com/ProjectBabbler/ebird-api/compare/3.0.1...3.0.2
[3.0.1]: https://github.com/ProjectBabbler/ebird-api/compare/3.0.0...3.0.1
[2.1.1]: https://github.com/ProjectBabbler/ebird-api/compare/2.0.1...2.1.1
[2.1.0]: https://github.com/ProjectBabbler/ebird-api/compare/2.0.0...2.1.0
[2.0.0]: https://github.com/ProjectBabbler/ebird-api/compare/1.0.2...2.0.0
[1.0.2]: https://github.com/ProjectBabbler/ebird-api/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/ProjectBabbler/ebird-api/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/ProjectBabbler/ebird-api/compare/0.2.0...1.0.0
[0.2.0]: https://github.com/ProjectBabbler/ebird-api/compare/0.1.1...0.2.0
[0.1.1]: https://github.com/ProjectBabbler/ebird-api/compare/0.1.0...0.1.1
