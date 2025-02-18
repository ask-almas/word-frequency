HTTP_BAD_REQUEST = 400


def validate_params(required_params, request_data):
    missing = [param for param in required_params if param not in request_data]
    if missing:
        return {"error": f"Missing required parameters: {', '.join(missing)}"}, HTTP_BAD_REQUEST
    return None
