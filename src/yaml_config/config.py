"""Module for loading YAML configuration files."""

import logging
import warnings

from copy import deepcopy
from typing import Any, Dict, Union

import yaml  # type: ignore


class Config:
    """
    Class for processing YAML configuration files.

    Parameters
    ----------
    config : Union[str, dict]
        Configuration settings provided as either:
        - str: Path to a YAML file.
        - dict: Dict with configuration settings.

    defaults : Union[str, dict, None]
        Configuration default settings either as:
        - str: Path to a YAML file
        - dict: Dict with default settins.
        - None: No default settings

    Methods
    -------
    get(path, default=None, not_found="silent")
        Gets a configuration key. Use the default argument to
        specify a value to return if the key is not found.

        Use the not_found argument to specify what happens when
        a key is not found. Choose from:

        - "silent" (do nothing, default)
        - "warn"   (raise a warning)
        - "error"  (raise a KeyError)

    set(path, value, not_found="error")
        Sets a configuration key to the provided value. Returns
        a boolean indicating whether the update was succesful.

        Use the not_found argument to specify what happens when
        the key is not found. Choose from:

        - "silent" (do nothing)
        - "warn"   (raise a warning)
        - "error"  (raise a KeyError, default)
    """

    def __init__(
        self, config: Union[str, dict], defaults: Union[str, dict, None] = None
    ) -> None:

        self._log = logging.getLogger(__name__)

        if isinstance(config, str):
            config = self._load(config)
        if isinstance(defaults, str):
            defaults = self._load(defaults)

        if defaults and config:
            self._config = self._override_defaults(defaults, config)
        elif defaults:
            self._config = deepcopy(defaults)
        elif config:
            self._config = deepcopy(config)
        else:
            raise ValueError("No configuration or default configuration supplied.")

    def _load(self, config_path: str) -> Dict[str, Any]:
        """
        Loads the configuration as dictionairy.

        Parameters
        ----------
        config_path : str
            Path to the YAML configuration file.

        Returns
        -------
        dict
            Configuration settings as dict.
        """

        self._log.info("Reading configuration from: %s", config_path)

        try:
            with open(config_path, "r") as config_file:
                config = yaml.safe_load(config_file)

        except FileNotFoundError as error:
            msg = f"Cannot find configuration file {config_path}."
            self._log.exception(msg)
            raise FileNotFoundError(msg) from error

        except IOError as error:
            msg = f"Cannot read configuration file {config_path}."
            self._log.exception(msg)
            raise RuntimeError(msg) from error

        self._log.info("Finished reading configuration.")
        return config

    def _override_defaults(self, defaults: dict, config: dict) -> dict:
        """
        Overrides default settings with configuration settings.

        Parameters
        ----------
        defaults : dict
            Dict with default configuration values.
        config: dict
            Dict with actual configuration values.

        Returns
        -------
        dict
            Dict with updated configuration values.
        """

        merged_keys = set(defaults) | set(config)
        combined = {}
        for key in merged_keys:
            # Appears in both, combine values
            if key in config and key in defaults:
                # Merge nested configuration
                if isinstance(defaults[key], dict) and isinstance(config, dict):
                    combined[key] = self._override_defaults(defaults[key], config[key])
                # Or copy scalar value
                else:
                    combined[key] = deepcopy(config[key])

            # Only in config
            elif key in config:
                combined[key] = deepcopy(config[key])

            # Only in defaults
            else:
                combined[key] = deepcopy(defaults[key])

        return combined

    def _check_key(self, section: Dict[str, Any], key: str, not_found: str) -> bool:
        """
        Checks presence of a key in a section of the configuration.

        Parameters
        ----------
        section : dict
            A section of the configuration.
        key : str
            Key to search the section for.
        not_found : str
            Action to perform when the key is not found.

        Returns
        -------
        bool
            True if the key exists, False otherwise.
        """

        valid = "error", "warn", "silent"
        if not_found not in valid:
            raise ValueError(
                "Unexpected value '%s' for not_found parameter, use one of '%s'."
                % (not_found, "', '".join(valid))
            )

        if key not in section:
            if not_found == "error":
                msg = f"Cannot find key '{key}' in configuration."
                self._log.error(msg)
                raise KeyError(msg)
            elif not_found == "warn":
                msg = f"Cannot find key '{key}' in configuration."
                warnings.warn(msg)
                self._log.warning(msg)
            return False

        return True

    def get(self, path: str, default: Any = None, not_found: str = "silent") -> Any:
        """
        Get a value from the configuration using the specified path.

        Parameters
        ----------
        path : str
            Path to the requested value, for example:
            "some_section/some_key" would retrieve config["some_section"]["some_key"]
        default : Optional[Any]
            Value to return when the path is not found.
        not_found : Optional[str]
            Specify what to do when a path is not found:
            - pass:    silently return the default value (default)
            - warn:    raise a warning then return default value.
            - error:   raise an error.

        Returns
        -------
        Any
            The requested value.
        """

        self._log.debug("Getting configuration key: %s", path)

        # Recursively traverse the path
        parent = self._config
        while "/" in path:
            key, path = path.split("/", 1)
            if self._check_key(parent, key, not_found):
                parent = parent[key]
            else:
                return default

        # Return key if it exists
        if self._check_key(parent, path, not_found):
            self._log.debug("Returning configuration value: %s", parent[path])
            return parent[path]

        # Return default otherwise
        self._log.debug("Returning default value: %s", default)
        return default

    def set(self, path: str, value: Any, not_found: str = "error") -> bool:
        """
        Set a configuration key using the specified path and value.

        Parameters
        ----------
        path : str
            Path to the requested value, for example:
            "some_section/some_key" would retrieve config["some_section"]["some_key"]
        value : Any
            Value to set the key to.
        not_found : Optional[str]
            Specify what to do when a path is not found:
            - error:   raise an error (default).
            - warn:    raise a warning then return default value.
            - pass:    continue silently, leaving the configuration as-is.

        Returns
        -------
        bool
            True on succes, False on error.
        """

        self._log.debug("Setting configuration key: %s", path)

        # Recursively traverse the path
        parent = self._config
        while "/" in path:
            key, path = path.split("/", 1)
            if self._check_key(parent, key, not_found):
                parent = parent[key]
            else:
                return False

        # Set key if it exists
        if self._check_key(parent, path, not_found):
            self._log.debug("Setting value: %s", value)
            parent[path] = value
            return True

        return False

    def __getitem__(self, path):
        """Convenience wrapper for get() method."""

        return self.get(path)

    def __setitem__(self, path, value):
        """Convenience wrapper for set() method."""

        return self.set(path, value)

    def to_dict(self):
        """Returns config as a dict."""

        return self._config
