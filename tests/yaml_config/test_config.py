"""Module for the Config unit tests."""

import pytest
from yaml_config import Config


class TestConfig:
    """Class with unit tests for the Config class."""

    @pytest.fixture
    def config_dict(self):
        """Returns a simple configuration dict."""

        return {
            "level_1_int": 1,
            "level_1_dict": {
                "level_2_int": 2,
            }
        }

    @pytest.fixture
    def config_object(self, config_dict):
        """Returns a simple Config object."""

        return Config(config_dict)

    def test_config_dict(self, config_dict):
        """Tests construction from a dict."""

        cfg = Config(config_dict)
        assert cfg.to_dict() == config_dict

    def test_config_yaml(self, config_dict):
        """Tests construction from a YAML file."""

        cfg = Config("tests/data/test_config.yaml")
        assert cfg.to_dict() == config_dict

    def test_raise_not_found(self):
        """Tests raising error when YAML file not found."""

        with pytest.raises(FileNotFoundError):
            Config("file/not/found.yaml")

    def test_get_existing(self):
        """Tests getting an existing value."""

    def test_get_default_value(self):
        """Tests returning a default value."""

    def test_get_missing_pass(self):
        """Tests silently passing a missing configuration key."""

    def test_get_missing_warn(self):
        """Tests warning on a missing configuration key."""

    def test_get_missing_error(self):
        """Tests error on a missing configuration key."""

    def test_set_existing_value(self):
        """Tests overwriting an existing configuration value."""

    def test_set_new_value(self):
        """Tests setting a new configuration value."""
