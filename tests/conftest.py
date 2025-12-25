"""
Pytest configuration and shared fixtures for axe-core-python tests.

This module provides:
- Shared fixtures for browser automation (Selenium, Playwright sync/async)
- Custom pytest markers (slow, selenium, playwright)
- Hook implementations for test filtering and organization
"""

from pathlib import Path

import pytest
import pytest_asyncio

# Test page path
TEST_FILE = "test_page.html"
TEST_FILE_PATH = Path(__file__).parent.absolute() / TEST_FILE
TEST_FILE_URL = f"file://{TEST_FILE_PATH}"


def pytest_addoption(parser):
    """Add custom command-line options."""
    parser.addoption(
        "--runslow",
        action="store_true",
        default=False,
        help="run slow tests (browser tests)",
    )
    parser.addoption(
        "--browser",
        action="store",
        default="all",
        choices=["all", "chrome", "firefox", "chromium", "webkit"],
        help="run tests only for specific browser",
    )


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "slow: mark test as slow to run (requires --runslow)")
    config.addinivalue_line("markers", "selenium: mark test as selenium-based")
    config.addinivalue_line("markers", "playwright: mark test as playwright-based")
    config.addinivalue_line("markers", "unit: mark test as unit test (fast)")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "chrome: mark test for Chrome browser")
    config.addinivalue_line("markers", "firefox: mark test for Firefox browser")
    config.addinivalue_line("markers", "chromium: mark test for Chromium browser")
    config.addinivalue_line("markers", "webkit: mark test for WebKit browser")


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on command-line options."""
    # Handle --runslow option
    if not config.getoption("--runslow"):
        skip_slow = pytest.mark.skip(reason="need --runslow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)

    # Handle --browser option
    browser = config.getoption("--browser")
    if browser != "all":
        browser_markers = {"chrome", "firefox", "chromium", "webkit"}
        skip_browser = pytest.mark.skip(reason=f"test not for {browser} browser")
        for item in items:
            item_markers = {m.name for m in item.iter_markers()}
            # If test has browser markers but not the selected one, skip it
            if item_markers & browser_markers and browser not in item_markers:
                item.add_marker(skip_browser)


@pytest.fixture(scope="session")
def test_page_path() -> Path:
    """Return the path to the test HTML page."""
    return TEST_FILE_PATH


@pytest.fixture(scope="session")
def test_page_url() -> str:
    """Return the file URL to the test HTML page."""
    return TEST_FILE_URL


# ============================================================================
# Selenium Fixtures
# ============================================================================


@pytest.fixture
def firefox_webdriver(test_page_url):
    """Create a Firefox WebDriver instance."""
    from selenium import webdriver

    driver = webdriver.Firefox()
    driver.get(test_page_url)
    yield driver
    driver.quit()


@pytest.fixture
def chrome_webdriver(test_page_url):
    """Create a Chrome WebDriver instance."""
    from selenium import webdriver

    driver = webdriver.Chrome()
    driver.get(test_page_url)
    yield driver
    driver.quit()


# ============================================================================
# Playwright Sync Fixtures
# ============================================================================


@pytest.fixture
def sync_playwright_firefox(test_page_url):
    """Create a sync Playwright Firefox page."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        page.goto(test_page_url)
        yield page
        browser.close()


@pytest.fixture
def sync_playwright_chromium(test_page_url):
    """Create a sync Playwright Chromium page."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(test_page_url)
        yield page
        browser.close()


@pytest.fixture
def sync_playwright_webkit(test_page_url):
    """Create a sync Playwright WebKit page."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.webkit.launch()
        page = browser.new_page()
        page.goto(test_page_url)
        yield page
        browser.close()


# ============================================================================
# Playwright Async Fixtures
# ============================================================================


@pytest_asyncio.fixture
async def async_playwright_firefox(test_page_url):
    """Create an async Playwright Firefox page."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await page.goto(test_page_url)
        yield page
        await browser.close()


@pytest_asyncio.fixture
async def async_playwright_chromium(test_page_url):
    """Create an async Playwright Chromium page."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(test_page_url)
        yield page
        await browser.close()


@pytest_asyncio.fixture
async def async_playwright_webkit(test_page_url):
    """Create an async Playwright WebKit page."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.webkit.launch()
        page = await browser.new_page()
        await page.goto(test_page_url)
        yield page
        await browser.close()


# ============================================================================
# Helper Functions for Test Result Validation
# ============================================================================


def validate_axe_result_structure(result: dict) -> None:
    """Validate that axe result has the expected structure."""
    required_keys = {"inapplicable", "incomplete", "passes", "violations"}
    assert required_keys <= set(result.keys()), (
        f"Missing keys: {required_keys - set(result.keys())}"
    )

    # Each category should be a list
    for key in required_keys:
        assert isinstance(result[key], list), f"{key} should be a list"


def validate_violation_structure(violation: dict) -> None:
    """Validate that a violation has the expected structure."""
    required_keys = {"id", "impact", "description", "help", "helpUrl", "nodes", "tags"}
    assert required_keys <= set(violation.keys()), (
        f"Missing keys: {required_keys - set(violation.keys())}"
    )

    # Nodes should be a list
    assert isinstance(violation["nodes"], list), "nodes should be a list"

    # Tags should be a list
    assert isinstance(violation["tags"], list), "tags should be a list"


def validate_node_structure(node: dict) -> None:
    """Validate that a node has the expected structure."""
    required_keys = {"html", "target"}
    assert required_keys <= set(node.keys()), f"Missing keys: {required_keys - set(node.keys())}"

    # Target should be a list of selectors
    assert isinstance(node["target"], list), "target should be a list"
