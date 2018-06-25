from enum import Enum

from power_shovel.utils import color_codes as COLOR


class LogLevels(Enum):
    NONE = -1
    ERROR = 0
    WARN = 1
    INFO = 2
    DEBUG = 3


__LEVEL = LogLevels.ERROR


def set_level(level):
    """Set the log level"""
    global __LEVEL
    __LEVEL = level


def error(txt):
    if __LEVEL.value >= LogLevels.ERROR.value:
        print(COLOR.red(txt))


def warn(txt):
    if __LEVEL.value >= LogLevels.WARN.value:
        print(COLOR.yellow(txt))


def info(txt):
    if __LEVEL.value >= LogLevels.INFO.value:
        print(txt)


def debug(txt):
    if __LEVEL.value >= LogLevels.DEBUG.value:
        print(COLOR.gray(txt))


__all__ = [
    LogLevels,
    set_level,
    error,
    warn,
    info,
    debug
]