"""Assemblyline OneNote Service"""

from __future__ import annotations

import hashlib
import traceback
from pathlib import Path

from assemblyline_v4_service.common.base import ServiceBase, ServiceRequest
from assemblyline_v4_service.common.result import Result, ResultOrderedKeyValueSection
from pyOneNote.Header import Header
from pyOneNote.OneDocument import OneDocment

from onenote.file_section import ExtractedFile, FileSection


class OneNote(ServiceBase):
    """Assemblyline OneNote Service"""

    def __init__(self, config: dict | None = None) -> None:
        super().__init__(config)

    def execute(self, request: ServiceRequest) -> None:
        with open(request.file_path, "rb") as request_file:
            try:
                document = OneDocment(request_file)
            except OSError:
                self.log.error(
                    f"pyOneNote was unable to open {request.sha256}: "
                    f"{traceback.format_exc(limit=2)}"
                )
            else:
                request.result = Result(
                    [
                        self._make_header_result(document.header),
                        self._make_file_result(
                            document.get_files(), Path(self.working_directory)
                        ).as_result_section(request),
                    ]
                )

    @staticmethod
    def _make_header_result(header: Header) -> ResultOrderedKeyValueSection:
        """Return a ResultSection with the header info"""
        return ResultOrderedKeyValueSection(
            "OneNote Document Header", body=header.convert_to_dictionary()
        )

    @staticmethod
    def _make_file_result(files: dict, directory: Path) -> FileSection:
        """Make a result for embedded files"""
        section = FileSection("Embedded Files", [], [])
        for _, file_node in files.items():
            if not isinstance(file_node, dict):
                continue
            if "content" not in file_node:
                continue
            content = file_node["content"]
            name = hashlib.sha256(content).hexdigest()[0:8] + file_node.get(
                "extension", ""
            )
            path = directory / name
            with open(path, "wb") as f:
                f.write(content)
            section.extracted_files.append(
                ExtractedFile(str(path), name, "Embedded file extracted from OneNote")
            )
        return section
