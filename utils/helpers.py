HTTP_BAD_REQUEST = 400


def validate_params(required_params, params):
    errors = {}
    for param in required_params:
        if param not in params:
            errors[param] = f"'{param}' is required."

    depth = params.get("depth")
    if depth:
        try:
            depth = int(depth)
            if depth < 0 or depth > 3:
                errors["depth"] = "'depth' must be a positive integer no greater than 3."
        except ValueError:
            errors["depth"] = "'depth' must be an integer."

    ignore_list = params.get("ignore_list")
    if ignore_list:
        if not isinstance(ignore_list, list):
            errors["ignore_list"] = "'ignore_list' must be a list."

    percentile = params.get("percentile")
    if percentile:
        try:
            percentile = float(percentile)
            if percentile < 0 or percentile > 1:
                errors["percentile"] = "'percentile' must be between 0 and 1."
        except ValueError:
            errors["percentile"] = "'percentile' must be a number between 0 and 1."

    if errors:
        return errors, HTTP_BAD_REQUEST

    return None
