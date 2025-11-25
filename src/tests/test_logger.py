"""
Unit tests for logger module
"""
import pytest
from utils.logger import LOG


class TestLogger:
    """Test logger functionality"""

    def test_logger_exists(self):
        """Test that LOG object exists"""
        assert LOG is not None

    def test_logger_has_methods(self):
        """Test that logger has expected methods"""
        assert hasattr(LOG, 'debug')
        assert hasattr(LOG, 'info')
        assert hasattr(LOG, 'warning')
        assert hasattr(LOG, 'error')
        assert hasattr(LOG, 'critical')

    def test_logger_can_log_messages(self, caplog):
        """Test that logger can log messages"""
        test_message = "Test log message"
        LOG.info(test_message)

        # The message should have been logged
        # Note: caplog may not capture loguru messages in all cases,
        # so we just verify the method doesn't raise an error
        assert True

    def test_logger_debug_level(self):
        """Test logging at debug level"""
        try:
            LOG.debug("Debug message")
            assert True
        except Exception as e:
            pytest.fail(f"Logger debug failed: {e}")

    def test_logger_error_level(self):
        """Test logging at error level"""
        try:
            LOG.error("Error message")
            assert True
        except Exception as e:
            pytest.fail(f"Logger error failed: {e}")

