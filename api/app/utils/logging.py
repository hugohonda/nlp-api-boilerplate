from fastapi import Request
import logging


class APILogger:
    def __init__(self):
        self.logger = logging.getLogger("api_logger")
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Create and configure a StreamHandler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        # Add the StreamHandler to the logger
        self.logger.addHandler(stream_handler)

    def add_request_id(self, request_id):
        # Add a unique request ID to the logger's extra attributes
        self.logger = self.logger.bind(request_id=request_id)

    def add_request_info(self, request: Request):
        # Add request-related information to the logger's extra attributes
        self.logger = self.logger.bind(
            method=request.method,
            url=request.url.path,
            client=request.client.host,
        )

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def exception(self, message):
        self.logger.exception(message)


logger = APILogger()
