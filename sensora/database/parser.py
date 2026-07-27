"""
YAML parser for Sensora hardware definition files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class YamlParser:
    """
    Parses YAML definition files.

    This class is responsible only for reading YAML and converting it
    into Python dictionaries. Schema validation and object creation are
    handled elsewhere.
    """

    def load(self, file_path: Path | str) -> dict[str, Any]:
        """
        Load a YAML file.

        Parameters
        ----------
        file_path
            Path to the YAML file.

        Returns
        -------
        dict[str, Any]
            Parsed YAML data.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.

        IsADirectoryError
            If the path points to a directory.

        ValueError
            If the YAML document is empty.

        TypeError
            If the root YAML object is not a mapping.

        yaml.YAMLError
            If the YAML is malformed.
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"YAML file not found: {path}")

        if not path.is_file():
            raise IsADirectoryError(f"Expected a file: {path}")

        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if data is None:
            raise ValueError(f"YAML file is empty: {path}")

        if not isinstance(data, dict):
            raise TypeError(f"Root YAML object must be a mapping: {path}")

        return data

    def loads(self, content: str) -> dict[str, Any]:
        """
        Parse YAML from a string.

        Parameters
        ----------
        content
            YAML document.

        Returns
        -------
        dict[str, Any]
            Parsed YAML data.

        Raises
        ------
        ValueError
            If the document is empty.

        TypeError
            If the root YAML object is not a mapping.

        yaml.YAMLError
            If the YAML is malformed.
        """
        data = yaml.safe_load(content)

        if data is None:
            raise ValueError("YAML content is empty.")

        if not isinstance(data, dict):
            raise TypeError("Root YAML object must be a mapping.")

        return data
