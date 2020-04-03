# venvctl Change Log

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.10] - 2020-04-03

### Added - 2020-04-03

- Security module now availabe exposing bandit both programmatically and for the CLI.

### Changed - 2020-04-03

(nothing)

### Removed - 2020-04-03

(nothing)

### Fixed - 2020-04-03

(nothing)

## [1.3.9] - 2020-03-30

### Added - 2020-03-30

- Security module (not yet available both programmatically and for the CLI).

### Changed - 2020-03-30

- Now the venvs will be created even if they already exist (support for regeneration or update).

### Removed - 2020-03-30

- removed hardcoded references to python3, allowing to correctly ship virtual environments both for Python 2.x and 3.x

### Fixed - 2020-03-30

- bandit B110:try_except_pass in the CLI module, version handler.

## [1.3.8] - 2020-03-28

### Added - 2020-03-28

(nothing)

### Changed - 2020-03-28

(nothing)

### Removed - 2020-03-28

(nothing)

### Fixed - 2020-03-28

- Improved README with better documentation;
- Aligned README dependencies description to the current versions.

[Unreleased]: https://gitlab.com/hyperd/venvctl/-/compare/v1.3.10...master
[1.3.10]: https://gitlab.com/hyperd/venvctl/-/compare/v1.3.9...v1.3.10
[1.3.9]: https://gitlab.com/hyperd/venvctl/-/compare/v1.3.8...v1.3.9
[1.3.8]: https://gitlab.com/hyperd/venvctl/-/compare/v1.3.7...v1.3.8
