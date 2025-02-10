# Copyright (c) 2023-2025 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
"""Module containing input models for routing IS-IS tests."""

from __future__ import annotations

from ipaddress import IPv4Address
from typing import Any, Literal
from warnings import warn

from pydantic import BaseModel, ConfigDict

from anta.custom_types import Interface


class ISISInstance(BaseModel):
    """Model for an IS-IS instance."""

    model_config = ConfigDict(extra="forbid")
    name: str
    """The name of the IS-IS instance."""
    vrf: str = "default"
    """VRF context of the IS-IS instance."""
    dataplane: Literal["MPLS", "mpls", "unset"] = "MPLS"
    """Configured SR data-plane for the IS-IS instance."""
    segments: list[Segment] | None = None
    """List of IS-IS SR segments associated with the instance. Required field in the `VerifyISISSegmentRoutingAdjacencySegments` test."""
    graceful_restart: bool = True
    """Specifies the Graceful Restart,
    Options:
    - True: Default mode, refer as graceful restart is enabled.
    - False: Refer as graceful restart is disabled."""
    graceful_helper: bool = True
    """Specifies the Graceful Restart Helper,
    Options:
    - True: Default mode, refer as graceful restart helper is enabled.
    - False: Refer as graceful restart helper is disabled."""

    def __str__(self) -> str:
        """Return a human-readable string representation of the ISISInstance for reporting."""
        return f"Instance: {self.name} VRF: {self.vrf}"


class Segment(BaseModel):
    """Model for an IS-IS segment."""

    model_config = ConfigDict(extra="forbid")
    interface: Interface
    """Local interface name."""
    level: Literal[1, 2] = 2
    """IS-IS level of the segment."""
    sid_origin: Literal["dynamic", "configured"] = "dynamic"
    """Origin of the segment ID."""
    address: IPv4Address
    """Adjacency IPv4 address of the segment."""

    def __str__(self) -> str:
        """Return a human-readable string representation of the Segment for reporting."""
        return f"Local Intf: {self.interface} Adj IP Address: {self.address}"


class ISISInterface(BaseModel):
    """Model for an IS-IS enabled interface."""

    model_config = ConfigDict(extra="forbid")
    name: Interface
    """Interface name."""
    vrf: str = "default"
    """VRF context of the interface."""
    level: Literal[1, 2] = 2
    """IS-IS level of the interface."""
    count: int | None = None
    """Expected number of IS-IS neighbors on this interface. Required field in the `VerifyISISNeighborCount` test."""
    mode: Literal["point-to-point", "broadcast", "passive"] | None = None
    """IS-IS network type of the interface. Required field in the `VerifyISISInterfaceMode` test."""

    def __str__(self) -> str:
        """Return a human-readable string representation of the ISISInterface for reporting."""
        return f"Interface: {self.name} VRF: {self.vrf} Level: {self.level}"


class InterfaceCount(ISISInterface):  # pragma: no cover
    """Alias for the ISISInterface model to maintain backward compatibility.

    When initialized, it will emit a deprecation warning and call the ISISInterface model.

    TODO: Remove this class in ANTA v2.0.0.
    """

    def __init__(self, **data: Any) -> None:  # noqa: ANN401
        """Initialize the InterfaceCount class, emitting a deprecation warning."""
        warn(
            message="InterfaceCount model is deprecated and will be removed in ANTA v2.0.0. Use the ISISInterface model instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(**data)


class InterfaceState(ISISInterface):  # pragma: no cover
    """Alias for the ISISInterface model to maintain backward compatibility.

    When initialized, it will emit a deprecation warning and call the ISISInterface model.

    TODO: Remove this class in ANTA v2.0.0.
    """

    def __init__(self, **data: Any) -> None:  # noqa: ANN401
        """Initialize the InterfaceState class, emitting a deprecation warning."""
        warn(
            message="InterfaceState model is deprecated and will be removed in ANTA v2.0.0. Use the ISISInterface model instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(**data)


class IsisInstance(ISISInstance):  # pragma: no cover
    """Alias for the ISISInstance model to maintain backward compatibility.

    When initialized, it will emit a deprecation warning and call the ISISInstance model.

    TODO: Remove this class in ANTA v2.0.0.
    """

    def __init__(self, **data: Any) -> None:  # noqa: ANN401
        """Initialize the IsisInstance class, emitting a deprecation warning."""
        warn(
            message="IsisInstance model is deprecated and will be removed in ANTA v2.0.0. Use the ISISInstance model instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(**data)
