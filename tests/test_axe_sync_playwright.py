"""
Sync Playwright integration tests for axe-core-python.

These tests run axe-core accessibility checks using Playwright sync API.
They are marked as slow because they launch real browsers.

Run with: pytest --runslow -m playwright
"""

import pytest

from axe_core_python.sync_playwright import Axe

from .conftest import (
    validate_axe_result_structure,
    validate_node_structure,
    validate_violation_structure,
)


class TestSyncPlaywrightFirefox:
    """Sync Playwright tests using Firefox browser."""

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.firefox
    def test_run_axe_basic(self, sync_playwright_firefox):
        """Run axe against sample page and verify basic result structure."""
        axe = Axe()
        result = axe.run(page=sync_playwright_firefox)

        validate_axe_result_structure(result)

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.firefox
    def test_run_axe_expected_counts(self, sync_playwright_firefox):
        """Run axe against sample page and verify expected violation counts."""
        axe = Axe()
        result = axe.run(page=sync_playwright_firefox)

        # Counts may vary slightly between axe-core versions
        assert len(result["inapplicable"]) >= 70, "Should have many inapplicable rules"
        assert len(result["incomplete"]) >= 0, "Incomplete can be 0 or more"
        assert len(result["passes"]) >= 5, "Should have some passing rules"
        assert len(result["violations"]) >= 8, "Test page should have violations"

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.firefox
    def test_run_axe_violations_structure(self, sync_playwright_firefox):
        """Test that violations have the expected structure."""
        axe = Axe()
        result = axe.run(page=sync_playwright_firefox)

        assert len(result["violations"]) > 0, "Test page should have violations"

        for violation in result["violations"]:
            validate_violation_structure(violation)
            for node in violation["nodes"]:
                validate_node_structure(node)

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.firefox
    def test_run_axe_with_context_string(self, sync_playwright_firefox):
        """Test running axe with context as string selector."""
        axe = Axe()
        result = axe.run(page=sync_playwright_firefox, context="body")

        validate_axe_result_structure(result)

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.firefox
    def test_run_axe_with_context_dict(self, sync_playwright_firefox):
        """Test running axe with context as dict with include/exclude."""
        axe = Axe()
        result = axe.run(page=sync_playwright_firefox, context={"include": [["form"]]})

        validate_axe_result_structure(result)
        assert len(result["violations"]) > 0

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.firefox
    def test_run_axe_with_options_run_only(self, sync_playwright_firefox):
        """Test running axe with options to run only specific rules."""
        axe = Axe()
        result = axe.run(page=sync_playwright_firefox, options={"runOnly": ["label"]})

        validate_axe_result_structure(result)
        assert len(result["violations"]) <= 9

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.firefox
    def test_run_axe_with_options_disable_rule(self, sync_playwright_firefox):
        """Test running axe with a specific rule disabled."""
        axe = Axe()
        result = axe.run(
            page=sync_playwright_firefox, options={"rules": {"label": {"enabled": False}}}
        )

        validate_axe_result_structure(result)
        violation_ids = [v["id"] for v in result["violations"]]
        assert "label" not in violation_ids

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.firefox
    def test_run_axe_detects_known_violations(self, sync_playwright_firefox):
        """Test that axe detects known violations in the test page."""
        axe = Axe()
        result = axe.run(page=sync_playwright_firefox)

        violation_ids = [v["id"] for v in result["violations"]]
        assert "label" in violation_ids, "Should detect missing label"
        assert "list" in violation_ids, "Should detect list structure violation"

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.firefox
    def test_run_axe_result_has_timestamp(self, sync_playwright_firefox):
        """Test that axe result includes timestamp."""
        axe = Axe()
        result = axe.run(page=sync_playwright_firefox)

        assert "timestamp" in result, "Result should have timestamp"

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.firefox
    def test_run_axe_result_has_url(self, sync_playwright_firefox):
        """Test that axe result includes the tested URL."""
        axe = Axe()
        result = axe.run(page=sync_playwright_firefox)

        assert "url" in result, "Result should have url"
        assert "test_page.html" in result["url"]


class TestSyncPlaywrightChromium:
    """Sync Playwright tests using Chromium browser."""

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.chromium
    def test_run_axe_basic(self, sync_playwright_chromium):
        """Run axe against sample page and verify basic result structure."""
        axe = Axe()
        result = axe.run(page=sync_playwright_chromium)

        validate_axe_result_structure(result)

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.chromium
    def test_run_axe_expected_counts(self, sync_playwright_chromium):
        """Run axe against sample page and verify expected violation counts."""
        axe = Axe()
        result = axe.run(page=sync_playwright_chromium)

        # Counts may vary slightly between axe-core versions
        assert len(result["inapplicable"]) >= 70, "Should have many inapplicable rules"
        assert len(result["incomplete"]) >= 0, "Incomplete can be 0 or more"
        assert len(result["passes"]) >= 5, "Should have some passing rules"
        assert len(result["violations"]) >= 8, "Test page should have violations"

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.chromium
    def test_run_axe_violations_structure(self, sync_playwright_chromium):
        """Test that violations have the expected structure."""
        axe = Axe()
        result = axe.run(page=sync_playwright_chromium)

        assert len(result["violations"]) > 0, "Test page should have violations"

        for violation in result["violations"]:
            validate_violation_structure(violation)

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.chromium
    def test_run_axe_with_context_and_options(self, sync_playwright_chromium):
        """Test running axe with both context and options."""
        axe = Axe()
        result = axe.run(
            page=sync_playwright_chromium,
            context="form",
            options={"runOnly": {"type": "tag", "values": ["wcag2a"]}},
        )

        validate_axe_result_structure(result)

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.chromium
    def test_run_axe_detects_known_violations(self, sync_playwright_chromium):
        """Test that axe detects known violations in the test page."""
        axe = Axe()
        result = axe.run(page=sync_playwright_chromium)

        violation_ids = [v["id"] for v in result["violations"]]
        assert "label" in violation_ids, "Should detect missing label"


class TestSyncPlaywrightWebKit:
    """Sync Playwright tests using WebKit browser."""

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.webkit
    def test_run_axe_basic(self, sync_playwright_webkit):
        """Run axe against sample page and verify basic result structure."""
        axe = Axe()
        result = axe.run(page=sync_playwright_webkit)

        validate_axe_result_structure(result)

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.webkit
    def test_run_axe_expected_counts(self, sync_playwright_webkit):
        """Run axe against sample page and verify expected violation counts."""
        axe = Axe()
        result = axe.run(page=sync_playwright_webkit)

        # Counts may vary slightly between axe-core versions
        assert len(result["inapplicable"]) >= 70, "Should have many inapplicable rules"
        assert len(result["incomplete"]) >= 0, "Incomplete can be 0 or more"
        assert len(result["passes"]) >= 5, "Should have some passing rules"
        assert len(result["violations"]) >= 8, "Test page should have violations"

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.webkit
    def test_run_axe_violations_structure(self, sync_playwright_webkit):
        """Test that violations have the expected structure."""
        axe = Axe()
        result = axe.run(page=sync_playwright_webkit)

        assert len(result["violations"]) > 0, "Test page should have violations"

        for violation in result["violations"]:
            validate_violation_structure(violation)

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.webkit
    def test_run_axe_detects_known_violations(self, sync_playwright_webkit):
        """Test that axe detects known violations in the test page."""
        axe = Axe()
        result = axe.run(page=sync_playwright_webkit)

        violation_ids = [v["id"] for v in result["violations"]]
        assert "label" in violation_ids, "Should detect missing label"


class TestSyncPlaywrightCustomAxeScript:
    """Tests for using custom axe script with sync Playwright."""

    @pytest.mark.slow
    @pytest.mark.playwright
    @pytest.mark.chromium
    def test_run_axe_from_file(self, sync_playwright_chromium):
        """Test running axe with script loaded from file."""
        from axe_core_python.base import AXE_FILE_PATH

        axe = Axe.from_file(AXE_FILE_PATH)
        result = axe.run(page=sync_playwright_chromium)

        validate_axe_result_structure(result)
        assert len(result["violations"]) >= 8
