import logging
import os
import subprocess

from power_shovel.config import CONFIG
from power_shovel.exceptions import ExecuteFailed


logger = logging.getLogger(__name__)


def raise_for_status(code: int) -> None:
    """
    Raise `ExecuteFailed` if the code is an error code
    :param code: code to check
    """
    if code != 0:
        raise ExecuteFailed(f"Process returned a non-zero code: {code}")


def execute(command: str, silent: bool = False, env: dict = None) -> int:
    """
    Execute a shell command.

    ```
    execute("echo this is an example")
    ```

    Any config variables will be expanded.

    ```
    execute("echo this is the working directory: {PWD}")
    ```

    :param command: space separated command and args
    :param silent: do not echo command
    :return:
    """
    formatted_command = CONFIG.format(command)
    if not silent:
        logger.info(formatted_command)

    # Need to pass full environment, merge passed in env with process env.
    built_env = os.environ.copy()
    if env:
        built_env.update(env)

    args = [arg for arg in formatted_command.split(" ") if arg]
    return subprocess.call(args, env=built_env)


def get_dev_uid() -> int:
    """get dev uid of running process"""
    return int(subprocess.check_output(["id", "-u"])[:-1])


def get_dev_gid() -> int:
    """get dev gid of running process"""
    return int(subprocess.check_output(["id", "-g"])[:-1])
