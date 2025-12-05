import json
from pathlib import Path
from typing import Optional, Union


class FileManager:
    """
    Contains functions that make it easier to manage files and directories.
    """

    def create_folder(self, folder_path: Path) -> None:
        """
        Creates a new folder based on the provided path. Creates
        parent folders as well when non-existent.

        Args:
            file_path: Path of the folder
        """
        folder_path.mkdir(parents=True, exist_ok=True)

    def load_json(self, file_path: Path) -> Union[dict, list]:
        """
        Loads JSON from the given file path.

        Args:
            file_path: Path where the JSON file is located

        Returns:
            dict | list: The content that the JSON contains
        """
        with file_path.open(encoding="utf-8") as f:
            return json.load(f)

    def save_json(self, file_path: Path, data: Union[dict, list], indent: int = 2) -> None:
        """
        Writes any data as JSON to the given file path.

        Args:
            file_path: Path where to write the JSON file to
            data: Data to store within the JSON
            indent: Indent of the JSON file
        """
        file_path.write_text(json.dumps(data, indent=indent, ensure_ascii=False), encoding="utf-8")

    def save_python(
        self, file_path: Path, code: str, encoding: str = "utf-8", overwrite: Optional[bool] = True
    ) -> None:
        """
        Writes the given code as Python to the given file path.

        Args:
            file_path: Path where to write the Python file to
            code: The code to write to the Python file
            encoding: The text encoding (Default: 'utf-8')
        """
        if file_path.exists() and not overwrite:
            return

        file_path.write_text(code, encoding=encoding)

    def remove_file(self, file_path: Path) -> None:
        """
        Removes the provided path.

        Args:
            file_path: Path to remove
        """
        file_path.unlink(missing_ok=True)
