import time


def convert_seconds_to_timeframe(seconds):
    """Converts seconds to time frame.
    Args:
      seconds: time in seconds.
    Returns:
      str, converted time string.
    """
    # convert seconds to struct_time
    time_struct = time.gmtime(seconds)
    # get time components
    h = time_struct.tm_hour
    m = time_struct.tm_min
    s = time_struct.tm_sec
    ms = int((seconds - int(seconds)) * 1000)
    # format time string
    time_string = "{:02d}:{:02d}:{:02d},{:03d}".format(h, m, s, ms)

    return time_string


def retry_on_error(max_retries, wait_time=1.0):
    """"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    print(f"Error：{e}")
                    print(f" {retries + 1}/{max_retries} time reply...")
                    retries += 1
                    time.sleep(wait_time)
            raise Exception(f"Over，max num is: {max_retries}")

        return wrapper

    return decorator
