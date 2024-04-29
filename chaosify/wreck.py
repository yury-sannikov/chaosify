import random


def maybe_wreck(function_result, error_threshold: float, result=None, exception=None):
    if random.random() >= error_threshold:
        return function_result

    # If we have no exception set, return defined result
    if exception is None:
        return result

    # raise exception
    raise exception
