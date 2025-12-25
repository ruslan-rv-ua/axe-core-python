"""
Unit tests for the base module.

These tests cover the AxeBase class and its helper methods
without requiring browser automation (fast tests).
"""

import tempfile
from pathlib import Path

import pytest

from axe_core_python.base import AXE_FILE_PATH, AXE_SCRIPT, AxeBase


class TestAxeScript:
    """Tests for the bundled axe-core script."""

    @pytest.mark.unit
    def test_axe_file_exists(self):
        """Test that the bundled axe.min.js file exists."""
        assert AXE_FILE_PATH.exists(), "axe.min.js file should exist"

    @pytest.mark.unit
    def test_axe_script_not_empty(self):
        """Test that the axe script is not empty."""
        assert len(AXE_SCRIPT) > 0, "AXE_SCRIPT should not be empty"

    @pytest.mark.unit
    def test_axe_script_contains_axe_function(self):
        """Test that the axe script contains the axe.run function."""
        assert "axe" in AXE_SCRIPT.lower(), "Script should contain 'axe'"


class TestFormatScriptArgs:
    """Tests for the _format_script_args static method."""

    @pytest.mark.unit
    def test_format_args_no_params(self):
        """Test formatting with no parameters."""
        result = AxeBase._format_script_args()
        assert result == "", "Should return empty string when no params"

    @pytest.mark.unit
    def test_format_args_context_only_string(self):
        """Test formatting with context as string only."""
        result = AxeBase._format_script_args(context="body")
        assert result == "'body'", "Should return quoted string context"

    @pytest.mark.unit
    def test_format_args_context_only_dict(self):
        """Test formatting with context as dict only."""
        result = AxeBase._format_script_args(context={"include": ["#main"]})
        assert "include" in result, "Should include context dict"

    @pytest.mark.unit
    def test_format_args_context_only_list(self):
        """Test formatting with context as list only."""
        result = AxeBase._format_script_args(context=["#main", "#footer"])
        assert "#main" in result and "#footer" in result, "Should include list items"

    @pytest.mark.unit
    def test_format_args_options_only(self):
        """Test formatting with options only."""
        result = AxeBase._format_script_args(options={"runOnly": ["wcag2a"]})
        assert "runOnly" in result, "Should include options"

    @pytest.mark.unit
    def test_format_args_both_params(self):
        """Test formatting with both context and options."""
        result = AxeBase._format_script_args(context="body", options={"runOnly": ["wcag2a"]})
        # Both should be present with comma separator
        assert "'body'" in result, "Should include context"
        assert "runOnly" in result, "Should include options"
        assert "," in result, "Should have comma separator"

    @pytest.mark.unit
    def test_format_args_complex_context(self):
        """Test formatting with complex context configuration."""
        context = {"include": [["#main"], ["#sidebar"]], "exclude": [["#ad-banner"]]}
        result = AxeBase._format_script_args(context=context)
        assert "include" in result
        assert "exclude" in result

    @pytest.mark.unit
    def test_format_args_complex_options(self):
        """Test formatting with complex options configuration."""
        options = {
            "runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa"]},
            "rules": {"color-contrast": {"enabled": False}},
        }
        result = AxeBase._format_script_args(options=options)
        assert "runOnly" in result
        assert "rules" in result


class TestAxeBaseFromFile:
    """Tests for the from_file class method."""

    @pytest.mark.unit
    def test_from_file_with_valid_path(self):
        """Test creating Axe instance from a valid file path."""
        # Use the bundled axe file for testing
        # We need a concrete implementation to test from_file
        # Import one of the concrete classes
        from axe_core_python.selenium import Axe

        axe = Axe.from_file(AXE_FILE_PATH)
        assert axe is not None
        assert len(axe.axe_script) > 0

    @pytest.mark.unit
    def test_from_file_with_string_path(self):
        """Test creating Axe instance from a string path."""
        from axe_core_python.selenium import Axe

        axe = Axe.from_file(str(AXE_FILE_PATH))
        assert axe is not None
        assert len(axe.axe_script) > 0

    @pytest.mark.unit
    def test_from_file_with_custom_script(self):
        """Test creating Axe instance from a custom script file."""
        from axe_core_python.selenium import Axe

        # Create a temporary file with mock script
        with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
            mock_script = "// Mock axe script\nvar axe = {};"
            f.write(mock_script)
            temp_path = f.name

        try:
            axe = Axe.from_file(temp_path)
            assert axe.axe_script == mock_script
        finally:
            Path(temp_path).unlink()

    @pytest.mark.unit
    def test_from_file_nonexistent_raises_error(self):
        """Test that from_file raises error for nonexistent file."""
        from axe_core_python.selenium import Axe

        with pytest.raises(FileNotFoundError):
            Axe.from_file("/nonexistent/path/axe.min.js")


class TestAxeBaseInit:
    """Tests for AxeBase initialization."""

    @pytest.mark.unit
    def test_init_with_default_script(self):
        """Test initialization with default script."""
        from axe_core_python.selenium import Axe

        axe = Axe()
        assert axe.axe_script == AXE_SCRIPT

    @pytest.mark.unit
    def test_init_with_custom_script(self):
        """Test initialization with custom script."""
        from axe_core_python.selenium import Axe

        custom_script = "// Custom axe script"
        axe = Axe(axe_script=custom_script)
        assert axe.axe_script == custom_script


class TestAllAxeImplementations:
    """Tests that verify all Axe implementations have consistent interface."""

    @pytest.mark.unit
    def test_selenium_axe_has_run_method(self):
        """Test that Selenium Axe has run method."""
        from axe_core_python.selenium import Axe

        axe = Axe()
        assert hasattr(axe, "run")
        assert callable(axe.run)

    @pytest.mark.unit
    def test_sync_playwright_axe_has_run_method(self):
        """Test that Sync Playwright Axe has run method."""
        from axe_core_python.sync_playwright import Axe

        axe = Axe()
        assert hasattr(axe, "run")
        assert callable(axe.run)

    @pytest.mark.unit
    def test_async_playwright_axe_has_run_method(self):
        """Test that Async Playwright Axe has run method."""
        from axe_core_python.async_playwright import Axe

        axe = Axe()
        assert hasattr(axe, "run")
        # For async, run is a coroutine function
        import inspect

        assert inspect.iscoroutinefunction(axe.run)

    @pytest.mark.unit
    def test_all_implementations_inherit_from_base(self):
        """Test that all implementations inherit from AxeBase."""
        from axe_core_python.async_playwright import Axe as AsyncAxe
        from axe_core_python.selenium import Axe as SeleniumAxe
        from axe_core_python.sync_playwright import Axe as SyncAxe

        assert issubclass(SeleniumAxe, AxeBase)
        assert issubclass(SyncAxe, AxeBase)
        assert issubclass(AsyncAxe, AxeBase)

    @pytest.mark.unit
    def test_all_implementations_have_from_file(self):
        """Test that all implementations have from_file method."""
        from axe_core_python.async_playwright import Axe as AsyncAxe
        from axe_core_python.selenium import Axe as SeleniumAxe
        from axe_core_python.sync_playwright import Axe as SyncAxe

        for cls in [SeleniumAxe, SyncAxe, AsyncAxe]:
            assert hasattr(cls, "from_file")
            assert callable(cls.from_file)
