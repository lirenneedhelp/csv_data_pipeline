def to_float(value, default=None):
    try:
        return float(value)
    except ValueError:
        return default