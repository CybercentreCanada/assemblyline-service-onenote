"""Tests for OneNote service"""

from io import BytesIO
import pytest

from pyOneNote.Header import Header

from onenote.onenote import OneNote


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
                ("fcrAllocVerificationFreeChunkList", "FileChunkReference64x32:(stp:0, cb:0)"),
                ("bnCreated", 0),
                ("bnLastWroteToThisFile", 0),
                ("bnOldestWritten", 0),
                ("bnNewestWritten", 0),
            ],
        )
    ],
)
def test_make_header_result(header, section_body_data):
    assert OneNote.make_header_result(header).section_body._data == section_body_data
