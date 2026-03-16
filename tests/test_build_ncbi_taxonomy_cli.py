"""Unit checks for the taxonomy build CLI helper behavior."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from taxonomy_tools.build_ncbi_taxonomy import download_taxdump


class BuildNcbiTaxonomyCliTests(unittest.TestCase):
    """Validate the optional download helper without making network calls."""

    def test_download_taxdump_writes_response_bytes_to_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "downloads" / "taxdump.tar.gz"
            payload = b"fake-tarball-bytes"

            with patch(
                "taxonomy_tools.build_ncbi_taxonomy.urllib.request.urlopen",
                return_value=_FakeResponse(payload),
            ):
                download_taxdump("https://example.invalid/taxdump.tar.gz", destination)

            self.assertEqual(destination.read_bytes(), payload)


class _FakeResponse:
    """Minimal context manager used to stub urllib responses in tests."""

    def __init__(self, payload: bytes) -> None:
        self._payload = payload
        self._offset = 0

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def read(self, size: int = -1) -> bytes:
        """Provide a file-like read interface for `shutil.copyfileobj`."""

        if size == -1:
            size = len(self._payload) - self._offset
        start = self._offset
        end = min(len(self._payload), self._offset + size)
        self._offset = end
        return self._payload[start:end]
