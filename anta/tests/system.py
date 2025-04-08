# Copyright (c) 2023-2025 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
"""Module related to system-level features and protocols tests."""

# Mypy does not understand AntaTest.Input typing
# mypy: disable-error-code=attr-defined
from __future__ import annotations

import re
from enum import Enum
from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import Field, model_validator

from anta.custom_types import Hostname, PositiveInteger
from anta.input_models.system import NTPPool, NTPServer
from anta.models import AntaCommand, AntaTest
from anta.tools import get_value

if TYPE_CHECKING:
    import sys
    from ipaddress import IPv4Address

    from anta.models import AntaTemplate

    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self

CPU_IDLE_THRESHOLD = 25
MEMORY_THRESHOLD = 0.25
DISK_SPACE_THRESHOLD = 75


class ReloadCauses(str, Enum):
    """Represents different causes of reloads as immutable string values."""

    USER = "Reload requested by the user."
    FPGA = "Reload requested after FPGA upgrade"
    ZTP = "System reloaded due to Zero Touch Provisioning"


class VerifyUptime(AntaTest):
    """Verifies the device uptime.

    Expected Results
    ----------------
    * Success: The test will pass if the device uptime is higher than the provided value.
    * Failure: The test will fail if the device uptime is lower than the provided value.

    Examples
    --------
    ```yaml
    anta.tests.system:
      - VerifyUptime:
          minimum: 86400
    ```
    """

    categories: ClassVar[list[str]] = ["system"]
    commands: ClassVar[list[AntaCommand | AntaTemplate]] = [AntaCommand(command="show uptime", revision=1)]

    class Input(AntaTest.Input):
        """Input model for the VerifyUptime test."""

        minimum: PositiveInteger
        """Minimum uptime in seconds."""

    @AntaTest.anta_test
    def test(self) -> None:
        """Main test function for VerifyUptime."""
        self.result.is_success()
        command_output = self.instance_commands[0].json_output
        if command_output["upTime"] < self.inputs.minimum:
            self.result.is_failure(f"Device uptime is incorrect - Expected: {self.inputs.minimum}s Actual: {command_output['upTime']}s")


class VerifyReloadCause(AntaTest):
    """Verifies the last reload cause of the device.

    Expected Results
    ----------------
    * Success: The test passes if there are no reload causes, or if the last reload was user-initiated, after an FPGA upgrade, or caused by Zero Touch Provisioning.
    * Failure: The test will fail if the last reload was NOT caused by the user or after an FPGA upgrade or due to Zero Touch Provisioning.
    * Error: The test will report an error if the reload cause is NOT available.

    Examples
    --------
    ```yaml
    anta.tests.system:
      - VerifyReloadCause:
        allowed_causes:
          - ZTP
    ```
    """

    categories: ClassVar[list[str]] = ["system"]
    commands: ClassVar[list[AntaCommand | AntaTemplate]] = [AntaCommand(command="show reload cause", revision=1)]

    class Input(AntaTest.Input):
        """Input model for the VerifyReloadCause test."""

        allowed_causes: list[str] = Field(default=["USER", "FPGA"])
        """Minimum uptime in seconds."""

    @AntaTest.anta_test
    def test(self) -> None:
        """Main test function for VerifyReloadCause."""
        command_output = self.instance_commands[0].json_output
        if len(command_output["resetCauses"]) == 0:
            # No reload causes
            self.result.is_success()
            return
        reset_causes = command_output["resetCauses"]
        command_output_data = reset_causes[0].get("description")
        reload_causes = [cause.value for allowed_causes in self.inputs.allowed_causes if (cause := getattr(ReloadCauses, allowed_causes, None))]
        if command_output_data in reload_causes:
            self.result.is_success()
        else:
            self.result.is_failure(f"Reload cause is: {command_output_data}")


class VerifyCoredump(AntaTest):
    """Verifies there are no core dump files.

    Expected Results
    ----------------
    * Success: The test will pass if there are NO core dump(s) in /var/core.
    * Failure: The test will fail if there are core dump(s) in /var/core.

    Notes
    -----
    * This test will NOT check for minidump(s) generated by certain agents in /var/core/minidump.

    Examples
    --------
    ```yaml
    anta.tests.system:
      - VerifyCoredump:
    ```
    """

    categories: ClassVar[list[str]] = ["system"]
    commands: ClassVar[list[AntaCommand | AntaTemplate]] = [AntaCommand(command="show system coredump", revision=1)]

    @AntaTest.anta_test
    def test(self) -> None:
        """Main test function for VerifyCoredump."""
        command_output = self.instance_commands[0].json_output
        core_files = command_output["coreFiles"]
        if "minidump" in core_files:
            core_files.remove("minidump")
        if not core_files:
            self.result.is_success()
        else:
            self.result.is_failure(f"Core dump(s) have been found: {', '.join(core_files)}")


class VerifyAgentLogs(AntaTest):
    """Verifies there are no agent crash reports.

    Expected Results
    ----------------
    * Success: The test will pass if there is NO agent crash reported.
    * Failure: The test will fail if any agent crashes are reported.

    Examples
    --------
    ```yaml
    anta.tests.system:
      - VerifyAgentLogs:
    ```
    """

    categories: ClassVar[list[str]] = ["system"]
    commands: ClassVar[list[AntaCommand | AntaTemplate]] = [AntaCommand(command="show agent logs crash", ofmt="text")]

    @AntaTest.anta_test
    def test(self) -> None:
        """Main test function for VerifyAgentLogs."""
        command_output = self.instance_commands[0].text_output
        if len(command_output) == 0:
            self.result.is_success()
        else:
            pattern = re.compile(r"^===> (.*?) <===$", re.MULTILINE)
            agents = "\n * ".join(pattern.findall(command_output))
            self.result.is_failure(f"Device has reported agent crashes:\n * {agents}")


class VerifyCPUUtilization(AntaTest):
    """Verifies whether the CPU utilization is below 75%.

    Expected Results
    ----------------
    * Success: The test will pass if the CPU utilization is below 75%.
    * Failure: The test will fail if the CPU utilization is over 75%.

    Examples
    --------
    ```yaml
    anta.tests.system:
      - VerifyCPUUtilization:
    ```
    """

    categories: ClassVar[list[str]] = ["system"]
    commands: ClassVar[list[AntaCommand | AntaTemplate]] = [AntaCommand(command="show processes top once", revision=1)]

    @AntaTest.anta_test
    def test(self) -> None:
        """Main test function for VerifyCPUUtilization."""
        self.result.is_success()
        command_output = self.instance_commands[0].json_output
        command_output_data = command_output["cpuInfo"]["%Cpu(s)"]["idle"]
        if command_output_data < CPU_IDLE_THRESHOLD:
            self.result.is_failure(f"Device has reported a high CPU utilization -  Expected: < 75% Actual: {100 - command_output_data}%")


class VerifyMemoryUtilization(AntaTest):
    """Verifies whether the memory utilization is below 75%.

    Expected Results
    ----------------
    * Success: The test will pass if the memory utilization is below 75%.
    * Failure: The test will fail if the memory utilization is over 75%.

    Examples
    --------
    ```yaml
    anta.tests.system:
      - VerifyMemoryUtilization:
    ```
    """

    categories: ClassVar[list[str]] = ["system"]
    commands: ClassVar[list[AntaCommand | AntaTemplate]] = [AntaCommand(command="show version", revision=1)]

    @AntaTest.anta_test
    def test(self) -> None:
        """Main test function for VerifyMemoryUtilization."""
        self.result.is_success()
        command_output = self.instance_commands[0].json_output
        memory_usage = command_output["memFree"] / command_output["memTotal"]
        if memory_usage < MEMORY_THRESHOLD:
            self.result.is_failure(f"Device has reported a high memory usage - Expected: < 75% Actual: {(1 - memory_usage) * 100:.2f}%")


class VerifyFileSystemUtilization(AntaTest):
    """Verifies that no partition is utilizing more than 75% of its disk space.

    Expected Results
    ----------------
    * Success: The test will pass if all partitions are using less than 75% of its disk space.
    * Failure: The test will fail if any partitions are using more than 75% of its disk space.

    Examples
    --------
    ```yaml
    anta.tests.system:
      - VerifyFileSystemUtilization:
    ```
    """

    categories: ClassVar[list[str]] = ["system"]
    commands: ClassVar[list[AntaCommand | AntaTemplate]] = [AntaCommand(command="bash timeout 10 df -h", ofmt="text")]

    @AntaTest.anta_test
    def test(self) -> None:
        """Main test function for VerifyFileSystemUtilization."""
        command_output = self.instance_commands[0].text_output
        self.result.is_success()
        for line in command_output.split("\n")[1:]:
            if "loop" not in line and len(line) > 0 and (percentage := int(line.split()[4].replace("%", ""))) > DISK_SPACE_THRESHOLD:
                self.result.is_failure(f"Mount point: {line} - Higher disk space utilization - Expected: {DISK_SPACE_THRESHOLD}% Actual: {percentage}%")


class VerifyNTP(AntaTest):
    """Verifies if NTP is synchronised.

    Expected Results
    ----------------
    * Success: The test will pass if the NTP is synchronised.
    * Failure: The test will fail if the NTP is NOT synchronised.

    Examples
    --------
    ```yaml
    anta.tests.system:
      - VerifyNTP:
    ```
    """

    categories: ClassVar[list[str]] = ["system"]
    commands: ClassVar[list[AntaCommand | AntaTemplate]] = [AntaCommand(command="show ntp status", ofmt="text")]

    @AntaTest.anta_test
    def test(self) -> None:
        """Main test function for VerifyNTP."""
        command_output = self.instance_commands[0].text_output
        if command_output.split("\n")[0].split(" ")[0] == "synchronised":
            self.result.is_success()
        else:
            data = command_output.split("\n")[0]
            self.result.is_failure(f"NTP status mismatch - Expected: synchronised Actual: {data}")


class VerifyNTPAssociations(AntaTest):
    """Verifies the Network Time Protocol (NTP) associations.

    This test performs the following checks:

      1. For the NTP servers:
        - The primary NTP server (marked as preferred) has the condition 'sys.peer'.
        - All other NTP servers have the condition 'candidate'.
        - All the NTP servers have the expected stratum level.
      2. For the NTP servers pool:
        - All the NTP servers belong to the specified NTP pool.
        - All the NTP servers have valid condition (sys.peer | candidate).
        - All the NTP servers have the stratum level within the specified startum level.

    Expected Results
    ----------------
    * Success: The test will pass if all the NTP servers meet the expected state.
    * Failure: The test will fail if any of the NTP server does not meet the expected state.

    Examples
    --------
    ```yaml
    anta.tests.system:
      - VerifyNTPAssociations:
          ntp_servers:
            - server_address: 1.1.1.1
              preferred: True
              stratum: 1
            - server_address: 2.2.2.2
              stratum: 2
            - server_address: 3.3.3.3
              stratum: 2
      - VerifyNTPAssociations:
          ntp_pool:
            server_addresses: [1.1.1.1, 2.2.2.2]
            preferred_stratum_range: [1,3]
    ```
    """

    categories: ClassVar[list[str]] = ["system"]
    commands: ClassVar[list[AntaCommand | AntaTemplate]] = [AntaCommand(command="show ntp associations")]

    class Input(AntaTest.Input):
        """Input model for the VerifyNTPAssociations test."""

        ntp_servers: list[NTPServer] | None = None
        """List of NTP servers."""
        ntp_pool: NTPPool | None = None
        """NTP servers pool."""
        NTPServer: ClassVar[type[NTPServer]] = NTPServer

        @model_validator(mode="after")
        def validate_inputs(self) -> Self:
            """Validate the inputs provided to the VerifyNTPAssociations test.

            Either `ntp_servers` or `ntp_pool` can be provided at the same time.
            """
            if not self.ntp_servers and not self.ntp_pool:
                msg = "'ntp_servers' or 'ntp_pool' must be provided"
                raise ValueError(msg)
            if self.ntp_servers and self.ntp_pool:
                msg = "Either 'ntp_servers' or 'ntp_pool' can be provided at the same time"
                raise ValueError(msg)

            # Verifies the len of preferred_stratum_range in NTP Pool should be 2 as this is the range.
            stratum_range = 2
            if self.ntp_pool and len(self.ntp_pool.preferred_stratum_range) > stratum_range:
                msg = "'preferred_stratum_range' list should have at most 2 items"
                raise ValueError(msg)
            return self

    def _validate_ntp_server(self, ntp_server: NTPServer, peers: dict[str, Any]) -> list[str]:
        """Validate the NTP server, condition and stratum level."""
        failure_msgs: list[str] = []
        server_address = str(ntp_server.server_address)

        # We check `peerIpAddr` in the peer details - covering IPv4Address input, or the peer key - covering Hostname input.
        matching_peer = next((peer for peer, peer_details in peers.items() if (server_address in {peer_details["peerIpAddr"], peer})), None)

        if not matching_peer:
            failure_msgs.append(f"{ntp_server} - Not configured")
            return failure_msgs

        # Collecting the expected/actual NTP peer details.
        exp_condition = "sys.peer" if ntp_server.preferred else "candidate"
        exp_stratum = ntp_server.stratum
        act_condition = get_value(peers[matching_peer], "condition")
        act_stratum = get_value(peers[matching_peer], "stratumLevel")

        if act_condition != exp_condition:
            failure_msgs.append(f"{ntp_server} - Incorrect condition - Expected: {exp_condition} Actual: {act_condition}")

        if act_stratum != exp_stratum:
            failure_msgs.append(f"{ntp_server} - Incorrect stratum level - Expected: {exp_stratum} Actual: {act_stratum}")

        return failure_msgs

    def _validate_ntp_pool(self, server_addresses: list[Hostname | IPv4Address], peer: str, stratum_range: list[int], peer_details: dict[str, Any]) -> list[str]:
        """Validate the NTP server pool, condition and stratum level."""
        failure_msgs: list[str] = []

        # We check `peerIpAddr` and `peer` in the peer details - covering server_addresses input
        if (peer_ip := peer_details["peerIpAddr"]) not in server_addresses and peer not in server_addresses:
            failure_msgs.append(f"NTP Server: {peer_ip} Hostname: {peer} - Associated but not part of the provided NTP pool")
            return failure_msgs

        act_condition = get_value(peer_details, "condition")
        act_stratum = get_value(peer_details, "stratumLevel")

        if act_condition not in ["sys.peer", "candidate"]:
            failure_msgs.append(f"NTP Server: {peer_ip} Hostname: {peer} - Incorrect condition  - Expected: sys.peer, candidate Actual: {act_condition}")

        if int(act_stratum) not in range(stratum_range[0], stratum_range[1] + 1):
            msg = f"Expected Stratum Range: {stratum_range[0]} to {stratum_range[1]} Actual: {act_stratum}"
            failure_msgs.append(f"NTP Server: {peer_ip} Hostname: {peer} - Incorrect stratum level - {msg}")

        return failure_msgs

    @AntaTest.anta_test
    def test(self) -> None:
        """Main test function for VerifyNTPAssociations."""
        self.result.is_success()

        if not (peers := get_value(self.instance_commands[0].json_output, "peers")):
            self.result.is_failure("No NTP peers configured")
            return

        if self.inputs.ntp_servers:
            # Iterate over each NTP server.
            for ntp_server in self.inputs.ntp_servers:
                failure_msgs = self._validate_ntp_server(ntp_server, peers)
                for msg in failure_msgs:
                    self.result.is_failure(msg)
            return

        # Verifies the NTP pool details
        server_addresses = self.inputs.ntp_pool.server_addresses
        exp_stratum_range = self.inputs.ntp_pool.preferred_stratum_range
        for peer, peer_details in peers.items():
            failure_msgs = self._validate_ntp_pool(server_addresses, peer, exp_stratum_range, peer_details)
            for msg in failure_msgs:
                self.result.is_failure(msg)


class VerifyMaintenance(AntaTest):
    """Verifies that the device is not currently under or entering maintenance.

    Expected Results
    ----------------
    * Success: The test will pass if the device is not under or entering maintenance.
    * Failure: The test will fail if the device is under or entering maintenance.

    Examples
    --------
    ```yaml
    anta.tests.system:
      - VerifyMaintenance:
    ```
    """

    categories: ClassVar[list[str]] = ["system"]
    commands: ClassVar[list[AntaCommand | AntaTemplate]] = [AntaCommand(command="show maintenance", revision=1)]

    @AntaTest.anta_test
    def test(self) -> None:
        """Main test function for VerifyMaintenance."""
        self.result.is_success()

        # If units is not empty we have to examine the output for details.
        if not (units := get_value(self.instance_commands[0].json_output, "units")):
            return
        units_under_maintenance = [unit for unit, info in units.items() if info["state"] == "underMaintenance"]
        units_entering_maintenance = [unit for unit, info in units.items() if info["state"] == "maintenanceModeEnter"]
        causes = set()
        # Iterate over units, check for units under or entering maintenance, and examine the causes.
        for info in units.values():
            if info["adminState"] == "underMaintenance":
                causes.add("Quiesce is configured")
            if info["onBootMaintenance"]:
                causes.add("On-boot maintenance is configured")
            if info["intfsViolatingTrafficThreshold"]:
                causes.add("Interface traffic threshold violation")

        # Building the error message.
        if units_under_maintenance:
            self.result.is_failure(f"Units under maintenance: '{', '.join(units_under_maintenance)}'")
        if units_entering_maintenance:
            self.result.is_failure(f"Units entering maintenance: '{', '.join(units_entering_maintenance)}'")
        if causes:
            self.result.is_failure(f"Possible causes: '{', '.join(sorted(causes))}'")
