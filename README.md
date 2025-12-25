    # axe-core-python
    
![PyPI](https://img.shields.io/pypi/v/axe-core-python) 
![PyPI - License](https://img.shields.io/pypi/l/axe-core-python) 
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/axe-core-python)
![PyPI - Downloads](https://img.shields.io/pypi/dm/axe-core-python) 


Automated web accessibility testing using [axe-core](https://github.com/dequelabs/axe-core) engine.

## Documentation

- [Full documentation](https://ruslan-rv-ua.github.io/axe-core-python/).

## Requirements

- Python >= 3.12
- [selenium](https://www.selenium.dev) >= 4.4.0 
or [playwright](https://github.com/microsoft/playwright-python) >= 1.25.0

## Installation

```console
pip install -U axe-core-python
```

## Usage

```python
from playwright.sync_api import sync_playwright
from axe_core_python.sync_playwright import Axe

axe = Axe()

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.google.com")
    result = axe.run(page)
    browser.close()

violations = result['violations']
print(f"{len(violations)} violations found.")
```

For more examples see [documentation](https://ruslan-rv-ua.github.io/axe-core-python/).

## CLI Commands

### update-axe

Update the bundled `axe.min.js` file to the latest version:

```console
update-axe
```

This command downloads the latest version of axe-core from GitHub releases and updates the file `src/axe_core_python/axe.min.js`.

## Development

### Running Tests

```bash
# Install dependencies
uv sync

# Run fast unit tests (no browser required)
uv run pytest

# Run all tests including slow browser tests
uv run pytest --runslow

# Run tests for specific browser
uv run pytest --runslow -m chromium
uv run pytest --runslow -m firefox

# Run with coverage
uv run pytest --cov=axe_core_python --cov-report=html
```

### Test Markers

- `unit` — Fast unit tests without browsers
- `slow` — Slow tests requiring `--runslow` flag
- `selenium` — Selenium WebDriver tests
- `playwright` — Playwright tests
- `chrome`, `firefox`, `chromium`, `webkit` — Browser-specific tests

## License

MIT