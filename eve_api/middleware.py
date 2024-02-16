from loguru import logger
import uuid
import time


IGNORED_PATHS = [
    "/static/rest_framework/css/bootstrap-tweaks.css",
    "/static/rest_framework/css/default.css",
    "/static/rest_framework/js/ajax-form.js",
    "/static/rest_framework/js/bootstrap.min.js",
    "/static/rest_framework/js/prettify-min.js",
    "/static/rest_framework/js/jquery-3.5.1.min.js",
    "/static/rest_framework/js/csrf.js",
    "/static/rest_framework/js/default.js",
    "/static/rest_framework/css/prettify.css",
    "/static/rest_framework/css/bootstrap.min.css",
    "/favicon.ico"
]


def logging_middleware(get_response):
    def middleware(request):
        if request.path in IGNORED_PATHS:
            return get_response(request)

        request_id = str(uuid.uuid4())

        # Add context to all loggers
        with logger.contextualize(request_id=request_id):

            request.start_time = time.time()

            response = get_response(request)

            elapsed = time.time() - request.start_time

            # After the response is received
            logger.bind(
                path=request.path,
                method=request.method,
                status_code=response.status_code,
                response_size=len(response.content),
                elapsed=elapsed,
            ).info(
                "finished logging '{method}' request to '{path}'",
                method=request.method,
                path=request.path,
            )

            response["X-Request-ID"] = request_id

            return response
    return middleware
