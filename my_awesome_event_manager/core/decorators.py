import functools
import time

# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


def calculate_api_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        value.data["results_time"] = f"{run_time:.4} sec."
        return value

    return wrapper


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
