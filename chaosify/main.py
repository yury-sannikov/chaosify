import functools
from .check import should_instrument
from .wreck import maybe_wreck


def chaos(error_threshold: float, result=None, exception=None):
    def chaos_outer(func):
        if not should_instrument(func):
            return func

        @functools.wraps(func)
        def chaos_inner(*args, **kwargs):
            fn_res = func(*args, **kwargs)
            return maybe_wreck(
                fn_res,
                error_threshold=error_threshold,
                result=result,
                exception=exception,
            )

        return chaos_inner

    return chaos_outer
