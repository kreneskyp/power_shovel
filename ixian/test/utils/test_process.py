import pytest

from ixian.exceptions import ExecuteFailed
from ixian.utils.process import (
    raise_for_status,
    get_dev_uid,
    get_dev_gid,
    execute,
)


class TestRaiseForStatus:
    def test_zero(self):
        """zero is the unix standard for a successful process. No error should be raised."""
        raise_for_status(0)

    def test_error(self):
        """Error codes should raise ExecuteFailed"""
        for code in [-2, -1, 1, 2]:
            with pytest.raises(ExecuteFailed):
                raise_for_status(code)


class TestExecute:
    """Tests for `execute` helper that is used to run shell commands"""

    def test_success(self):
        """Test a process returning successfully"""
        return_code = execute("ls")
        assert return_code == 0

    def test_error(self):
        """Test a process returning a nonzero code"""
        return_code = execute("false")
        assert return_code == 1

    def test_command_formatting(self):
        """Variables in the command are expanded before being executed"""
        return_code = execute("echo this is the working directory: {PWD}")
        assert return_code == 0

    def test_command_multiple_args(self):
        """command may be a string with space separated arguments"""
        return_code = execute("echo this command has args")
        assert return_code == 0

    def test_silent(self, mock_logger):
        """when silent, command is not echoed by the logger"""
        return_code = execute("ls", silent=True)
        assert return_code == 0
        mock_logger.info.assert_not_called()

        # Test with silent=False to sanity check
        return_code = execute("ls", silent=False)
        assert return_code == 0
        mock_logger.info.called_with("ls")


def test_get_dev_uid():
    assert get_dev_uid() == 0


def test_get_dev_gid():
    assert get_dev_gid() == 0