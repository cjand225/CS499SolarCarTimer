import logging


class debugFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.DEBUG:
            return record


class infoFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.INFO:
            return record


class warningFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.WARNING:
            return record


class errorFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.ERROR:
            return record


class criticalFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.CRITICAL:
            return record
