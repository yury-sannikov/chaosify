import functools


def chaos(error_rate: float, result=None, exception=None):
    def chaos_outer(func):
        @functools.wraps(func)
        def chaos_inner(*args, **kwargs):
            result = func(*args, **kwargs)
            return result

        return chaos_inner

    return chaos_outer
