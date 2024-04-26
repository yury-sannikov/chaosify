import random


def maybe_wreck[
    T
](function_result: T, error_threshold: float, result: T = None, exception=None) -> T:
    if random.random() >= error_threshold:
        return function_result

    # If we have no exception set, return defined result
    if exception is None:
        return result

    # raise exception
    raise exception
