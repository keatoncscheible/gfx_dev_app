import logging
import os


def add_logging_level(level_name, level_num, method_name=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `level_name` becomes an attribute of the `logging` module with the value
    `level_num`. `method_name` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `method_name` is not specified, `level_name.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> add_logging_level('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    if not method_name:
        method_name = level_name.lower()

    if hasattr(logging, level_name):
        raise AttributeError("{} already defined in logging module".format(level_name))
    if hasattr(logging, method_name):
        raise AttributeError("{} already defined in logging module".format(method_name))
    if hasattr(logging.getLoggerClass(), method_name):
        raise AttributeError("{} already defined in logger class".format(method_name))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(level_num):
            self._log(level_num, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(level_num, message, *args, **kwargs)

    logging.addLevelName(level_num, level_name)
    setattr(logging, level_name, level_num)
    setattr(logging.getLoggerClass(), method_name, logForLevel)
    setattr(logging, method_name, logToRoot)


class PyFxDevLogFilter(logging.Filter):
    def filter(self, record):
        filtered_files = ["acceleratesupport.py"]

        if record.filename in filtered_files:
            return False
        else:
            return True


if not os.path.exists("logs"):
    os.mkdir("logs")


file_logger = logging.FileHandler(filename="logs/pyfx.log")
file_logger.setLevel(logging.DEBUG)
file_logger.addFilter(PyFxDevLogFilter())
file_logger_formatter = logging.Formatter(
    "{filename} : {funcName} : line({lineno}) : time({relativeCreated} ms)\n{levelname} : {message}\n",
    style="{",
)
file_logger.setFormatter(file_logger_formatter)

file_logger_cond = logging.FileHandler(filename="logs/pyfx_cond.log")
file_logger_cond.setLevel(logging.DEBUG)
file_logger_cond.addFilter(PyFxDevLogFilter())
file_logger_cond_formatter = logging.Formatter("{levelname} : {message}", style="{")
file_logger_cond.setFormatter(file_logger_cond_formatter)

console_logger = logging.StreamHandler()
console_logger.setLevel(logging.DEBUG)
console_logger.addFilter(PyFxDevLogFilter())
console_logger_formatter = logging.Formatter("{levelname} : {message}", style="{")
console_logger.setFormatter(console_logger_formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_logger)
logger.addHandler(file_logger_cond)
logger.addHandler(console_logger)

pyfx_log = logger
pyfx_log.shutdown = logging.shutdown
