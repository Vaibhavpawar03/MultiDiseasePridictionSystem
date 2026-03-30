def map_level(value):
    mapping = {
        "low": 0,
        "normal": 1,
        "high": 2,
        "very_high": 3
    }
    return mapping.get(str(value).lower(), 1)


def map_yes_no(value):
    return 1 if str(value).lower() == "yes" else 0


def map_gender(value):
    return 1 if str(value).lower() == "male" else 0