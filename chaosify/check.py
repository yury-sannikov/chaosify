import os
import inspect
from functools import cache, lru_cache
from pathlib import Path


@cache
def is_enabled() -> bool:
    return os.environ.get("CHAOS_ENABLED", "false").lower() == "true"


@lru_cache
def is_function_enabled(func) -> bool:
    """ """
    path = Path(inspect.getfile(func)).relative_to(Path.cwd())
    file_path = str(path.parent).replace("/", ".")
    func_path = f"{file_path}.{path.stem}.{func.__name__}"
    excluded = os.environ.get("CHAOS_EXCLUDE", "").split(",")
    for item in excluded:
        if item and item in func_path:
            return False
    return True


def should_instrument(func) -> bool:
    if not is_enabled():
        return False

    return is_function_enabled(func)
