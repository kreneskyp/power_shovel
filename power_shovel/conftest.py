import pytest
from unittest import mock

from power_shovel.config import CONFIG
from power_shovel.exceptions import MockExit
from power_shovel.module import load_modules, clear_modules
from power_shovel.runner import ExitCodes
from power_shovel.task import clear_task_registry
from power_shovel.test.fake import (
    mock_task,
    mock_nested_single_dependency_nodes,
    MOCK_TASKS,
    mock_tasks_with_clean_functions,
    mock_tasks_with_passing_checkers,
    mock_failing_tasks,
    build_test_args,
)


# =================================================================================================
# Environment and system components
# =================================================================================================


@pytest.fixture
def mock_environment():
    """
    Initialize power_shovel with a test environment
    """
    CONFIG.PROJECT_NAME = "unittests"
    load_modules("power_shovel.modules.core", "power_shovel.test.modules.test")
    yield
    clear_task_registry()
    clear_modules()


@pytest.fixture
def mock_init():
    """
    Mock `runner.init`
    """
    patcher = mock.patch("power_shovel.runner.init")
    mock_init = patcher.start()
    mock_init.return_value = ExitCodes.SUCCESS
    yield mock_init
    patcher.stop()


@pytest.fixture(params=ExitCodes.init_errors)
def mock_init_exit_errors(request, mock_init):
    mock_init.return_value = request.param
    yield mock_init


@pytest.fixture
def mock_run():
    """
    Mock `runner.run`
    """
    patcher = mock.patch("power_shovel.runner.run")
    mock_run = patcher.start()
    mock_run.return_value = ExitCodes.SUCCESS
    yield mock_run
    patcher.stop()


@pytest.fixture(params=ExitCodes.run_errors)
def mock_run_exit_errors(request, mock_run):
    mock_run.return_value = request.param
    yield mock_run


@pytest.fixture
def mock_parse_args():
    """
    Mock runner.parse_args()
    """
    patcher = mock.patch("power_shovel.runner.parse_args")
    mock_parse_args = patcher.start()
    mock_parse_args.return_value = build_test_args()
    yield mock_parse_args
    patcher.stop()


# =================================================================================================
# Tasks and trees of tasks
# =================================================================================================


@pytest.fixture
def task(mock_environment):
    """Create a single mock task"""
    yield mock_task()
    clear_task_registry()


@pytest.fixture
def nested_tasks():
    """Create a single mock task"""
    yield mock_nested_single_dependency_nodes()
    clear_task_registry()


@pytest.fixture
def tasks_with_cleaners():
    """nested tasks all with mocked cleaner functions"""
    yield mock_tasks_with_clean_functions()
    clear_task_registry()


@pytest.fixture
def tasks_with_passing_checkers(request):
    """nested tasks all with mocked cleaner functions"""
    yield mock_tasks_with_passing_checkers()
    clear_task_registry()


@pytest.fixture
def tasks_that_fail():
    """nested tasks all with mocked cleaner functions"""
    yield mock_failing_tasks()
    clear_task_registry()


@pytest.fixture(params=list(MOCK_TASKS.keys()))
def task_scenarios(request):
    """
    Fixture that iterates through all MOCK_TASKS scenarios
    """
    yield MOCK_TASKS[request.param]()
    clear_task_registry()


# =================================================================================================
# Utils
# =================================================================================================


@pytest.fixture
def mock_exit():
    def raise_exit_code(code):
        raise MockExit(ExitCodes(code))

    patcher = mock.patch("power_shovel.runner.sys.exit")
    mock_exit = patcher.start()
    mock_exit.side_effect = raise_exit_code
    yield mock_exit
    patcher.stop()
