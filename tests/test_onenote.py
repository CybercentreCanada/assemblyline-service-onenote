"""Tests for OneNote service"""

import os
import tempfile
from io import BytesIO
from pathlib import Path

import pytest
from pyOneNote.Header import Header

from onenote.file_section import ExtractedFile
from onenote.onenote import OneNote

# pylint: disable=protected-access


@pytest.mark.parametrize(
    "header,section_body_data",
    [
        (
            Header(BytesIO(b"\0" * 1024)),
            [
                ("guidFileType", "00000000-0000-0000-0000-000000000000"),
                ("guidFile", "00000000-0000-0000-0000-000000000000"),
                ("guidLegacyFileVersion", "00000000-0000-0000-0000-000000000000"),
                ("guidFileFormat", "00000000-0000-0000-0000-000000000000"),
                ("ffvLastCodeThatWroteToThisFile", 0),
                ("ffvOldestCodeThatHasWrittenToThisFile", 0),
                ("ffvNewestCodeThatHasWrittenToThisFile", 0),
                ("ffvOldestCodeThatMayReadThisFile", 0),
                ("fcrLegacyFreeChunkList", "FileChunkReference32:(stp:0, cb:0)"),
                ("fcrLegacyTransactionLog", "FileChunkReference32:(stp:0, cb:0)"),
                ("cTransactionsInLog", 0),
                ("cbLegacyExpectedFileLength", 0),
                ("rgbPlaceholder", 0),
                ("fcrLegacyFileNodeListRoot", "FileChunkReference32:(stp:0, cb:0)"),
                ("cbLegacyFreeSpaceInFreeChunkList", 0),
                ("fNeedsDefrag", 0),
                ("fRepairedFile", 0),
                ("fNeedsGarbageCollect", 0),
                ("fHasNoEmbeddedFileObjects", 0),
                ("guidAncestor", "00000000-0000-0000-0000-000000000000"),
                ("crcName", 0),
                ("fcrHashedChunkList", "FileChunkReference64x32:(stp:0, cb:0)"),
                ("fcrTransactionLog", "FileChunkReference64x32:(stp:0, cb:0)"),
                ("fcrFileNodeListRoot", "FileChunkReference64x32:(stp:0, cb:0)"),
                ("fcrFreeChunkList", "FileChunkReference64x32:(stp:0, cb:0)"),
                ("cbExpectedFileLength", 0),
                ("cbFreeSpaceInFreeChunkList", 0),
                ("guidFileVersion", "00000000-0000-0000-0000-000000000000"),
                ("nFileVersionGeneration", 0),
                ("guidDenyReadFileVersion", "00000000-0000-0000-0000-000000000000"),
                ("grfDebugLogFlags", 0),
                ("fcrDebugLog", "FileChunkReference64x32:(stp:0, cb:0)"),
                (
                    "fcrAllocVerificationFreeChunkList",
                    "FileChunkReference64x32:(stp:0, cb:0)",
                ),
                ("bnCreated", 0),
                ("bnLastWroteToThisFile", 0),
                ("bnOldestWritten", 0),
                ("bnNewestWritten", 0),
            ],
        )
    ],
)
def test_make_header_result(header, section_body_data):
    """Test _make_header_result works correctly on a header of all 0 bytes."""
    assert OneNote._make_header_result(header).section_body._data == section_body_data


@pytest.mark.parametrize(
    "files,extracted,supplementary",
    [
        (
            {
                "0ea24ec3-efd6-4c40-86ed-66602bee1dd4": {
                    "extension": ".png",
                    "content": b"pretend this is a png",
                    "identity": "<ExtendedGUID> (0b14d955-917d-45f4-9215-e6481a3aa965, 26)",
                },
                "5098b486-368f-4718-bdd4-46775aede324": {
                    "extension": ".png",
                    "content": b"pretend this is also a png",
                    "identity": "<ExtendedGUID> (13144cb4-a680-08a1-3c45-ed18d2511d1b, 49)",
                },
                "7f92f024-e16d-477a-a7ca-fed5c6280197": {
                    "extension": ".txt",
                    "content": b"Here's a file attachment for testing onenoteanalyzer extraction.",
                    "identity": "<ExtendedGUID> (13144cb4-a680-08a1-3c45-ed18d2511d1b, 48)",
                },
            },
            [
                ("57352850.png", "Embedded file extracted from OneNote"),
                ("13adc23e.png", "Embedded file extracted from OneNote"),
                ("a24798de.txt", "Embedded file extracted from OneNote"),
            ],
            [],
        )
    ],

)
def test_make_file_result(files, extracted, supplementary):
    """Test _make_file_result on dummy data extracted by OnenoteDocument."""

    def compare_file_lists(
        working_directory: str,
        gotten: list[ExtractedFile],
        expected: list[tuple[str, str]],
    ) -> None:
        assert len(gotten) == len(expected)
        for file_, (expected_name, expected_description) in zip(gotten, expected):
            assert file_ == (
                os.path.join(working_directory, expected_name),
                expected_name,
                expected_description,
            )

    with tempfile.TemporaryDirectory() as working_directory:
        file_result = OneNote._make_file_result(files, Path(working_directory))
        compare_file_lists(working_directory, file_result.extracted_files, extracted)
        compare_file_lists(
            working_directory, file_result.supplementary_files, supplementary
        )
