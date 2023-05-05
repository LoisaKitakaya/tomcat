def explain_status_code(status_code):
    status_codes = {
        200: "OK",
        201: "Created",
        204: "No Content",
        301: "Moved Permanently",
        302: "Moved Temporarily",
        304: "Not Modified",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        409: "Conflict",
        500: "Internal Server Error",
        501: "The server does not support the requested functionality",
        503: "Service Unavailable",
    }

    for key, value in status_codes.items():
        if status_code == key:
            return value
