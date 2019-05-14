# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/).
This project adheres to [PEP440](https://www.python.org/dev/peps/pep-0440/)
and by implication, [Semantic Versioning](http://semver.org/).

## [2.1.1] - 2019-05-145
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

[Unreleased]: https://github.com/ProjectBabbler/ebird-api/compare/2.1.1...HEAD
[2.1.1]: https://github.com/ProjectBabbler/ebird-api/compare/2.0.1...2.1.1
[2.1.0]: https://github.com/ProjectBabbler/ebird-api/compare/2.0.0...2.1.0
[2.0.0]: https://github.com/ProjectBabbler/ebird-api/compare/1.0.2...2.0.0
[1.0.2]: https://github.com/ProjectBabbler/ebird-api/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/ProjectBabbler/ebird-api/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/ProjectBabbler/ebird-api/compare/0.2.0...1.0.0
[0.2.0]: https://github.com/ProjectBabbler/ebird-api/compare/0.1.1...0.2.0
[0.1.1]: https://github.com/ProjectBabbler/ebird-api/compare/0.1.0...0.1.1
