"""
Selenium integration tests for axe-core-python.

These tests run axe-core accessibility checks using Selenium WebDriver.
They are marked as slow because they launch real browsers.

Run with: pytest --runslow -m selenium
"""

import pytest

from axe_core_python.selenium import Axe

from .conftest import (
    validate_axe_result_structure,
    validate_node_structure,
    validate_violation_structure,
)


class TestSeleniumFirefox:
    """Selenium tests using Firefox browser."""

    @pytest.mark.slow
    @pytest.mark.selenium
    @pytest.mark.firefox
    def test_run_axe_basic(self, firefox_webdriver):
        """Run axe against sample page and verify basic result structure."""
        axe = Axe()
        result = axe.run(webdriver=firefox_webdriver)

        validate_axe_result_structure(result)

    @pytest.mark.slow
    @pytest.mark.selenium
    @pytest.mark.firefox
    def test_run_axe_expected_counts(self, firefox_webdriver):
        """Run axe against sample page and verify expected violation counts."""
        axe = Axe()
        result = axe.run(webdriver=firefox_webdriver)

        # Counts may vary slightly between axe-core versions
        assert len(result["inapplicable"]) >= 70, "Should have many inapplicable rules"
        assert len(result["incomplete"]) >= 0, "Incomplete can be 0 or more"
        assert len(result["passes"]) >= 5, "Should have some passing rules"
        assert len(result["violations"]) >= 8, "Test page should have violations"

    @pytest.mark.slow
    @pytest.mark.selenium
    @pytest.mark.firefox
    def test_run_axe_violations_structure(self, firefox_webdriver):
        """Test that violations have the expected structure."""
        axe = Axe()
        result = axe.run(webdriver=firefox_webdriver)

        assert len(result["violations"]) > 0, "Test page should have violations"

        for violation in result["violations"]:
            validate_violation_structure(violation)
            for node in violation["nodes"]:
                validate_node_structure(node)

    @pytest.mark.slow
    @pytest.mark.selenium
    @pytest.mark.firefox
    def test_run_axe_with_context_string(self, firefox_webdriver):
        """Test running axe with context as string selector."""
        axe = Axe()
        result = axe.run(webdriver=firefox_webdriver, context="body")

        validate_axe_result_structure(result)

    @pytest.mark.slow
    @pytest.mark.selenium
    @pytest.mark.firefox
    def test_run_axe_with_context_dict(self, firefox_webdriver):
        """Test running axe with context as dict with include/exclude."""
        axe = Axe()
        result = axe.run(webdriver=firefox_webdriver, context={"include": [["form"]]})

        validate_axe_result_structure(result)
        # Should still find violations in the form
        assert len(result["violations"]) > 0

    @pytest.mark.slow
    @pytest.mark.selenium
    @pytest.mark.firefox
    def test_run_axe_with_options_run_only(self, firefox_webdriver):
        """Test running axe with options to run only specific rules."""
        axe = Axe()
        result = axe.run(webdriver=firefox_webdriver, options={"runOnly": ["label"]})

        validate_axe_result_structure(result)
        # With runOnly, we should have fewer checks
        assert len(result["violations"]) <= 9

    @pytest.mark.slow
    @pytest.mark.selenium
    @pytest.mark.firefox
    def test_run_axe_with_options_disable_rule(self, firefox_webdriver):
        """Test running axe with a specific rule disabled."""
        axe = Axe()
        result = axe.run(
            webdriver=firefox_webdriver, options={"rules": {"label": {"enabled": False}}}
        )

        validate_axe_result_structure(result)
        # Check that 'label' rule is not in violations
        violation_ids = [v["id"] for v in result["violations"]]
        assert "label" not in violation_ids

    @pytest.mark.slow
    @pytest.mark.selenium
    @pytest.mark.firefox
    def test_run_axe_detects_known_violations(self, firefox_webdriver):
        """Test that axe detects known violations in the test page."""
        axe = Axe()
        result = axe.run(webdriver=firefox_webdriver)

        violation_ids = [v["id"] for v in result["violations"]]

        # Test page has input without label
        assert "label" in violation_ids, "Should detect missing label"

        # Test page has list structure violation
        assert "list" in violation_ids, "Should detect list structure violation"

    @pytest.mark.slow
    @pytest.mark.selenium
    @pytest.mark.firefox
    def test_run_axe_result_has_timestamp(self, firefox_webdriver):
        """Test that axe result includes timestamp."""
        axe = Axe()
        result = axe.run(webdriver=firefox_webdriver)

        assert "timestamp" in result, "Result should have timestamp"

    @pytest.mark.slow
    @pytest.mark.selenium
    @pytest.mark.firefox
    def test_run_axe_result_has_url(self, firefox_webdriver):
        """Test that axe result includes the tested URL."""
        axe = Axe()
        result = axe.run(webdriver=firefox_webdriver)

        assert "url" in result, "Result should have url"
        assert "test_page.html" in result["url"]


class TestSeleniumChrome:
    """Selenium tests using Chrome browser."""

    @pytest.mark.slow
    @pytest.mark.selenium
    @pytest.mark.chrome
    def test_run_axe_basic(self, chrome_webdriver):
        """Run axe against sample page and verify basic result structure."""
        axe = Axe()
        result = axe.run(webdriver=chrome_webdriver)

        validate_axe_result_structure(result)

    @pytest.mark.slow
    @pytest.mark.selenium
    @pytest.mark.chrome
    def test_run_axe_expected_counts(self, chrome_webdriver):
        """Run axe against sample page and verify expected violation counts."""
        axe = Axe()
        result = axe.run(webdriver=chrome_webdriver)

        # Counts may vary slightly between axe-core versions
        assert len(result["inapplicable"]) >= 70, "Should have many inapplicable rules"
        assert len(result["incomplete"]) >= 0, "Incomplete can be 0 or more"
        assert len(result["passes"]) >= 5, "Should have some passing rules"
        assert len(result["violations"]) >= 8, "Test page should have violations"

    @pytest.mark.slow
    @pytest.mark.selenium
    @pytest.mark.chrome
    def test_run_axe_violations_structure(self, chrome_webdriver):
        """Test that violations have the expected structure."""
        axe = Axe()
        result = axe.run(webdriver=chrome_webdriver)

        assert len(result["violations"]) > 0, "Test page should have violations"

        for violation in result["violations"]:
            validate_violation_structure(violation)

    @pytest.mark.slow
    @pytest.mark.selenium
    @pytest.mark.chrome
    def test_run_axe_with_context_and_options(self, chrome_webdriver):
        """Test running axe with both context and options."""
        axe = Axe()
        result = axe.run(
            webdriver=chrome_webdriver,
            context="form",
            options={"runOnly": {"type": "tag", "values": ["wcag2a"]}},
        )

        validate_axe_result_structure(result)

    @pytest.mark.slow
    @pytest.mark.selenium
    @pytest.mark.chrome
    def test_run_axe_detects_known_violations(self, chrome_webdriver):
        """Test that axe detects known violations in the test page."""
        axe = Axe()
        result = axe.run(webdriver=chrome_webdriver)

        violation_ids = [v["id"] for v in result["violations"]]
        assert "label" in violation_ids, "Should detect missing label"


class TestSeleniumCustomAxeScript:
    """Tests for using custom axe script with Selenium."""

    @pytest.mark.slow
    @pytest.mark.selenium
    @pytest.mark.firefox
    def test_run_axe_from_file(self, firefox_webdriver):
        """Test running axe with script loaded from file."""
        from axe_core_python.base import AXE_FILE_PATH

        axe = Axe.from_file(AXE_FILE_PATH)
        result = axe.run(webdriver=firefox_webdriver)

        validate_axe_result_structure(result)
        assert len(result["violations"]) >= 8
