# Copyright (c) 2023-2025 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
"""Test inputs for anta.tests.hardware."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any

from anta.models import AntaTest
from anta.result_manager.models import AntaTestStatus
from anta.tests.software import VerifyEOSExtensions, VerifyEOSVersion, VerifyTerminAttrVersion
from tests.units.anta_tests import test

if TYPE_CHECKING:
    from tests.units.anta_tests import AntaUnitTestDataDict

DATA: AntaUnitTestDataDict = {
    (VerifyEOSVersion, "success"): {
        "eos_data": [{"modelName": "vEOS-lab", "internalVersion": "4.27.0F-24305004.4270F", "version": "4.27.0F"}],
        "inputs": {"versions": ["4.27.0F", "4.28.0F"]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyEOSVersion, "failure"): {
        "eos_data": [{"modelName": "vEOS-lab", "internalVersion": "4.27.0F-24305004.4270F", "version": "4.27.0F"}],
        "inputs": {"versions": ["4.27.1F"]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["EOS version mismatch - Actual: 4.27.0F not in Expected: 4.27.1F"]},
    },
    (VerifyTerminAttrVersion, "success"): {
        "eos_data": [
            {
                "imageFormatVersion": "1.0",
                "uptime": 1107543.52,
                "modelName": "vEOS-lab",
                "details": {
                    "deviations": [],
                    "components": [{"name": "Aboot", "version": "Aboot-veos-8.0.0-3255441"}],
                    "switchType": "fixedSystem",
                    "packages": {"TerminAttr-core": {"release": "1", "version": "v1.17.0"}},
                },
            }
        ],
        "inputs": {"versions": ["v1.17.0", "v1.18.1"]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyTerminAttrVersion, "failure"): {
        "eos_data": [
            {
                "imageFormatVersion": "1.0",
                "uptime": 1107543.52,
                "modelName": "vEOS-lab",
                "details": {
                    "deviations": [],
                    "components": [{"name": "Aboot", "version": "Aboot-veos-8.0.0-3255441"}],
                    "switchType": "fixedSystem",
                    "packages": {"TerminAttr-core": {"release": "1", "version": "v1.17.0"}},
                },
            }
        ],
        "inputs": {"versions": ["v1.17.1", "v1.18.1"]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["TerminAttr version mismatch - Actual: v1.17.0 not in Expected: v1.17.1, v1.18.1"]},
    },
    (VerifyEOSExtensions, "success-no-extensions"): {
        "eos_data": [{"extensions": {}, "extensionStoredDir": "flash:", "warnings": ["No extensions are available"]}, {"extensions": []}],
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyEOSExtensions, "success-extensions"): {
        "eos_data": [
            {
                "extensions": {
                    "AristaCloudGateway-1.0.1-1.swix": {
                        "version": "1.0.1",
                        "release": "1",
                        "presence": "present",
                        "status": "installed",
                        "boot": True,
                        "numPackages": 1,
                        "error": False,
                        "vendor": "",
                        "summary": "Arista Cloud Connect",
                        "installedSize": 60532424,
                        "packages": {"AristaCloudGateway-1.0.1-1.x86_64.rpm": {"version": "1.0.1", "release": "1"}},
                        "description": "An extension for Arista Cloud Connect gateway",
                        "affectedAgents": [],
                        "agentsToRestart": [],
                    }
                }
            },
            {"extensions": ["AristaCloudGateway-1.0.1-1.swix"]},
        ],
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyEOSExtensions, "failure"): {
        "eos_data": [
            {
                "extensions": {
                    "AristaCloudGateway-1.0.1-1.swix": {
                        "version": "1.0.1",
                        "release": "1",
                        "presence": "present",
                        "status": "installed",
                        "boot": False,
                        "numPackages": 1,
                        "error": False,
                        "vendor": "",
                        "summary": "Arista Cloud Connect",
                        "installedSize": 60532424,
                        "packages": {"AristaCloudGateway-1.0.1-1.x86_64.rpm": {"version": "1.0.1", "release": "1"}},
                        "description": "An extension for Arista Cloud Connect gateway",
                        "affectedAgents": [],
                        "agentsToRestart": [],
                    }
                }
            },
            {"extensions": []},
        ],
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["EOS extensions mismatch - Installed: AristaCloudGateway-1.0.1-1.swix Configured: Not found"]},
    },
    (VerifyEOSExtensions, "failure-multiple-extensions"): {
        "eos_data": [
            {
                "extensions": {
                    "AristaCloudGateway-1.0.1-1.swix": {
                        "version": "1.0.1",
                        "release": "1",
                        "presence": "present",
                        "status": "installed",
                        "boot": False,
                        "numPackages": 1,
                        "error": False,
                        "vendor": "",
                        "summary": "Arista Cloud Connect",
                        "installedSize": 60532424,
                        "packages": {"AristaCloudGateway-1.0.1-1.x86_64.rpm": {"version": "1.0.1", "release": "1"}},
                        "description": "An extension for Arista Cloud Connect gateway",
                        "affectedAgents": [],
                        "agentsToRestart": [],
                    },
                    "EOS-4.33.0F-NDRSensor.swix": {
                        "version": "4.33.0",
                        "release": "39050855.4330F",
                        "presence": "present",
                        "status": "notInstalled",
                        "boot": True,
                        "numPackages": 9,
                        "error": False,
                        "statusDetail": "No RPMs are compatible with current EOS version.",
                        "vendor": "",
                        "summary": "NDR sensor",
                        "installedSize": 0,
                        "packages": {},
                        "description": "NDR sensor provides libraries to generate flow activity records using DPI\nmetadata and IPFIX flow records.",
                        "affectedAgents": [],
                        "agentsToRestart": [],
                    },
                }
            },
            {"extensions": ["AristaCloudGateway-1.0.1-1.swix", "EOS-4.33.0F-NDRSensor.swix"]},
        ],
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "EOS extensions mismatch - Installed: AristaCloudGateway-1.0.1-1.swix Configured: AristaCloudGateway-1.0.1-1.swix, EOS-4.33.0F-NDRSensor.swix"
            ],
        },
    },
}
