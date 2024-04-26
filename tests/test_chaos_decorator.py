import os
import sys
import pytest
from unittest import mock

RANDOM = 0.5


@pytest.fixture()
def chaos_env(monkeypatch):
    with mock.patch.dict(os.environ, clear=True):
        envvars = {
            "CHAOS_ENABLED": "true",
        }
        for k, v in envvars.items():
            monkeypatch.setenv(k, v)
        yield


@pytest.fixture()
def chaos_instance(chaos_env):
    from chaosify import chaos

    with mock.patch("random.random", return_value=RANDOM):
        yield chaos


@pytest.mark.parametrize(
    "error_threshold, shoud_throw",
    [(RANDOM, False), (RANDOM + sys.float_info.epsilon, True)],
)
def test_chaos_raise_exception(chaos_instance, error_threshold, shoud_throw):
    @chaos_instance(error_threshold, exception=Exception("Havoc"))
    def _func_under_test():
        return 1

    if shoud_throw:
        with pytest.raises(Exception):
            _func_under_test()
    else:
        assert _func_under_test() == 1


@pytest.mark.parametrize(
    "error_threshold, shoud_fail",
    [(RANDOM, False), (RANDOM + sys.float_info.epsilon, True)],
)
def test_chaos_return_result(chaos_instance, error_threshold, shoud_fail):
    @chaos_instance(error_threshold, result=2)
    def _func_under_test():
        return 1

    if shoud_fail:
        assert _func_under_test() == 2
    else:
        assert _func_under_test() == 1
