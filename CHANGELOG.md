# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `update-axe` CLI command to update the bundled `axe.min.js` file to the latest version
- Comprehensive test suite with proper organization
  - Unit tests for base module (`test_base.py`)
  - Integration tests for Selenium (`test_axe_selenium.py`)
  - Integration tests for Playwright sync API (`test_axe_sync_playwright.py`)
  - Integration tests for Playwright async API (`test_axe_async_playwright.py`)
- Test markers for filtering tests (`slow`, `unit`, `selenium`, `playwright`, `chromium`, `firefox`, `webkit`)
- `--runslow` pytest option to run slow browser tests
- `--browser` pytest option to run tests for specific browser
- Shared fixtures in `conftest.py` for browser automation
- Tests for `context` and `options` parameters in `axe.run()`
- Tests for `from_file()` class method
- Result structure validation helpers

### Changed
- Updated minimum Python version to 3.12
- Refactored test files to use shared fixtures from `conftest.py`
- Test assertions are now more flexible to accommodate axe-core version changes

### Fixed
- Fixed typo in test name: `test_run_axe_sample_page_chrimium` → `test_run_axe_sample_page_chromium`
- Fixed webkit fixture incorrectly using chromium browser instead of webkit

## [0.1.0] - 2024-XX-XX

### Added
- Initial release of axe-core-python
- Core accessibility testing functionality
- Integration with axe-core JavaScript library
- Support for multiple browser automation frameworks
