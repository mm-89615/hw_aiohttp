import json


def generate_error(error_cls, message):
    return error_cls(
        text=json.dumps({"error": message}),
        content_type="application/json",
    )
