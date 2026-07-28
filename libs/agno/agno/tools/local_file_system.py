import json
from pathlib import Path
from typing import Callable, List, Optional, Tuple
from uuid import uuid4

from agno.tools import Toolkit
from agno.utils.log import log_debug, log_error


class LocalFileSystemTools(Toolkit):
    def __init__(
        self,
        target_directory: Optional[str] = None,
        default_extension: str = "txt",
        restrict_to_base_dir: bool = True,
        read_file: bool = True,
        write_file: bool = False,
        all: bool = False,
        **kwargs,
    ):
        """Initialize the LocalFileSystem toolkit.

        Args:
            target_directory: Default directory for file operations. Creates if doesn't exist.
            default_extension: Default file extension when none specified.
            restrict_to_base_dir: If True, file operations cannot escape target_directory.
            read_file: Enable the read_file tool.
            write_file: Enable the write_file tool. Disabled by default (destructive).
            all: Enable all tools.
        """
        self.target_directory = target_directory or str(Path.cwd())
        self.default_extension = default_extension.lstrip(".")
        self.restrict_to_base_dir = restrict_to_base_dir

        target_path = Path(self.target_directory)
        target_path.mkdir(parents=True, exist_ok=True)

        tools: List[Callable] = []
        if all or write_file:
            tools.append(self.write_file)
        if all or read_file:
            tools.append(self.read_file)

        super().__init__(name="local_file_system", tools=tools, **kwargs)

    def check_escape(self, filename: str, directory: Optional[str] = None) -> Tuple[bool, Path]:
        """Check if the file path is within the target directory.

        Args:
            filename: The file name or relative path to check.
            directory: Directory to resolve against. Uses target_directory if not provided.

        Returns:
            Tuple of (is_safe, resolved_path). If not safe, returns target_directory as path.
        """
        relative_path = str(Path(directory) / filename) if directory else filename
        return self._check_path(relative_path, Path(self.target_directory).resolve(), self.restrict_to_base_dir)

    def write_file(
        self,
        content: str,
        filename: Optional[str] = None,
        directory: Optional[str] = None,
        extension: Optional[str] = None,
    ) -> str:
        """Write content to a local file.

        Args:
            content: Content to write to the file.
            filename: Name of the file. Defaults to UUID if not provided.
            directory: Directory to write file to. Uses target_directory if not provided.
            extension: File extension. Uses default_extension if not provided.

        Returns:
            JSON with status and file_path on success.
        """
        try:
            filename = filename or str(uuid4())
            name_path = Path(filename)
            extension = (extension or name_path.suffix.lstrip(".") or self.default_extension).lstrip(".")
            full_name = str(name_path.with_name(f"{name_path.stem}.{extension}"))

            safe, file_path = self.check_escape(full_name, directory)
            if not safe:
                return json.dumps({"error": f"Path '{filename}' is outside the allowed base directory"})

            log_debug(f"Writing file to local system: {file_path.name}")

            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)

            return json.dumps({"status": "success", "file_path": str(file_path)})

        except Exception as e:
            error_msg = f"Failed to write file: {str(e)}"
            log_error(error_msg)
            return json.dumps({"error": error_msg})

    def read_file(self, filename: str, directory: Optional[str] = None) -> str:
        """Read content from a local file.

        Args:
            filename: Name of the file to read.
            directory: Directory to read file from. Uses target_directory if not provided.

        Returns:
            JSON with file_path and content on success.
        """
        try:
            safe, file_path = self.check_escape(filename, directory)
            if not safe:
                return json.dumps({"error": f"Path '{filename}' is outside the allowed base directory"})

            log_debug(f"Reading file from local system: {filename}")

            if not file_path.exists():
                return json.dumps({"error": f"File not found: {file_path}"})

            content = file_path.read_text()
            return json.dumps({"file_path": str(file_path), "content": content})

        except Exception as e:
            error_msg = f"Failed to read file: {str(e)}"
            log_error(error_msg)
            return json.dumps({"error": error_msg})
