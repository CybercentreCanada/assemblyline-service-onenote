"""Assemblyline OneNote Service"""

from __future__ import annotations

from assemblyline_v4_service.common.base import ServiceBase, ServiceRequest
from assemblyline_v4_service.common.result import Result, ResultOrderedKeyValueSection
from pyOneNote.OneDocument import OneDocment
from pyOneNote.Header import Header


class OneNote(ServiceBase):
    """Assemblyline OneNote Service"""
    def __init__(self, config: dict | None = None) -> None:
        super().__init__(config)

    def execute(self, request: ServiceRequest) -> None:
        request.result = Result()
        with open(request.file_path, 'rb') as request_file:
            document = OneDocment(request_file)
            header_result = self.make_header_result(document.header)
            request.result.add_section(header_result)

    @staticmethod
    def make_header_result(header: Header) -> ResultOrderedKeyValueSection:
        """Return a ResultSection with the header info"""
        return ResultOrderedKeyValueSection("OneNote Document Header", body=header.convert_to_dictionary())
