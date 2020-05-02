# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- check book loaned status before loaning
- make sure tabled don't leave page when shrinking width
- make tests for user data separation


## 2020-05-02
### Fixed
- Error in loaning books

### Changed
- login made thorugh template instead of backend to avoid CSRF issues
- improvements to tests
- disable DEL method for LoansViewSet
- reloading the page no longer breaks authentication

### Added
- Login panel
- implemented logout
- implemented per-user queryset for models viewsets


## 2020-03-28
### Added
- user name link to home view in the banner
- new tests for JwtTestCase
- authentication to unit tests

### Changed
- structure of index template

## 2020-03-22
### Added
- make template that checks for authentication, and redirects accordingly

### Changed

### Removed

### Fixed






