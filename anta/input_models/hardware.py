# Copyright (c) 2025 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
"""Module containing input models for hardware tests."""

from pydantic import BaseModel, ConfigDict, Field


class AdverseDropThresholds(BaseModel):
    """Thresholds for adverse drop counters over various time periods."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    minute: int = Field(default=0, alias="dropInLastMinute", description="Last minute")
    """Threshold for the last minute."""
    ten_minute: int = Field(default=0, alias="dropInLastTenMinute", description="Last 10 minutes")
    """Threshold for the last ten minutes."""
    hour: int = Field(default=0, alias="dropInLastOneHour", description="Last hour")
    """Threshold for the last hour."""
    day: int = Field(default=0, alias="dropInLastOneDay", description="Last day")
    """Threshold for the last day."""
    week: int = Field(default=0, alias="dropInLastOneWeek", description="Last week")
    """Threshold for the last week."""


class PCIeThresholds(BaseModel):
    """Thresholds for PCIe device error counters."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    correctable_errors: int = Field(default=0, alias="correctableErrors", description="Correctable errors")
    """Threshold for correctable errors."""
    non_fatal_errors: int = Field(default=0, alias="nonFatalErrors", description="Non-fatal errors")
    """Threshold for non-fatal errors."""
    fatal_errors: int = Field(default=0, alias="fatalErrors", description="Fatal errors")
    """Threshold for fatal errors."""
