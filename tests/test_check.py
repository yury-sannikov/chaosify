import os
import pytest
from unittest import mock
import chaosify.check as check


def function_to_instrument():
    """
    This function is used for testing purposes.
    """


@pytest.mark.parametrize(
    "enabled,exclude,expected",
    [
        ("true", "", True),
        ("True", "", True),
        ("false", "", False),
        ("False", "", False),
        ("true", "function_to_instrument", False),
        ("true", "test_check.function_to_instrument", False),
        ("true", "tests.test_check.function_to_instrument", False),
        ("true", "tests.test_check", False),
    ],
)
def test_check(monkeypatch, enabled, exclude, expected):
    check.is_enabled.cache_clear()
    check.is_function_enabled.cache_clear()
    with mock.patch.dict(os.environ, clear=True):
        envvars = {
            "CHAOS_ENABLED": enabled,
            "CHAOS_EXCLUDE": exclude,
        }

        for k, v in envvars.items():
            monkeypatch.setenv(k, v)
        assert check.should_instrument(function_to_instrument) == expected
