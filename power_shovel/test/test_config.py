import pytest

from power_shovel.config import CONFIG, Config, MissingConfiguration


class Parent(Config):
    FOO = "foo"


class Child(Config):
    BAR = "bar"


class GrandChild(Config):
    XOO = "xoo"


@pytest.fixture
def mock_nested_config():
    root = Parent()
    child = Child()
    root.add("CHILD", child)
    child.add("GRANDCHILD", GrandChild())
    yield root


class TestConfig:
    def test_add(self, mock_nested_config):
        """Child configs can be added to the main config object"""
        assert mock_nested_config.FOO == "foo"
        assert mock_nested_config.CHILD.BAR == "bar"
        print(mock_nested_config.CHILD.__dict__)
        assert mock_nested_config.CHILD.GRANDCHILD.XOO == "xoo"

    def test_format(self):
        """Config object may be used to format strings"""
        config = Config()
        assert config.format("{ENV}") == "DEV"

    def test_format_nested_value(self):
        """Config values are recursively resolved"""
        config = Config()
        config.NESTED = "{ENV}"
        config.NESTED_2ND_LEVEL = "{NESTED}"
        assert config.format("{NESTED_2ND_LEVEL}") == "DEV"

    def test_format_child(self, mock_nested_config):
        """Child config should be usable by format"""
        assert mock_nested_config.format("{CHILD.BAR}") == "bar"
        assert mock_nested_config.format("{CHILD.GRANDCHILD.XOO}") == "xoo"

        # nested config can reference values defined by other configs
        mock_nested_config.CHILD.NESTED = "{CHILD.GRANDCHILD.XOO}"
        mock_nested_config.CHILD.GRANDCHILD.NESTED_2ND_LEVEL = "{CHILD.NESTED}"
        assert mock_nested_config.format("{CHILD.NESTED}") == "xoo"
        assert mock_nested_config.format("{CHILD.GRANDCHILD.NESTED_2ND_LEVEL}") == "xoo"

    def test_format_extra_kwargs(self, mock_nested_config):
        """Extra kwargs are formatted just like str.format()"""
        assert (
            mock_nested_config.format("{CHILD.BAR} {EXTRA}", EXTRA="extra")
            == "bar extra"
        )

    def test_format_missing_config(self):
        """Config object may be used to format strings"""
        """missing config is raise when trying to format using a config value that doesn't exist"""
        config = Config()
        config.NESTED = "{DOES_NOT_EXIST}"

        # If a direct reference is missing, key is None
        with pytest.raises(MissingConfiguration) as exec_info:
            config.format("{DOES_NOT_EXIST}")
        assert str(exec_info.value) == str(MissingConfiguration("DOES_NOT_EXIST"))

        # If a nested reference is missing, key is the variable that references the missing key
        with pytest.raises(MissingConfiguration) as exec_info:
            config.format("{NESTED}")
        assert str(exec_info.value) == str(
            MissingConfiguration("DOES_NOT_EXIST", "NESTED")
        )

    def test_variables(self):
        """Test default values for config"""
        config = Config()
        assert config.POWER_SHOVEL == "/opt/power_shovel/power_shovel"
        assert config.PWD == "/opt/power_shovel"
        assert config.PROJECT_NAME is None
        assert config.ENV == "DEV"
        assert config.BUILDER_DIR == ".builder"
        assert config.BUILDER == "/opt/power_shovel/.builder"

    def test_config_instance(self):
        """Test that global config object was created"""
        assert isinstance(CONFIG, Config)
