import logging


class debugFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == 10:
            return record


class infoFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == 20:
            return record


class warningFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == 30:
            return record


class errorFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == 40:
            return record


class criticalFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == 50:
            return record
