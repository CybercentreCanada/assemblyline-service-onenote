"""

"""
from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple

from assemblyline_v4_service.common.request import ServiceRequest
from assemblyline_v4_service.common.result import ResultSection


class ExtractedFile(NamedTuple):
    """Files to be extracted"""

    path: str
    name: str
    description: str


@dataclass()
class FileSection:
    """ResultSection mock with file data attached"""

    title: str
    extracted_files: list[ExtractedFile]
    supplementary_files: list[ExtractedFile]

    def as_result_section(self, request: ServiceRequest) -> ResultSection:
        """Convert to ResultSection"""
        for extracted_file in self.extracted_files:
            request.add_extracted(*extracted_file)
        for supplementary_file in self.supplementary_files:
            request.add_supplementary(*supplementary_file)

        return ResultSection(
            self.title,
            body="\n".join(extracted_file.name for extracted_file in self.extracted_files),
        )
