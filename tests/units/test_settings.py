# Copyright (c) 2023-2025 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
"""Unit tests for the anta.settings module."""

from __future__ import annotations

import logging
import os
import sys
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from anta.settings import DEFAULT_MAX_CONCURRENCY, DEFAULT_NOFILE, AntaRunnerSettings

if os.name == "posix":
    # The function is not defined on non-POSIX system
    import resource


class TestAntaRunnerSettings:
    """Tests for the AntaRunnerSettings class."""

    def test_defaults(self, setenvvar: pytest.MonkeyPatch) -> None:
        """Test defaults for ANTA runner settings."""
        settings = AntaRunnerSettings()
        assert settings.nofile == DEFAULT_NOFILE
        assert settings.max_concurrency == DEFAULT_MAX_CONCURRENCY

    def test_env_var(self, setenvvar: pytest.MonkeyPatch) -> None:
        """Test setting different ANTA runner settings."""
        setenvvar.setenv("ANTA_NOFILE", "20480")
        settings = AntaRunnerSettings()
        assert settings.nofile == 20480
        assert settings.max_concurrency == DEFAULT_MAX_CONCURRENCY

    def test_validation(self, setenvvar: pytest.MonkeyPatch) -> None:
        """Test validation of ANTA runner settings."""
        setenvvar.setenv("ANTA_NOFILE", "-1")
        with pytest.raises(ValidationError):
            AntaRunnerSettings()

        setenvvar.setenv("ANTA_MAX_CONCURRENCY", "0")
        with pytest.raises(ValidationError):
            AntaRunnerSettings()

    @pytest.mark.skipif(os.name == "posix", reason="Run this test on Windows only")
    def test_file_descriptor_limit_windows(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test file_descriptor_limit on Windows."""
        caplog.set_level(logging.INFO)
        settings = AntaRunnerSettings()
        assert settings.file_descriptor_limit == sys.maxsize
        assert "Running on a non-POSIX system, cannot adjust the maximum number of file descriptors." in caplog.text

    @pytest.mark.skipif(os.name != "posix", reason="Fake non-posix for coverage")
    async def test_file_descriptor_limit_fake_windows(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test file_descriptor_limit on fake Windows."""
        caplog.set_level(logging.INFO)
        with patch("os.name", new="win32"):
            settings = AntaRunnerSettings()
            assert settings.file_descriptor_limit == sys.maxsize
            assert "Running on a non-POSIX system, cannot adjust the maximum number of file descriptors." in caplog.records[0].message

    @pytest.mark.skipif(os.name != "posix", reason="Cannot run this test on Windows")
    def test_file_descriptor_limit_posix(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test file_descriptor_limit on POSIX systems."""
        with (
            caplog.at_level(logging.DEBUG),
            patch.dict("os.environ", {"ANTA_NOFILE": "20480"}),
            patch("resource.getrlimit") as getrlimit_mock,
            patch("resource.setrlimit") as setrlimit_mock,
        ):
            # Simulate the default system limits
            system_limits = (8192, 1048576)

            # Setup getrlimit mock return value
            getrlimit_mock.return_value = system_limits

            # Simulate setrlimit behavior
            def side_effect_setrlimit(_resource_id: int, limits: tuple[int, int]) -> None:
                getrlimit_mock.return_value = (limits[0], limits[1])

            setrlimit_mock.side_effect = side_effect_setrlimit

            settings = AntaRunnerSettings()

            # Assert the limits were updated as expected
            assert settings.file_descriptor_limit == 20480
            assert "Initial file descriptor limits for the current ANTA process: Soft Limit: 8192 | Hard Limit: 1048576" in caplog.text
            assert "Setting file descriptor soft limit to 20480" in caplog.text

            setrlimit_mock.assert_called_once_with(resource.RLIMIT_NOFILE, (20480, 1048576))  # pylint: disable=possibly-used-before-assignment

    @pytest.mark.skipif(os.name != "posix", reason="Cannot run this test on Windows")
    def test_file_descriptor_limit_value_error(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test file_descriptor_limit with invalid environment variables."""
        with (
            caplog.at_level(logging.DEBUG),
            patch.dict("os.environ", {"ANTA_NOFILE": "666"}),
            patch("resource.getrlimit") as getrlimit_mock,
            patch("resource.setrlimit") as setrlimit_mock,
        ):
            # Simulate the default system limits
            system_limits = (32768, 131072)

            # Setup getrlimit mock return value
            getrlimit_mock.return_value = system_limits

            # Simulate setrlimit behavior raising ValueError
            def side_effect_setrlimit(_resource_id: int, _limits: tuple[int, int]) -> None:
                msg = "not allowed to raise maximum limit"
                raise ValueError(msg)

            setrlimit_mock.side_effect = side_effect_setrlimit

            settings = AntaRunnerSettings()

            # Assert the limits were *NOT* updated as expected
            assert settings.file_descriptor_limit == 32768
            assert "Initial file descriptor limits for the current ANTA process: Soft Limit: 32768 | Hard Limit: 131072" in caplog.text
            assert caplog.records[-1].levelname == "WARNING"
            assert "Failed to set file descriptor soft limit for the current ANTA process" in caplog.records[-1].getMessage()

            setrlimit_mock.assert_called_once_with(resource.RLIMIT_NOFILE, (666, 131072))
