BOLD_WHITE = "\033[1m"
RED = "\033[91m"
OK_GREEN = "\033[92m"
ENDC = "\033[0m"
YELLOW = "\033[93m"
GRAY = "\033[90m"


COLOR_REFERENCE = {
    "BOLD_WHITE": BOLD_WHITE,
    "RED": RED,
    "OK_GREEN": OK_GREEN,
    "YELLOW": YELLOW,
    "GRAY": GRAY,
}


def format(txt, color):
    return f"{color}{txt}{ENDC}"


def red(txt):
    return format(txt, RED)


def green(txt):
    return format(txt, OK_GREEN)


def yellow(txt):
    return format(txt, YELLOW)


def gray(txt):
    return format(txt, GRAY)


def bold_white(txt):
    return format(txt, BOLD_WHITE)