# Copyright (c) 2023-2025 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
"""Tests for anta.tests.routing.bgp.py."""

# pylint: disable=C0302
from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any

import pytest

from anta.input_models.routing.bgp import BgpAddressFamily
from anta.models import AntaTest
from anta.result_manager.models import AntaTestStatus
from anta.tests.routing.bgp import (
    VerifyBGPAdvCommunities,
    VerifyBGPExchangedRoutes,
    VerifyBGPNlriAcceptance,
    VerifyBGPPeerASNCap,
    VerifyBGPPeerCount,
    VerifyBGPPeerDropStats,
    VerifyBGPPeerGroup,
    VerifyBGPPeerMD5Auth,
    VerifyBGPPeerMPCaps,
    VerifyBGPPeerRouteLimit,
    VerifyBGPPeerRouteRefreshCap,
    VerifyBGPPeerSession,
    VerifyBGPPeerSessionRibd,
    VerifyBGPPeersHealth,
    VerifyBGPPeersHealthRibd,
    VerifyBGPPeerTtlMultiHops,
    VerifyBGPPeerUpdateErrors,
    VerifyBGPRedistribution,
    VerifyBGPRouteECMP,
    VerifyBgpRouteMaps,
    VerifyBGPRoutePaths,
    VerifyBGPSpecificPeers,
    VerifyBGPTimers,
    VerifyEVPNType2Route,
    _check_bgp_neighbor_capability,
)
from tests.units.anta_tests import test

if TYPE_CHECKING:
    from tests.units.anta_tests import AntaUnitTestDataDict


@pytest.mark.parametrize(
    ("input_dict", "expected"),
    [
        pytest.param({"advertised": True, "received": True, "enabled": True}, True, id="all True"),
        pytest.param({"advertised": False, "received": True, "enabled": True}, False, id="advertised False"),
        pytest.param({"advertised": True, "received": False, "enabled": True}, False, id="received False"),
        pytest.param({"advertised": True, "received": True, "enabled": False}, False, id="enabled False"),
        pytest.param({"advertised": True, "received": True}, False, id="missing enabled"),
        pytest.param({}, False),
    ],
)
def test_check_bgp_neighbor_capability(input_dict: dict[str, bool], expected: bool) -> None:
    """Test check_bgp_neighbor_capability."""
    assert _check_bgp_neighbor_capability(input_dict) == expected


DATA: AntaUnitTestDataDict = {
    (VerifyBGPPeerCount, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.0.1": {
                                "peerState": "Idle",
                                "peerAsn": "65100",
                                "ipv4Unicast": {"afiSafiState": "advertised", "nlrisReceived": 0, "nlrisAccepted": 0},
                                "l2VpnEvpn": {"afiSafiState": "negotiated", "nlrisReceived": 42, "nlrisAccepted": 42},
                            },
                            "10.1.0.2": {
                                "peerState": "Idle",
                                "peerAsn": "65100",
                                "ipv4Unicast": {"afiSafiState": "advertised", "nlrisReceived": 0, "nlrisAccepted": 0},
                                "l2VpnEvpn": {"afiSafiState": "negotiated", "nlrisReceived": 42, "nlrisAccepted": 42},
                            },
                        },
                    },
                    "DEV": {
                        "vrf": "DEV",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.254.1": {
                                "peerState": "Idle",
                                "peerAsn": "65120",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 4, "nlrisAccepted": 4},
                            }
                        },
                    },
                }
            }
        ],
        "inputs": {
            "address_families": [
                {"afi": "evpn", "num_peers": 2},
                {"afi": "ipv4", "safi": "unicast", "vrf": "default", "num_peers": 2},
                {"afi": "ipv4", "safi": "unicast", "vrf": "DEV", "num_peers": 1},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerCount, "success-peer-state-check-true"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.0.1": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4MplsVpn": {"afiSafiState": "advertised", "nlrisReceived": 0, "nlrisAccepted": 0},
                                "l2VpnEvpn": {"afiSafiState": "negotiated", "nlrisReceived": 42, "nlrisAccepted": 42},
                            },
                            "10.1.0.2": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4MplsVpn": {"afiSafiState": "advertised", "nlrisReceived": 0, "nlrisAccepted": 0},
                                "l2VpnEvpn": {"afiSafiState": "negotiated", "nlrisReceived": 42, "nlrisAccepted": 42},
                            },
                            "10.1.254.1": {
                                "peerState": "Established",
                                "peerAsn": "65120",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 17, "nlrisAccepted": 17},
                            },
                            "10.1.255.0": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 14, "nlrisAccepted": 14},
                            },
                            "10.1.255.2": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 14, "nlrisAccepted": 14},
                            },
                        },
                    },
                    "DEV": {
                        "vrf": "DEV",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.254.1": {
                                "peerState": "Established",
                                "peerAsn": "65120",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 4, "nlrisAccepted": 4},
                            }
                        },
                    },
                }
            }
        ],
        "inputs": {
            "address_families": [
                {"afi": "evpn", "num_peers": 2, "check_peer_state": True},
                {"afi": "ipv4", "safi": "unicast", "vrf": "default", "num_peers": 3, "check_peer_state": True},
                {"afi": "ipv4", "safi": "unicast", "vrf": "DEV", "num_peers": 1, "check_peer_state": True},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerCount, "failure-vrf-not-configured"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.0.1": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4MplsVpn": {"afiSafiState": "advertised", "nlrisReceived": 0, "nlrisAccepted": 0},
                                "l2VpnEvpn": {"afiSafiState": "negotiated", "nlrisReceived": 42, "nlrisAccepted": 42},
                            },
                            "10.1.0.2": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4MplsVpn": {"afiSafiState": "advertised", "nlrisReceived": 0, "nlrisAccepted": 0},
                                "l2VpnEvpn": {"afiSafiState": "negotiated", "nlrisReceived": 42, "nlrisAccepted": 42},
                            },
                            "10.1.254.1": {
                                "peerState": "Established",
                                "peerAsn": "65120",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 17, "nlrisAccepted": 17},
                            },
                            "10.1.255.0": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 14, "nlrisAccepted": 14},
                            },
                            "10.1.255.2": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 14, "nlrisAccepted": 14},
                            },
                        },
                    },
                    "DEV": {
                        "vrf": "DEV",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.254.1": {
                                "peerState": "Established",
                                "peerAsn": "65120",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 4, "nlrisAccepted": 4},
                            }
                        },
                    },
                }
            }
        ],
        "inputs": {
            "address_families": [
                {"afi": "evpn", "num_peers": 2, "check_peer_state": True},
                {"afi": "ipv4", "safi": "unicast", "vrf": "default", "num_peers": 3, "check_peer_state": True},
                {"afi": "ipv4", "safi": "unicast", "vrf": "PROD", "num_peers": 2, "check_peer_state": True},
            ]
        },
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["AFI: ipv4 SAFI: unicast VRF: PROD - VRF not configured"]},
    },
    (VerifyBGPPeerCount, "failure-peer-state-check-true"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.0.1": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4MplsVpn": {"afiSafiState": "advertised", "nlrisReceived": 0, "nlrisAccepted": 0},
                                "l2VpnEvpn": {"afiSafiState": "negotiated", "nlrisReceived": 42, "nlrisAccepted": 42},
                            },
                            "10.1.0.2": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4MplsVpn": {"afiSafiState": "advertised", "nlrisReceived": 0, "nlrisAccepted": 0},
                                "l2VpnEvpn": {"afiSafiState": "negotiated", "nlrisReceived": 42, "nlrisAccepted": 42},
                            },
                            "10.1.254.1": {
                                "peerState": "Established",
                                "peerAsn": "65120",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 17, "nlrisAccepted": 17},
                            },
                            "10.1.255.0": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 14, "nlrisAccepted": 14},
                            },
                            "10.1.255.2": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 14, "nlrisAccepted": 14},
                            },
                        },
                    },
                    "DEV": {
                        "vrf": "DEV",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.254.1": {
                                "peerState": "Established",
                                "peerAsn": "65120",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 4, "nlrisAccepted": 4},
                            }
                        },
                    },
                }
            }
        ],
        "inputs": {
            "address_families": [
                {"afi": "evpn", "num_peers": 2, "check_peer_state": True},
                {"afi": "vpn-ipv4", "num_peers": 2, "check_peer_state": True},
                {"afi": "ipv4", "safi": "unicast", "vrf": "default", "num_peers": 3, "check_peer_state": True},
                {"afi": "ipv4", "safi": "unicast", "vrf": "DEV", "num_peers": 1, "check_peer_state": True},
            ]
        },
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["AFI: vpn-ipv4 - Peer count mismatch - Expected: 2 Actual: 0"]},
    },
    (VerifyBGPPeerCount, "failure-wrong-count-peer-state-check-true"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.0.1": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4MplsVpn": {"afiSafiState": "advertised", "nlrisReceived": 0, "nlrisAccepted": 0},
                                "l2VpnEvpn": {"afiSafiState": "negotiated", "nlrisReceived": 42, "nlrisAccepted": 42},
                            },
                            "10.1.0.2": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4MplsVpn": {"afiSafiState": "advertised", "nlrisReceived": 0, "nlrisAccepted": 0},
                                "l2VpnEvpn": {"afiSafiState": "negotiated", "nlrisReceived": 42, "nlrisAccepted": 42},
                            },
                            "10.1.254.1": {
                                "peerState": "Established",
                                "peerAsn": "65120",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 17, "nlrisAccepted": 17},
                            },
                            "10.1.255.0": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 14, "nlrisAccepted": 14},
                            },
                            "10.1.255.2": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 14, "nlrisAccepted": 14},
                            },
                        },
                    },
                    "DEV": {
                        "vrf": "DEV",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.254.1": {
                                "peerState": "Established",
                                "peerAsn": "65120",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 4, "nlrisAccepted": 4},
                            }
                        },
                    },
                }
            }
        ],
        "inputs": {
            "address_families": [
                {"afi": "evpn", "num_peers": 3, "check_peer_state": True},
                {"afi": "ipv4", "safi": "unicast", "vrf": "default", "num_peers": 3, "check_peer_state": True},
                {"afi": "ipv4", "safi": "unicast", "vrf": "DEV", "num_peers": 2, "check_peer_state": True},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "AFI: evpn - Peer count mismatch - Expected: 3 Actual: 2",
                "AFI: ipv4 SAFI: unicast VRF: DEV - Peer count mismatch - Expected: 2 Actual: 1",
            ],
        },
    },
    (VerifyBGPPeerCount, "failure-wrong-count"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.0.1": {
                                "peerState": "Idle",
                                "peerAsn": "65100",
                                "ipv4Unicast": {"afiSafiState": "advertised", "nlrisReceived": 0, "nlrisAccepted": 0},
                                "l2VpnEvpn": {"afiSafiState": "negotiated", "nlrisReceived": 42, "nlrisAccepted": 42},
                            }
                        },
                    },
                    "DEV": {
                        "vrf": "DEV",
                        "routerId": "10.1.0.3",
                        "asn": "65120",
                        "peers": {
                            "10.1.254.1": {
                                "peerState": "Idle",
                                "peerAsn": "65120",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 4, "nlrisAccepted": 4},
                            }
                        },
                    },
                }
            }
        ],
        "inputs": {
            "address_families": [
                {"afi": "evpn", "num_peers": 2},
                {"afi": "ipv4", "safi": "unicast", "vrf": "default", "num_peers": 2},
                {"afi": "ipv4", "safi": "unicast", "vrf": "DEV", "num_peers": 2},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "AFI: evpn - Peer count mismatch - Expected: 2 Actual: 1",
                "AFI: ipv4 SAFI: unicast VRF: default - Peer count mismatch - Expected: 2 Actual: 1",
                "AFI: ipv4 SAFI: unicast VRF: DEV - Peer count mismatch - Expected: 2 Actual: 1",
            ],
        },
    },
    (VerifyBGPPeersHealth, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            },
                            {
                                "peerAddress": "10.100.0.13",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"l2VpnEvpn": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            },
                        ]
                    },
                    "DEV": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {"address_families": [{"afi": "evpn"}, {"afi": "ipv4", "safi": "unicast", "vrf": "default"}, {"afi": "ipv4", "safi": "unicast", "vrf": "DEV"}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeersHealth, "success-min-established-time"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Established",
                                "establishedTime": 169883,
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            },
                            {
                                "peerAddress": "10.100.0.13",
                                "state": "Established",
                                "establishedTime": 169883,
                                "neighborCapabilities": {"multiprotocolCaps": {"l2VpnEvpn": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            },
                        ]
                    },
                    "DEV": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Established",
                                "establishedTime": 169883,
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "minimum_established_time": 10000,
            "address_families": [{"afi": "evpn"}, {"afi": "ipv4", "safi": "unicast", "vrf": "default"}, {"afi": "ipv4", "safi": "unicast", "vrf": "DEV"}],
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeersHealth, "failure-vrf-not-configured"): {
        "eos_data": [{"vrfs": {}}],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "vrf": "default"},
                {"afi": "ipv4", "safi": "sr-te", "vrf": "MGMT"},
                {"afi": "path-selection"},
                {"afi": "link-state"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "AFI: ipv4 SAFI: unicast VRF: default - VRF not configured",
                "AFI: ipv4 SAFI: sr-te VRF: MGMT - VRF not configured",
                "AFI: path-selection - VRF not configured",
                "AFI: link-state - VRF not configured",
            ],
        },
    },
    (VerifyBGPPeersHealth, "failure-peer-not-found"): {
        "eos_data": [{"vrfs": {"default": {"peerList": []}, "MGMT": {"peerList": []}}}],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "vrf": "default"},
                {"afi": "ipv4", "safi": "sr-te", "vrf": "MGMT"},
                {"afi": "path-selection"},
                {"afi": "link-state"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "AFI: ipv4 SAFI: unicast VRF: default - No peers found",
                "AFI: ipv4 SAFI: sr-te VRF: MGMT - No peers found",
                "AFI: path-selection - No peers found",
                "AFI: link-state - No peers found",
            ],
        },
    },
    (VerifyBGPPeersHealth, "failure-session-not-established"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Idle",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                            },
                            {
                                "peerAddress": "10.100.0.13",
                                "state": "Idle",
                                "neighborCapabilities": {"multiprotocolCaps": {"dps": {"advertised": True, "received": True, "enabled": True}}},
                            },
                            {
                                "peerAddress": "10.100.0.14",
                                "state": "Active",
                                "neighborCapabilities": {"multiprotocolCaps": {"linkState": {"advertised": True, "received": True, "enabled": True}}},
                            },
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Active",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4SrTe": {"advertised": True, "received": True, "enabled": True}}},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "vrf": "default"},
                {"afi": "ipv4", "safi": "sr-te", "vrf": "MGMT"},
                {"afi": "path-selection"},
                {"afi": "link-state"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "AFI: ipv4 SAFI: unicast VRF: default Peer: 10.100.0.12 - Incorrect session state - Expected: Established Actual: Idle",
                "AFI: ipv4 SAFI: sr-te VRF: MGMT Peer: 10.100.0.12 - Incorrect session state - Expected: Established Actual: Active",
                "AFI: path-selection Peer: 10.100.0.13 - Incorrect session state - Expected: Established Actual: Idle",
                "AFI: link-state Peer: 10.100.0.14 - Incorrect session state - Expected: Established Actual: Active",
            ],
        },
    },
    (VerifyBGPPeersHealth, "failure-afi-not-negotiated"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": False, "received": False, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            },
                            {
                                "peerAddress": "10.100.0.13",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"dps": {"advertised": True, "received": False, "enabled": False}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            },
                            {
                                "peerAddress": "10.100.0.14",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"linkState": {"advertised": False, "received": False, "enabled": False}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            },
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4SrTe": {"advertised": False, "received": False, "enabled": False}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "vrf": "default"},
                {"afi": "ipv4", "safi": "sr-te", "vrf": "MGMT"},
                {"afi": "path-selection"},
                {"afi": "link-state"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "AFI: ipv4 SAFI: unicast VRF: default Peer: 10.100.0.12 - AFI/SAFI state is not negotiated - Advertised: False, Received: False, Enabled: True",
                "AFI: ipv4 SAFI: sr-te VRF: MGMT Peer: 10.100.0.12 - AFI/SAFI state is not negotiated - Advertised: False, Received: False, Enabled: False",
                "AFI: path-selection Peer: 10.100.0.13 - AFI/SAFI state is not negotiated - Advertised: True, Received: False, Enabled: False",
                "AFI: link-state Peer: 10.100.0.14 - AFI/SAFI state is not negotiated - Advertised: False, Received: False, Enabled: False",
            ],
        },
    },
    (VerifyBGPPeersHealth, "failure-tcp-queues"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 4, "inputQueueLength": 2},
                            },
                            {
                                "peerAddress": "10.100.0.13",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"dps": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 1, "inputQueueLength": 1},
                            },
                            {
                                "peerAddress": "10.100.0.14",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"linkState": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 2, "inputQueueLength": 3},
                            },
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4SrTe": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 1, "inputQueueLength": 5},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "vrf": "default"},
                {"afi": "ipv4", "safi": "sr-te", "vrf": "MGMT"},
                {"afi": "path-selection"},
                {"afi": "link-state"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "AFI: ipv4 SAFI: unicast VRF: default Peer: 10.100.0.12 - Session has non-empty message queues - InQ: 2 OutQ: 4",
                "AFI: ipv4 SAFI: sr-te VRF: MGMT Peer: 10.100.0.12 - Session has non-empty message queues - InQ: 5 OutQ: 1",
                "AFI: path-selection Peer: 10.100.0.13 - Session has non-empty message queues - InQ: 1 OutQ: 1",
                "AFI: link-state Peer: 10.100.0.14 - Session has non-empty message queues - InQ: 3 OutQ: 2",
            ],
        },
    },
    (VerifyBGPPeersHealth, "failure-min-established-time"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Established",
                                "establishedTime": 9883,
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            },
                            {
                                "peerAddress": "10.100.0.13",
                                "state": "Established",
                                "establishedTime": 9883,
                                "neighborCapabilities": {"multiprotocolCaps": {"l2VpnEvpn": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            },
                        ]
                    },
                    "DEV": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Established",
                                "establishedTime": 9883,
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "minimum_established_time": 10000,
            "address_families": [{"afi": "evpn"}, {"afi": "ipv4", "safi": "unicast", "vrf": "default"}, {"afi": "ipv4", "safi": "unicast", "vrf": "DEV"}],
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "AFI: evpn Peer: 10.100.0.13 - BGP session not established for the minimum required duration - Expected: 10000s Actual: 9883s",
                "AFI: ipv4 SAFI: unicast VRF: default Peer: 10.100.0.12 - BGP session not established for the minimum required duration - "
                "Expected: 10000s Actual: 9883s",
                "AFI: ipv4 SAFI: unicast VRF: DEV Peer: 10.100.0.12 - BGP session not established for the minimum required duration - "
                "Expected: 10000s Actual: 9883s",
            ],
        },
    },
    (VerifyBGPSpecificPeers, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            },
                            {
                                "peerAddress": "10.100.0.13",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"l2VpnEvpn": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            },
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.14",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "peers": ["10.100.0.12"]},
                {"afi": "evpn", "peers": ["10.100.0.13"]},
                {"afi": "ipv4", "safi": "unicast", "vrf": "MGMT", "peers": ["10.100.0.14"]},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPSpecificPeers, "success-min-established-time"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Established",
                                "establishedTime": 169883,
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            },
                            {
                                "peerAddress": "10.100.0.13",
                                "state": "Established",
                                "establishedTime": 169883,
                                "neighborCapabilities": {"multiprotocolCaps": {"l2VpnEvpn": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            },
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.14",
                                "state": "Established",
                                "establishedTime": 169883,
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "minimum_established_time": 10000,
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "peers": ["10.100.0.12"]},
                {"afi": "evpn", "peers": ["10.100.0.13"]},
                {"afi": "ipv4", "safi": "unicast", "vrf": "MGMT", "peers": ["10.100.0.14"]},
            ],
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPSpecificPeers, "failure-peer-not-configured"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.20",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"l2VpnEvpn": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.10",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "peers": ["10.100.0.12"]},
                {"afi": "evpn", "peers": ["10.100.0.13"]},
                {"afi": "ipv4", "safi": "unicast", "vrf": "MGMT", "peers": ["10.100.0.14"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "AFI: ipv4 SAFI: unicast VRF: default Peer: 10.100.0.12 - Not configured",
                "AFI: evpn Peer: 10.100.0.13 - Not configured",
                "AFI: ipv4 SAFI: unicast VRF: MGMT Peer: 10.100.0.14 - Not configured",
            ],
        },
    },
    (VerifyBGPSpecificPeers, "failure-vrf-not-configured"): {
        "eos_data": [{"vrfs": {}}],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "peers": ["10.100.0.12"]},
                {"afi": "evpn", "peers": ["10.100.0.13"]},
                {"afi": "ipv4", "safi": "unicast", "vrf": "MGMT", "peers": ["10.100.0.14"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "AFI: ipv4 SAFI: unicast VRF: default - VRF not configured",
                "AFI: evpn - VRF not configured",
                "AFI: ipv4 SAFI: unicast VRF: MGMT - VRF not configured",
            ],
        },
    },
    (VerifyBGPSpecificPeers, "failure-session-not-established"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Idle",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.14",
                                "state": "Idle",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "peers": ["10.100.0.12"]},
                {"afi": "ipv4", "safi": "unicast", "vrf": "MGMT", "peers": ["10.100.0.14"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "AFI: ipv4 SAFI: unicast VRF: default Peer: 10.100.0.12 - Incorrect session state - Expected: Established Actual: Idle",
                "AFI: ipv4 SAFI: unicast VRF: MGMT Peer: 10.100.0.14 - Incorrect session state - Expected: Established Actual: Idle",
            ],
        },
    },
    (VerifyBGPSpecificPeers, "failure-afi-safi-not-negotiated"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": False, "received": False, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.14",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": False, "received": False, "enabled": False}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "peers": ["10.100.0.12"]},
                {"afi": "ipv4", "safi": "unicast", "vrf": "MGMT", "peers": ["10.100.0.14"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "AFI: ipv4 SAFI: unicast VRF: default Peer: 10.100.0.12 - AFI/SAFI state is not negotiated - Advertised: False, Received: False, Enabled: True",
                "AFI: ipv4 SAFI: unicast VRF: MGMT Peer: 10.100.0.14 - AFI/SAFI state is not negotiated - Advertised: False, Received: False, Enabled: False",
            ],
        },
    },
    (VerifyBGPSpecificPeers, "failure-afi-safi-not-correct"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"l2VpnEvpn": {"advertised": False, "received": False, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.14",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"l2VpnEvpn": {"advertised": False, "received": False, "enabled": False}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "peers": ["10.100.0.12"]},
                {"afi": "ipv4", "safi": "unicast", "vrf": "MGMT", "peers": ["10.100.0.14"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "AFI: ipv4 SAFI: unicast VRF: default Peer: 10.100.0.12 - AFI/SAFI state is not negotiated",
                "AFI: ipv4 SAFI: unicast VRF: MGMT Peer: 10.100.0.14 - AFI/SAFI state is not negotiated",
            ],
        },
    },
    (VerifyBGPSpecificPeers, "failure-tcp-queues"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 3, "inputQueueLength": 3},
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.14",
                                "state": "Established",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 2, "inputQueueLength": 2},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "peers": ["10.100.0.12"]},
                {"afi": "ipv4", "safi": "unicast", "vrf": "MGMT", "peers": ["10.100.0.14"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "AFI: ipv4 SAFI: unicast VRF: default Peer: 10.100.0.12 - Session has non-empty message queues - InQ: 3 OutQ: 3",
                "AFI: ipv4 SAFI: unicast VRF: MGMT Peer: 10.100.0.14 - Session has non-empty message queues - InQ: 2 OutQ: 2",
            ],
        },
    },
    (VerifyBGPSpecificPeers, "failure-min-established-time"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.12",
                                "state": "Established",
                                "establishedTime": 9883,
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            },
                            {
                                "peerAddress": "10.100.0.13",
                                "state": "Established",
                                "establishedTime": 9883,
                                "neighborCapabilities": {"multiprotocolCaps": {"l2VpnEvpn": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            },
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.14",
                                "state": "Established",
                                "establishedTime": 9883,
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                                "peerTcpInfo": {"state": "ESTABLISHED", "outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "minimum_established_time": 10000,
            "address_families": [
                {"afi": "ipv4", "safi": "unicast", "peers": ["10.100.0.12"]},
                {"afi": "evpn", "peers": ["10.100.0.13"]},
                {"afi": "ipv4", "safi": "unicast", "vrf": "MGMT", "peers": ["10.100.0.14"]},
            ],
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "AFI: ipv4 SAFI: unicast VRF: default Peer: 10.100.0.12 - BGP session not established for the minimum required duration - "
                "Expected: 10000s Actual: 9883s",
                "AFI: evpn Peer: 10.100.0.13 - BGP session not established for the minimum required duration - Expected: 10000s Actual: 9883s",
                "AFI: ipv4 SAFI: unicast VRF: MGMT Peer: 10.100.0.14 - BGP session not established for the minimum required duration - "
                "Expected: 10000s Actual: 9883s",
            ],
        },
    },
    (VerifyBGPExchangedRoutes, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                            "192.0.254.5/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                        }
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                            "192.0.254.5/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                        }
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                            "192.0.255.4/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                        }
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                            "192.0.255.4/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                        }
                    }
                }
            },
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.1",
                    "vrf": "default",
                    "advertised_routes": ["192.0.254.5/32", "192.0.254.3/32"],
                    "received_routes": ["192.0.254.3/32", "192.0.255.4/32"],
                },
                {
                    "peer_address": "172.30.11.5",
                    "vrf": "default",
                    "advertised_routes": ["192.0.254.3/32", "192.0.254.5/32"],
                    "received_routes": ["192.0.254.3/32", "192.0.255.4/32"],
                },
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPExchangedRoutes, "success-check-active-false"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                            "192.0.254.5/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                        }
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                            "192.0.255.4/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                        }
                    }
                }
            },
        ],
        "inputs": {
            "check_active": False,
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.1",
                    "vrf": "default",
                    "advertised_routes": ["192.0.254.5/32", "192.0.254.3/32"],
                    "received_routes": ["192.0.254.3/32", "192.0.255.4/32"],
                }
            ],
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPExchangedRoutes, "success-advertised-route-validation-only"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                            "192.0.254.5/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                        }
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                            "192.0.254.5/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                        }
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": False}}]},
                            "192.0.255.4/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": False}}]},
                        }
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": False, "active": True}}]},
                            "192.0.255.4/32": {"bgpRoutePaths": [{"routeType": {"valid": False, "active": True}}]},
                        }
                    }
                }
            },
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "172.30.11.1", "vrf": "default", "advertised_routes": ["192.0.254.5/32", "192.0.254.3/32"]},
                {"peer_address": "172.30.11.5", "vrf": "default", "advertised_routes": ["192.0.254.3/32", "192.0.254.5/32"]},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPExchangedRoutes, "failure-no-routes"): {
        "eos_data": [
            {"vrfs": {"default": {"vrf": "default", "routerId": "192.0.255.1", "asn": "65001", "bgpRouteEntries": {}}}},
            {"vrfs": {"default": {"vrf": "default", "routerId": "192.0.255.1", "asn": "65001", "bgpRouteEntries": {}}}},
            {"vrfs": {"default": {"vrf": "default", "routerId": "192.0.255.1", "asn": "65001", "bgpRouteEntries": {}}}},
            {"vrfs": {"default": {"vrf": "default", "routerId": "192.0.255.1", "asn": "65001", "bgpRouteEntries": {}}}},
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "172.30.11.11", "vrf": "default", "advertised_routes": ["192.0.254.3/32"], "received_routes": ["192.0.255.3/32"]},
                {"peer_address": "172.30.11.12", "vrf": "default", "advertised_routes": ["192.0.254.31/32"], "received_routes": ["192.0.255.31/32"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 172.30.11.11 VRF: default Advertised route: 192.0.254.3/32 - Not found",
                "Peer: 172.30.11.11 VRF: default Received route: 192.0.255.3/32 - Not found",
                "Peer: 172.30.11.12 VRF: default Advertised route: 192.0.254.31/32 - Not found",
                "Peer: 172.30.11.12 VRF: default Received route: 192.0.255.31/32 - Not found",
            ],
        },
    },
    (VerifyBGPExchangedRoutes, "failure-invalid-or-inactive-routes"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": False, "active": True}}]},
                            "192.0.254.5/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": False}}]},
                        }
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": False, "active": True}}]},
                            "192.0.254.5/32": {"bgpRoutePaths": [{"routeType": {"valid": False, "active": True}}]},
                        }
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": False, "active": False}}]},
                            "192.0.255.4/32": {"bgpRoutePaths": [{"routeType": {"valid": False, "active": False}}]},
                        }
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": False}}]},
                            "192.0.255.4/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": False}}]},
                        }
                    }
                }
            },
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.1",
                    "vrf": "default",
                    "advertised_routes": ["192.0.254.3/32", "192.0.254.51/32"],
                    "received_routes": ["192.0.254.31/32", "192.0.255.4/32"],
                },
                {
                    "peer_address": "172.30.11.5",
                    "vrf": "default",
                    "advertised_routes": ["192.0.254.31/32", "192.0.254.5/32"],
                    "received_routes": ["192.0.254.3/32", "192.0.255.41/32"],
                },
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 172.30.11.1 VRF: default Advertised route: 192.0.254.3/32 - Valid: False Active: True",
                "Peer: 172.30.11.1 VRF: default Advertised route: 192.0.254.51/32 - Not found",
                "Peer: 172.30.11.1 VRF: default Received route: 192.0.254.31/32 - Not found",
                "Peer: 172.30.11.1 VRF: default Received route: 192.0.255.4/32 - Valid: False Active: False",
                "Peer: 172.30.11.5 VRF: default Advertised route: 192.0.254.31/32 - Not found",
                "Peer: 172.30.11.5 VRF: default Advertised route: 192.0.254.5/32 - Valid: False Active: True",
                "Peer: 172.30.11.5 VRF: default Received route: 192.0.254.3/32 - Valid: True Active: False",
                "Peer: 172.30.11.5 VRF: default Received route: 192.0.255.41/32 - Not found",
            ],
        },
    },
    (VerifyBGPExchangedRoutes, "failure-invalid-or-inactive-routes-as-per-given-input"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": False, "active": True}}]},
                            "192.0.254.5/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": False}}]},
                        }
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                            "192.0.254.5/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                        }
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                            "192.0.255.4/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                        }
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": False}}]},
                            "192.0.255.4/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": False}}]},
                        }
                    }
                }
            },
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "172.30.11.1", "vrf": "default", "advertised_routes": ["192.0.254.3/32", "192.0.254.51/32"]},
                {"peer_address": "172.30.11.5", "vrf": "default", "received_routes": ["192.0.254.3/32", "192.0.255.41/32"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 172.30.11.1 VRF: default Advertised route: 192.0.254.3/32 - Valid: False Active: True",
                "Peer: 172.30.11.1 VRF: default Advertised route: 192.0.254.51/32 - Not found",
                "Peer: 172.30.11.5 VRF: default Received route: 192.0.254.3/32 - Valid: True Active: False",
                "Peer: 172.30.11.5 VRF: default Received route: 192.0.255.41/32 - Not found",
            ],
        },
    },
    (VerifyBGPExchangedRoutes, "failure-check-active-false"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": False, "active": False}}]},
                            "192.0.254.5/32": {"bgpRoutePaths": [{"routeType": {"valid": False, "active": True}}]},
                        }
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "192.0.254.3/32": {"bgpRoutePaths": [{"routeType": {"valid": True, "active": True}}]},
                            "192.0.255.4/32": {"bgpRoutePaths": [{"routeType": {"valid": False, "active": True}}]},
                        }
                    }
                }
            },
        ],
        "inputs": {
            "check_active": False,
            "bgp_peers": [
                {
                    "peer_address": "172.30.11.1",
                    "vrf": "default",
                    "advertised_routes": ["192.0.254.5/32", "192.0.254.3/32"],
                    "received_routes": ["192.0.254.3/32", "192.0.255.4/32"],
                }
            ],
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 172.30.11.1 VRF: default Advertised route: 192.0.254.5/32 - Valid: False",
                "Peer: 172.30.11.1 VRF: default Advertised route: 192.0.254.3/32 - Valid: False",
                "Peer: 172.30.11.1 VRF: default Received route: 192.0.255.4/32 - Valid: False",
            ],
        },
    },
    (VerifyBGPPeerMPCaps, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": True, "received": True, "enabled": True},
                                        "ipv4MplsLabels": {"advertised": True, "received": True, "enabled": True},
                                    }
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.10",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": True, "received": True, "enabled": True},
                                        "ipv4MplsVpn": {"advertised": True, "received": True, "enabled": True},
                                    }
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "172.30.11.1", "vrf": "default", "capabilities": ["Ipv4Unicast", "ipv4 Mpls labels"]},
                {"peer_address": "172.30.11.10", "vrf": "MGMT", "capabilities": ["ipv4_Unicast", "ipv4 MplsVpn"]},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerMPCaps, "success-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "fd00:dc:1::1",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": True, "received": True, "enabled": True},
                                        "ipv4MplsLabels": {"advertised": True, "received": True, "enabled": True},
                                    }
                                },
                            },
                            {
                                "peerAddress": "fe80::250:56ff:fe01:112%Vl4094",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": True, "received": True, "enabled": True},
                                        "ipv4MplsLabels": {"advertised": True, "received": True, "enabled": True},
                                    }
                                },
                            },
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": True, "received": True, "enabled": True},
                                        "ipv4MplsVpn": {"advertised": True, "received": True, "enabled": True},
                                    }
                                },
                                "ifName": "Ethernet1",
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default", "capabilities": ["Ipv4Unicast", "ipv4 Mpls labels"]},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default", "capabilities": ["Ipv4Unicast", "ipv4 Mpls labels"]},
                {"interface": "Ethernet1", "vrf": "MGMT", "capabilities": ["ipv4_Unicast", "ipv4 MplsVpn"]},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerMPCaps, "failure-no-peer"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.10",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "172.30.11.10", "vrf": "default", "capabilities": ["ipv4Unicast", "l2-vpn-EVPN"]},
                {"peer_address": "172.30.11.1", "vrf": "MGMT", "capabilities": ["ipv4Unicast", "l2vpnevpn"]},
            ]
        },
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 172.30.11.10 VRF: default - Not found", "Peer: 172.30.11.1 VRF: MGMT - Not found"]},
    },
    (VerifyBGPPeerMPCaps, "failure-capabilities-not-found"): {
        "eos_data": [{"vrfs": {"default": {"peerList": [{"peerAddress": "172.30.11.1", "neighborCapabilities": {}}]}}}],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default", "capabilities": ["ipv4Unicast", "l2-vpn-EVPN"]}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 172.30.11.1 VRF: default - Multiprotocol capabilities not found"]},
    },
    (VerifyBGPPeerMPCaps, "failure-missing-capabilities"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                            }
                        ]
                    }
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default", "capabilities": ["ipv4 Unicast", "L2VpnEVPN"]}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 172.30.11.1 VRF: default - l2VpnEvpn not found"]},
    },
    (VerifyBGPPeerMPCaps, "failure-incorrect-capabilities"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": False, "received": False, "enabled": False},
                                        "ipv4MplsVpn": {"advertised": False, "received": True, "enabled": False},
                                    }
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.10",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "l2VpnEvpn": {"advertised": True, "received": False, "enabled": False},
                                        "ipv4MplsVpn": {"advertised": False, "received": False, "enabled": True},
                                    }
                                },
                            },
                            {
                                "peerAddress": "172.30.11.11",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": False, "received": False, "enabled": False},
                                        "ipv4MplsVpn": {"advertised": False, "received": False, "enabled": False},
                                    }
                                },
                            },
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "172.30.11.1", "vrf": "default", "capabilities": ["ipv4 unicast", "ipv4 mpls vpn", "L2 vpn EVPN"]},
                {"peer_address": "172.30.11.10", "vrf": "MGMT", "capabilities": ["ipv4_unicast", "ipv4 mplsvpn", "L2vpnEVPN"]},
                {"peer_address": "172.30.11.11", "vrf": "MGMT", "capabilities": ["Ipv4 Unicast", "ipv4 MPLSVPN", "L2 vpnEVPN"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 172.30.11.1 VRF: default - ipv4Unicast not negotiated - Advertised: False, Received: False, Enabled: False",
                "Peer: 172.30.11.1 VRF: default - ipv4MplsVpn not negotiated - Advertised: False, Received: True, Enabled: False",
                "Peer: 172.30.11.1 VRF: default - l2VpnEvpn not found",
                "Peer: 172.30.11.10 VRF: MGMT - ipv4Unicast not found",
                "Peer: 172.30.11.10 VRF: MGMT - ipv4MplsVpn not negotiated - Advertised: False, Received: False, Enabled: True",
                "Peer: 172.30.11.10 VRF: MGMT - l2VpnEvpn not negotiated - Advertised: True, Received: False, Enabled: False",
                "Peer: 172.30.11.11 VRF: MGMT - ipv4Unicast not negotiated - Advertised: False, Received: False, Enabled: False",
                "Peer: 172.30.11.11 VRF: MGMT - ipv4MplsVpn not negotiated - Advertised: False, Received: False, Enabled: False",
                "Peer: 172.30.11.11 VRF: MGMT - l2VpnEvpn not found",
            ],
        },
    },
    (VerifyBGPPeerMPCaps, "success-strict"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": True, "received": True, "enabled": True},
                                        "ipv4MplsLabels": {"advertised": True, "received": True, "enabled": True},
                                    }
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.10",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": True, "received": True, "enabled": True},
                                        "ipv4MplsVpn": {"advertised": True, "received": True, "enabled": True},
                                    }
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "172.30.11.1", "vrf": "default", "strict": True, "capabilities": ["Ipv4 Unicast", "ipv4MplsLabels"]},
                {"peer_address": "172.30.11.10", "vrf": "MGMT", "strict": True, "capabilities": ["ipv4-Unicast", "ipv4MplsVpn"]},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerMPCaps, "failure-srict"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": True, "received": True, "enabled": True},
                                        "ipv4MplsLabels": {"advertised": True, "received": True, "enabled": True},
                                    }
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.10",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": True, "received": True, "enabled": True},
                                        "ipv4MplsVpn": {"advertised": False, "received": True, "enabled": True},
                                    }
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "172.30.11.1", "vrf": "default", "strict": True, "capabilities": ["Ipv4 Unicast"]},
                {"peer_address": "172.30.11.10", "vrf": "MGMT", "strict": True, "capabilities": ["ipv4MplsVpn", "L2vpnEVPN"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 172.30.11.1 VRF: default - Mismatch - Expected: ipv4Unicast Actual: ipv4Unicast, ipv4MplsLabels",
                "Peer: 172.30.11.10 VRF: MGMT - Mismatch - Expected: ipv4MplsVpn, l2VpnEvpn Actual: ipv4Unicast, ipv4MplsVpn",
            ],
        },
    },
    (VerifyBGPPeerMPCaps, "failure-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "fd00:dc:1::1",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": True, "received": True, "enabled": True},
                                        "ipv4MplsLabels": {"advertised": False, "received": True, "enabled": True},
                                    }
                                },
                            },
                            {
                                "peerAddress": "fe80::250:56ff:fe01:112%Vl4094",
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": False, "received": True, "enabled": True},
                                        "ipv4MplsLabels": {"advertised": True, "received": True, "enabled": True},
                                    }
                                },
                            },
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "neighborCapabilities": {
                                    "multiprotocolCaps": {
                                        "ipv4Unicast": {"advertised": True, "received": True, "enabled": True},
                                        "ipv4MplsVpn": {"advertised": False, "received": True, "enabled": True},
                                    }
                                },
                                "ifName": "Ethernet1",
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default", "capabilities": ["Ipv4Unicast", "ipv4 Mpls labels"]},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default", "capabilities": ["Ipv4Unicast", "ipv4 Mpls labels"]},
                {"interface": "Ethernet1", "vrf": "MGMT", "capabilities": ["ipv4_Unicast", "ipv4 MplsVpn"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: fd00:dc:1::1 VRF: default - ipv4MplsLabels not negotiated - Advertised: False, Received: True, Enabled: True",
                "Peer: fe80::250:56ff:fe01:112%Vl4094 VRF: default - ipv4Unicast not negotiated - Advertised: False, Received: True, Enabled: True",
                "Interface: Ethernet1 VRF: MGMT - ipv4MplsVpn not negotiated - Advertised: False, Received: True, Enabled: True",
            ],
        },
    },
    (VerifyBGPPeerASNCap, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "172.30.11.1", "neighborCapabilities": {"fourOctetAsnCap": {"advertised": True, "received": True, "enabled": True}}}
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {"peerAddress": "172.30.11.10", "neighborCapabilities": {"fourOctetAsnCap": {"advertised": True, "received": True, "enabled": True}}}
                        ]
                    },
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default"}, {"peer_address": "172.30.11.10", "vrf": "MGMT"}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerASNCap, "success-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "neighborCapabilities": {"fourOctetAsnCap": {"advertised": True, "received": True, "enabled": True}}},
                            {
                                "peerAddress": "fe80::250:56ff:fe01:112%Vl4094",
                                "neighborCapabilities": {"fourOctetAsnCap": {"advertised": True, "received": True, "enabled": True}},
                            },
                        ]
                    },
                    "MGMT": {
                        "peerList": [{"neighborCapabilities": {"fourOctetAsnCap": {"advertised": True, "received": True, "enabled": True}}, "ifName": "Ethernet1"}]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default"},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default"},
                {"interface": "Ethernet1", "vrf": "MGMT"},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerASNCap, "failure-no-peer"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                            }
                        ]
                    }
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.10", "vrf": "default"}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 172.30.11.10 VRF: default - Not found"]},
    },
    (VerifyBGPPeerASNCap, "failure-missing-capabilities"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.10",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4MplsLabels": {"advertised": True, "received": True, "enabled": True}}},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default"}, {"peer_address": "172.30.11.10", "vrf": "MGMT"}]},
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": ["Peer: 172.30.11.1 VRF: default - 4-octet ASN capability not found", "Peer: 172.30.11.10 VRF: MGMT - 4-octet ASN capability not found"],
        },
    },
    (VerifyBGPPeerASNCap, "failure-incorrect-capabilities"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "172.30.11.1", "neighborCapabilities": {"fourOctetAsnCap": {"advertised": False, "received": False, "enabled": False}}}
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {"peerAddress": "172.30.11.10", "neighborCapabilities": {"fourOctetAsnCap": {"advertised": True, "received": False, "enabled": True}}}
                        ]
                    },
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default"}, {"peer_address": "172.30.11.10", "vrf": "MGMT"}]},
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 172.30.11.1 VRF: default - 4-octet ASN capability not negotiated - Advertised: False, Received: False, Enabled: False",
                "Peer: 172.30.11.10 VRF: MGMT - 4-octet ASN capability not negotiated - Advertised: True, Received: False, Enabled: True",
            ],
        },
    },
    (VerifyBGPPeerASNCap, "failure-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "neighborCapabilities": {"fourOctetAsnCap": {"advertised": True, "received": True, "enabled": True}}},
                            {
                                "peerAddress": "fe80::250:56ff:fe01:112%Vl4094",
                                "neighborCapabilities": {"fourOctetAsnCap": {"advertised": False, "received": True, "enabled": True}},
                            },
                        ]
                    },
                    "MGMT": {
                        "peerList": [{"neighborCapabilities": {"fourOctetAsnCap": {"advertised": False, "received": True, "enabled": True}}, "ifName": "Ethernet1"}]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default"},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default"},
                {"interface": "Ethernet1", "vrf": "MGMT"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: fe80::250:56ff:fe01:112%Vl4094 VRF: default - 4-octet ASN capability not negotiated - Advertised: False, Received: True, Enabled: True",
                "Interface: Ethernet1 VRF: MGMT - 4-octet ASN capability not negotiated - Advertised: False, Received: True, Enabled: True",
            ],
        },
    },
    (VerifyBGPPeerRouteRefreshCap, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "172.30.11.1", "neighborCapabilities": {"routeRefreshCap": {"advertised": True, "received": True, "enabled": True}}}
                        ]
                    },
                    "CS": {
                        "peerList": [
                            {"peerAddress": "172.30.11.11", "neighborCapabilities": {"routeRefreshCap": {"advertised": True, "received": True, "enabled": True}}}
                        ]
                    },
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default"}, {"peer_address": "172.30.11.11", "vrf": "CS"}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerRouteRefreshCap, "success-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "neighborCapabilities": {"routeRefreshCap": {"advertised": True, "received": True, "enabled": True}}},
                            {
                                "peerAddress": "fe80::250:56ff:fe01:112%Vl4094",
                                "neighborCapabilities": {"routeRefreshCap": {"advertised": True, "received": True, "enabled": True}},
                            },
                        ]
                    },
                    "CS": {
                        "peerList": [{"neighborCapabilities": {"routeRefreshCap": {"advertised": True, "received": True, "enabled": True}}, "ifName": "Ethernet1"}]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default"},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default"},
                {"interface": "Ethernet1", "vrf": "CS"},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerRouteRefreshCap, "failure-no-peer"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {"multiprotocolCaps": {"ip4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                            }
                        ]
                    },
                    "CS": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.12",
                                "neighborCapabilities": {"multiprotocolCaps": {"ip4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.12", "vrf": "default"}, {"peer_address": "172.30.11.1", "vrf": "CS"}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 172.30.11.12 VRF: default - Not found", "Peer: 172.30.11.1 VRF: CS - Not found"]},
    },
    (VerifyBGPPeerRouteRefreshCap, "failure-missing-capabilities"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.1",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                            }
                        ]
                    },
                    "CS": {
                        "peerList": [
                            {
                                "peerAddress": "172.30.11.11",
                                "neighborCapabilities": {"multiprotocolCaps": {"ipv4Unicast": {"advertised": True, "received": True, "enabled": True}}},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default"}, {"peer_address": "172.30.11.11", "vrf": "CS"}]},
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": ["Peer: 172.30.11.1 VRF: default - Route refresh capability not found", "Peer: 172.30.11.11 VRF: CS - Route refresh capability not found"],
        },
    },
    (VerifyBGPPeerRouteRefreshCap, "failure-incorrect-capabilities"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "172.30.11.1", "neighborCapabilities": {"routeRefreshCap": {"advertised": False, "received": False, "enabled": False}}}
                        ]
                    },
                    "CS": {
                        "peerList": [
                            {"peerAddress": "172.30.11.11", "neighborCapabilities": {"routeRefreshCap": {"advertised": True, "received": True, "enabled": True}}}
                        ]
                    },
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default"}, {"peer_address": "172.30.11.11", "vrf": "CS"}]},
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": ["Peer: 172.30.11.1 VRF: default - Route refresh capability not negotiated - Advertised: False, Received: False, Enabled: False"],
        },
    },
    (VerifyBGPPeerRouteRefreshCap, "failure-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "neighborCapabilities": {"routeRefreshCap": {"advertised": True, "received": False, "enabled": True}}},
                            {
                                "peerAddress": "fe80::250:56ff:fe01:112%Vl4094",
                                "neighborCapabilities": {"routeRefreshCap": {"advertised": True, "received": True, "enabled": False}},
                            },
                        ]
                    },
                    "CS": {
                        "peerList": [{"neighborCapabilities": {"routeRefreshCap": {"advertised": False, "received": True, "enabled": True}}, "ifName": "Ethernet1"}]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default"},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default"},
                {"interface": "Ethernet1", "vrf": "CS"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: fd00:dc:1::1 VRF: default - Route refresh capability not negotiated - Advertised: True, Received: False, Enabled: True",
                "Peer: fe80::250:56ff:fe01:112%Vl4094 VRF: default - Route refresh capability not negotiated - Advertised: True, Received: True, Enabled: False",
                "Interface: Ethernet1 VRF: CS - Route refresh capability not negotiated - Advertised: False, Received: True, Enabled: True",
            ],
        },
    },
    (VerifyBGPPeerMD5Auth, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "172.30.11.1", "state": "Established", "md5AuthEnabled": True}]},
                    "CS": {"peerList": [{"peerAddress": "172.30.11.10", "state": "Established", "md5AuthEnabled": True}]},
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default"}, {"peer_address": "172.30.11.10", "vrf": "CS"}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerMD5Auth, "success-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "state": "Established", "md5AuthEnabled": True},
                            {"peerAddress": "fe80::250:56ff:fe01:112%Vl4094", "state": "Established", "md5AuthEnabled": True},
                        ]
                    },
                    "CS": {"peerList": [{"state": "Established", "md5AuthEnabled": True, "ifName": "Ethernet1"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default"},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default"},
                {"interface": "Ethernet1", "vrf": "CS"},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerMD5Auth, "failure-no-peer"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "172.30.11.1", "state": "Established", "md5AuthEnabled": True}]},
                    "CS": {"peerList": [{"peerAddress": "172.30.11.11", "state": "Established", "md5AuthEnabled": True}]},
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.10", "vrf": "default"}, {"peer_address": "172.30.11.12", "vrf": "CS"}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 172.30.11.10 VRF: default - Not found", "Peer: 172.30.11.12 VRF: CS - Not found"]},
    },
    (VerifyBGPPeerMD5Auth, "failure-not-established-peer"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "172.30.11.1", "state": "Idle", "md5AuthEnabled": True}]},
                    "MGMT": {"peerList": [{"peerAddress": "172.30.11.10", "state": "Idle", "md5AuthEnabled": True}]},
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default"}, {"peer_address": "172.30.11.10", "vrf": "MGMT"}]},
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 172.30.11.1 VRF: default - Incorrect session state - Expected: Established Actual: Idle",
                "Peer: 172.30.11.10 VRF: MGMT - Incorrect session state - Expected: Established Actual: Idle",
            ],
        },
    },
    (VerifyBGPPeerMD5Auth, "failure-not-md5-peer"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "172.30.11.1", "state": "Established"},
                            {"peerAddress": "172.30.11.10", "state": "Established", "md5AuthEnabled": False},
                        ]
                    },
                    "MGMT": {"peerList": [{"peerAddress": "172.30.11.11", "state": "Established", "md5AuthEnabled": False}]},
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default"}, {"peer_address": "172.30.11.11", "vrf": "MGMT"}]},
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 172.30.11.1 VRF: default - Session does not have MD5 authentication enabled",
                "Peer: 172.30.11.11 VRF: MGMT - Session does not have MD5 authentication enabled",
            ],
        },
    },
    (VerifyBGPPeerMD5Auth, "failure-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "state": "Idle", "md5AuthEnabled": True},
                            {"peerAddress": "fe80::250:56ff:fe01:112%Vl4094", "state": "Established"},
                        ]
                    },
                    "CS": {"peerList": [{"state": "Idle", "md5AuthEnabled": True, "ifName": "Ethernet1"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default"},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default"},
                {"interface": "Ethernet1", "vrf": "CS"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: fd00:dc:1::1 VRF: default - Incorrect session state - Expected: Established Actual: Idle",
                "Peer: fe80::250:56ff:fe01:112%Vl4094 VRF: default - Session does not have MD5 authentication enabled",
                "Interface: Ethernet1 VRF: CS - Incorrect session state - Expected: Established Actual: Idle",
            ],
        },
    },
    (VerifyEVPNType2Route, "success"): {
        "eos_data": [
            {
                "vrf": "default",
                "routerId": "10.1.0.3",
                "asn": 65120,
                "evpnRoutes": {"RD: 10.1.0.5:500 mac-ip 10020 aac1.ab4e.bec2 192.168.20.102": {"evpnRoutePaths": [{"routeType": {"active": True, "valid": True}}]}},
            }
        ],
        "inputs": {"vxlan_endpoints": [{"address": "192.168.20.102", "vni": 10020}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyEVPNType2Route, "success-multiple-endpoints"): {
        "eos_data": [
            {
                "vrf": "default",
                "routerId": "10.1.0.3",
                "asn": 65120,
                "evpnRoutes": {"RD: 10.1.0.5:500 mac-ip 10020 aac1.ab4e.bec2 192.168.20.102": {"evpnRoutePaths": [{"routeType": {"active": True, "valid": True}}]}},
            },
            {
                "vrf": "default",
                "routerId": "10.1.0.3",
                "asn": 65120,
                "evpnRoutes": {"RD: 10.1.0.5:500 mac-ip 10010 aac1.ab5d.b41e": {"evpnRoutePaths": [{"routeType": {"active": True, "valid": True}}]}},
            },
        ],
        "inputs": {"vxlan_endpoints": [{"address": "192.168.20.102", "vni": 10020}, {"address": "aac1.ab5d.b41e", "vni": 10010}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyEVPNType2Route, "success-multiple-routes-ip"): {
        "eos_data": [
            {
                "vrf": "default",
                "routerId": "10.1.0.3",
                "asn": 65120,
                "evpnRoutes": {
                    "RD: 10.1.0.5:500 mac-ip 10020 aac1.ab4e.bec2 192.168.20.102": {"evpnRoutePaths": [{"routeType": {"active": True, "valid": True}}]},
                    "RD: 10.1.0.6:500 mac-ip 10020 aac1.ab4e.bec2 192.168.20.102": {"evpnRoutePaths": [{"routeType": {"active": False, "valid": False}}]},
                },
            }
        ],
        "inputs": {"vxlan_endpoints": [{"address": "192.168.20.102", "vni": 10020}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyEVPNType2Route, "success-multiple-routes-mac"): {
        "eos_data": [
            {
                "vrf": "default",
                "routerId": "10.1.0.3",
                "asn": 65120,
                "evpnRoutes": {
                    "RD: 10.1.0.5:500 mac-ip 10020 aac1.ab4e.bec2": {"evpnRoutePaths": [{"routeType": {"active": True, "valid": True}}]},
                    "RD: 10.1.0.6:500 mac-ip 10020 aac1.ab4e.bec2": {"evpnRoutePaths": [{"routeType": {"active": True, "valid": True}}]},
                },
            }
        ],
        "inputs": {"vxlan_endpoints": [{"address": "aac1.ab4e.bec2", "vni": 10020}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyEVPNType2Route, "success-multiple-routes-multiple-paths-ip"): {
        "eos_data": [
            {
                "vrf": "default",
                "routerId": "10.1.0.3",
                "asn": 65120,
                "evpnRoutes": {
                    "RD: 10.1.0.5:500 mac-ip 10020 aac1.ab4e.bec2 192.168.20.102": {
                        "evpnRoutePaths": [
                            {"routeType": {"active": True, "valid": True, "ecmp": True, "ecmpContributor": True, "ecmpHead": True}},
                            {"routeType": {"active": False, "valid": True, "ecmp": True, "ecmpContributor": True, "ecmpHead": False}},
                        ]
                    },
                    "RD: 10.1.0.6:500 mac-ip 10020 aac1.ab4e.bec2 192.168.20.102": {"evpnRoutePaths": [{"routeType": {"active": True, "valid": True}}]},
                },
            }
        ],
        "inputs": {"vxlan_endpoints": [{"address": "192.168.20.102", "vni": 10020}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyEVPNType2Route, "success-multiple-routes-multiple-paths-mac"): {
        "eos_data": [
            {
                "vrf": "default",
                "routerId": "10.1.0.3",
                "asn": 65120,
                "evpnRoutes": {
                    "RD: 10.1.0.5:500 mac-ip 10020 aac1.ab4e.bec2": {
                        "evpnRoutePaths": [
                            {"routeType": {"active": True, "valid": True, "ecmp": True, "ecmpContributor": True, "ecmpHead": True}},
                            {"routeType": {"active": False, "valid": True, "ecmp": True, "ecmpContributor": True, "ecmpHead": False}},
                        ]
                    },
                    "RD: 10.1.0.6:500 mac-ip 10020 aac1.ab4e.bec2": {"evpnRoutePaths": [{"routeType": {"active": True, "valid": True}}]},
                },
            }
        ],
        "inputs": {"vxlan_endpoints": [{"address": "aac1.ab4e.bec2", "vni": 10020}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyEVPNType2Route, "failure-no-routes"): {
        "eos_data": [{"vrf": "default", "routerId": "10.1.0.3", "asn": 65120, "evpnRoutes": {}}],
        "inputs": {"vxlan_endpoints": [{"address": "192.168.20.102", "vni": 10020}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Address: 192.168.20.102 VNI: 10020 - No EVPN Type-2 route"]},
    },
    (VerifyEVPNType2Route, "failure-path-not-active"): {
        "eos_data": [
            {
                "vrf": "default",
                "routerId": "10.1.0.3",
                "asn": 65120,
                "evpnRoutes": {"RD: 10.1.0.5:500 mac-ip 10020 aac1.ab4e.bec2 192.168.20.102": {"evpnRoutePaths": [{"routeType": {"active": False, "valid": True}}]}},
            }
        ],
        "inputs": {"vxlan_endpoints": [{"address": "192.168.20.102", "vni": 10020}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Address: 192.168.20.102 VNI: 10020 - No valid and active path"]},
    },
    (VerifyEVPNType2Route, "failure-multiple-endpoints"): {
        "eos_data": [
            {
                "vrf": "default",
                "routerId": "10.1.0.3",
                "asn": 65120,
                "evpnRoutes": {
                    "RD: 10.1.0.5:500 mac-ip 10020 aac1.ab4e.bec2 192.168.20.102": {"evpnRoutePaths": [{"routeType": {"active": False, "valid": False}}]}
                },
            },
            {
                "vrf": "default",
                "routerId": "10.1.0.3",
                "asn": 65120,
                "evpnRoutes": {"RD: 10.1.0.5:500 mac-ip 10010 aac1.ab5d.b41e": {"evpnRoutePaths": [{"routeType": {"active": False, "valid": False}}]}},
            },
        ],
        "inputs": {"vxlan_endpoints": [{"address": "192.168.20.102", "vni": 10020}, {"address": "aac1.ab5d.b41e", "vni": 10010}]},
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": ["Address: 192.168.20.102 VNI: 10020 - No valid and active path", "Address: aa:c1:ab:5d:b4:1e VNI: 10010 - No valid and active path"],
        },
    },
    (VerifyBGPAdvCommunities, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "172.30.11.1", "advertisedCommunities": {"standard": True, "extended": True, "large": True}}]},
                    "MGMT": {"peerList": [{"peerAddress": "172.30.11.10", "advertisedCommunities": {"standard": True, "extended": True, "large": True}}]},
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1"}, {"peer_address": "172.30.11.10", "vrf": "MGMT"}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPAdvCommunities, "success-specified-communities"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "172.30.11.1", "advertisedCommunities": {"standard": True, "extended": True, "large": False}}]},
                    "MGMT": {"peerList": [{"peerAddress": "172.30.11.10", "advertisedCommunities": {"standard": False, "extended": True, "large": False}}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "172.30.11.1", "advertised_communities": ["standard", "extended"]},
                {"peer_address": "172.30.11.10", "vrf": "MGMT", "advertised_communities": ["extended"]},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPAdvCommunities, "success-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "advertisedCommunities": {"standard": True, "extended": True, "large": True}},
                            {"peerAddress": "fe80::250:56ff:fe01:112%Vl4094", "advertisedCommunities": {"standard": True, "extended": True, "large": True}},
                        ]
                    },
                    "MGMT": {"peerList": [{"advertisedCommunities": {"standard": True, "extended": True, "large": True}, "ifName": "Ethernet1"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default"},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default"},
                {"interface": "Ethernet1", "vrf": "MGMT"},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPAdvCommunities, "failure-no-peer"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "172.30.11.1", "advertisedCommunities": {"standard": True, "extended": True, "large": True}}]},
                    "MGMT": {"peerList": [{"peerAddress": "172.30.11.1", "advertisedCommunities": {"standard": True, "extended": True, "large": True}}]},
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.10", "vrf": "default"}, {"peer_address": "172.30.11.12", "vrf": "MGMT"}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 172.30.11.10 VRF: default - Not found", "Peer: 172.30.11.12 VRF: MGMT - Not found"]},
    },
    (VerifyBGPAdvCommunities, "failure-not-correct-communities"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "172.30.11.1", "advertisedCommunities": {"standard": False, "extended": False, "large": False}}]},
                    "CS": {"peerList": [{"peerAddress": "172.30.11.10", "advertisedCommunities": {"standard": True, "extended": True, "large": False}}]},
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "172.30.11.1", "vrf": "default"}, {"peer_address": "172.30.11.10", "vrf": "CS"}]},
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 172.30.11.1 VRF: default - Standard: False, Extended: False, Large: False",
                "Peer: 172.30.11.10 VRF: CS - Standard: True, Extended: True, Large: False",
            ],
        },
    },
    (VerifyBGPAdvCommunities, "failure-specified-communities"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "172.30.11.1", "advertisedCommunities": {"standard": False, "extended": False, "large": False}}]},
                    "MGMT": {"peerList": [{"peerAddress": "172.30.11.10", "advertisedCommunities": {"standard": False, "extended": True, "large": False}}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "172.30.11.1", "advertised_communities": ["standard", "extended"]},
                {"peer_address": "172.30.11.10", "vrf": "MGMT", "advertised_communities": ["extended"]},
            ]
        },
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 172.30.11.1 VRF: default - Standard: False, Extended: False, Large: False"]},
    },
    (VerifyBGPAdvCommunities, "failure-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "advertisedCommunities": {"standard": False, "extended": True, "large": True}},
                            {"peerAddress": "fe80::250:56ff:fe01:112%Vl4094", "advertisedCommunities": {"standard": True, "extended": False, "large": True}},
                        ]
                    },
                    "MGMT": {"peerList": [{"advertisedCommunities": {"standard": True, "extended": True, "large": False}, "ifName": "Ethernet1"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default"},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default"},
                {"interface": "Ethernet1", "vrf": "MGMT"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: fd00:dc:1::1 VRF: default - Standard: False, Extended: True, Large: True",
                "Peer: fe80::250:56ff:fe01:112%Vl4094 VRF: default - Standard: True, Extended: False, Large: True",
                "Interface: Ethernet1 VRF: MGMT - Standard: True, Extended: True, Large: False",
            ],
        },
    },
    (VerifyBGPTimers, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "172.30.11.1", "holdTime": 180, "keepaliveTime": 60}]},
                    "MGMT": {"peerList": [{"peerAddress": "172.30.11.11", "holdTime": 180, "keepaliveTime": 60}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "172.30.11.1", "vrf": "default", "hold_time": 180, "keep_alive_time": 60},
                {"peer_address": "172.30.11.11", "vrf": "MGMT", "hold_time": 180, "keep_alive_time": 60},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPTimers, "success-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "holdTime": 180, "keepaliveTime": 60},
                            {"peerAddress": "fe80::250:56ff:fe01:112%Vl4094", "holdTime": 180, "keepaliveTime": 60},
                        ]
                    },
                    "MGMT": {"peerList": [{"holdTime": 180, "keepaliveTime": 60, "ifName": "Ethernet1"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default", "hold_time": 180, "keep_alive_time": 60},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default", "hold_time": 180, "keep_alive_time": 60},
                {"interface": "Ethernet1", "vrf": "MGMT", "hold_time": 180, "keep_alive_time": 60},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPTimers, "failure-no-peer"): {
        "eos_data": [{"vrfs": {"default": {"peerList": []}, "MGMT": {"peerList": []}}}],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "172.30.11.1", "vrf": "MGMT", "hold_time": 180, "keep_alive_time": 60},
                {"peer_address": "172.30.11.11", "vrf": "default", "hold_time": 180, "keep_alive_time": 60},
            ]
        },
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 172.30.11.1 VRF: MGMT - Not found", "Peer: 172.30.11.11 VRF: default - Not found"]},
    },
    (VerifyBGPTimers, "failure-not-correct-timers"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "172.30.11.1", "holdTime": 160, "keepaliveTime": 60}]},
                    "MGMT": {"peerList": [{"peerAddress": "172.30.11.11", "holdTime": 120, "keepaliveTime": 40}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "172.30.11.1", "vrf": "default", "hold_time": 180, "keep_alive_time": 60},
                {"peer_address": "172.30.11.11", "vrf": "MGMT", "hold_time": 180, "keep_alive_time": 60},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 172.30.11.1 VRF: default - Hold time mismatch - Expected: 180 Actual: 160",
                "Peer: 172.30.11.11 VRF: MGMT - Hold time mismatch - Expected: 180 Actual: 120",
                "Peer: 172.30.11.11 VRF: MGMT - Keepalive time mismatch - Expected: 60 Actual: 40",
            ],
        },
    },
    (VerifyBGPTimers, "failure-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "holdTime": 100, "keepaliveTime": 60},
                            {"peerAddress": "fe80::250:56ff:fe01:112%Vl4094", "holdTime": 180, "keepaliveTime": 50},
                        ]
                    },
                    "MGMT": {"peerList": [{"holdTime": 150, "keepaliveTime": 50, "ifName": "Ethernet1"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default", "hold_time": 180, "keep_alive_time": 60},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default", "hold_time": 180, "keep_alive_time": 60},
                {"interface": "Ethernet1", "vrf": "MGMT", "hold_time": 180, "keep_alive_time": 60},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: fd00:dc:1::1 VRF: default - Hold time mismatch - Expected: 180 Actual: 100",
                "Peer: fe80::250:56ff:fe01:112%Vl4094 VRF: default - Keepalive time mismatch - Expected: 60 Actual: 50",
                "Interface: Ethernet1 VRF: MGMT - Hold time mismatch - Expected: 180 Actual: 150",
                "Interface: Ethernet1 VRF: MGMT - Keepalive time mismatch - Expected: 60 Actual: 50",
            ],
        },
    },
    (VerifyBGPPeerDropStats, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.8",
                                "dropStats": {
                                    "inDropAsloop": 0,
                                    "inDropClusterIdLoop": 0,
                                    "inDropMalformedMpbgp": 0,
                                    "inDropOrigId": 0,
                                    "inDropNhLocal": 0,
                                    "inDropNhAfV6": 0,
                                    "prefixDroppedMartianV4": 0,
                                    "prefixDroppedMaxRouteLimitViolatedV4": 0,
                                    "prefixDroppedMartianV6": 0,
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.9",
                                "dropStats": {
                                    "inDropAsloop": 0,
                                    "inDropClusterIdLoop": 0,
                                    "inDropMalformedMpbgp": 0,
                                    "inDropOrigId": 0,
                                    "inDropNhLocal": 0,
                                    "inDropNhAfV6": 0,
                                    "prefixDroppedMartianV4": 0,
                                    "prefixDroppedMaxRouteLimitViolatedV4": 0,
                                    "prefixDroppedMartianV6": 0,
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "10.100.0.8",
                    "vrf": "default",
                    "drop_stats": ["prefixDroppedMartianV4", "prefixDroppedMaxRouteLimitViolatedV4", "prefixDroppedMartianV6"],
                },
                {"peer_address": "10.100.0.9", "vrf": "MGMT", "drop_stats": ["inDropClusterIdLoop", "inDropOrigId", "inDropNhLocal"]},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerDropStats, "success-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "fd00:dc:1::1",
                                "dropStats": {
                                    "inDropAsloop": 0,
                                    "inDropClusterIdLoop": 0,
                                    "inDropMalformedMpbgp": 0,
                                    "inDropOrigId": 0,
                                    "inDropNhLocal": 0,
                                    "inDropNhAfV6": 0,
                                    "prefixDroppedMartianV4": 0,
                                    "prefixDroppedMaxRouteLimitViolatedV4": 0,
                                    "prefixDroppedMartianV6": 0,
                                },
                            },
                            {
                                "peerAddress": "fe80::250:56ff:fe01:112%Vl4094",
                                "dropStats": {
                                    "inDropAsloop": 0,
                                    "inDropClusterIdLoop": 0,
                                    "inDropMalformedMpbgp": 0,
                                    "inDropOrigId": 0,
                                    "inDropNhLocal": 0,
                                    "inDropNhAfV6": 0,
                                    "prefixDroppedMartianV4": 0,
                                    "prefixDroppedMaxRouteLimitViolatedV4": 0,
                                    "prefixDroppedMartianV6": 0,
                                },
                            },
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "dropStats": {
                                    "inDropAsloop": 0,
                                    "inDropClusterIdLoop": 0,
                                    "inDropMalformedMpbgp": 0,
                                    "inDropOrigId": 0,
                                    "inDropNhLocal": 0,
                                    "inDropNhAfV6": 0,
                                    "prefixDroppedMartianV4": 0,
                                    "prefixDroppedMaxRouteLimitViolatedV4": 0,
                                    "prefixDroppedMartianV6": 0,
                                },
                                "ifName": "Ethernet1",
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "fd00:dc:1::1",
                    "vrf": "default",
                    "drop_stats": ["prefixDroppedMartianV4", "prefixDroppedMaxRouteLimitViolatedV4", "prefixDroppedMartianV6"],
                },
                {
                    "peer_address": "fe80::250:56ff:fe01:112%Vl4094",
                    "vrf": "default",
                    "drop_stats": ["prefixDroppedMartianV4", "prefixDroppedMaxRouteLimitViolatedV4", "prefixDroppedMartianV6"],
                },
                {"interface": "Ethernet1", "vrf": "MGMT", "drop_stats": ["inDropClusterIdLoop", "inDropOrigId", "inDropNhLocal"]},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerDropStats, "failure-not-found"): {
        "eos_data": [{"vrfs": {}}],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "10.100.0.8",
                    "vrf": "default",
                    "drop_stats": ["prefixDroppedMartianV4", "prefixDroppedMaxRouteLimitViolatedV4", "prefixDroppedMartianV6"],
                },
                {"peer_address": "10.100.0.9", "vrf": "MGMT", "drop_stats": ["inDropClusterIdLoop", "inDropOrigId", "inDropNhLocal"]},
            ]
        },
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 10.100.0.8 VRF: default - Not found", "Peer: 10.100.0.9 VRF: MGMT - Not found"]},
    },
    (VerifyBGPPeerDropStats, "failure"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.8",
                                "dropStats": {
                                    "inDropAsloop": 0,
                                    "inDropClusterIdLoop": 0,
                                    "inDropMalformedMpbgp": 0,
                                    "inDropOrigId": 1,
                                    "inDropNhLocal": 1,
                                    "inDropNhAfV6": 0,
                                    "prefixDroppedMartianV4": 1,
                                    "prefixDroppedMaxRouteLimitViolatedV4": 1,
                                    "prefixDroppedMartianV6": 0,
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.9",
                                "dropStats": {
                                    "inDropAsloop": 0,
                                    "inDropClusterIdLoop": 0,
                                    "inDropMalformedMpbgp": 0,
                                    "inDropOrigId": 1,
                                    "inDropNhLocal": 1,
                                    "inDropNhAfV6": 0,
                                    "prefixDroppedMartianV4": 0,
                                    "prefixDroppedMaxRouteLimitViolatedV4": 0,
                                    "prefixDroppedMartianV6": 0,
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "10.100.0.8",
                    "vrf": "default",
                    "drop_stats": ["prefixDroppedMartianV4", "prefixDroppedMaxRouteLimitViolatedV4", "prefixDroppedMartianV6"],
                },
                {"peer_address": "10.100.0.9", "vrf": "MGMT", "drop_stats": ["inDropClusterIdLoop", "inDropOrigId", "inDropNhLocal"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - Non-zero NLRI drop statistics counter - prefixDroppedMartianV4: 1",
                "Peer: 10.100.0.8 VRF: default - Non-zero NLRI drop statistics counter - prefixDroppedMaxRouteLimitViolatedV4: 1",
                "Peer: 10.100.0.9 VRF: MGMT - Non-zero NLRI drop statistics counter - inDropOrigId: 1",
                "Peer: 10.100.0.9 VRF: MGMT - Non-zero NLRI drop statistics counter - inDropNhLocal: 1",
            ],
        },
    },
    (VerifyBGPPeerDropStats, "success-all-drop-stats"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.8",
                                "dropStats": {
                                    "inDropAsloop": 0,
                                    "inDropClusterIdLoop": 0,
                                    "inDropMalformedMpbgp": 0,
                                    "inDropOrigId": 0,
                                    "inDropNhLocal": 0,
                                    "inDropNhAfV6": 0,
                                    "prefixDroppedMartianV4": 0,
                                    "prefixDroppedMaxRouteLimitViolatedV4": 0,
                                    "prefixDroppedMartianV6": 0,
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.9",
                                "dropStats": {
                                    "inDropAsloop": 0,
                                    "inDropClusterIdLoop": 0,
                                    "inDropMalformedMpbgp": 0,
                                    "inDropOrigId": 0,
                                    "inDropNhLocal": 0,
                                    "inDropNhAfV6": 0,
                                    "prefixDroppedMartianV4": 0,
                                    "prefixDroppedMaxRouteLimitViolatedV4": 0,
                                    "prefixDroppedMartianV6": 0,
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerDropStats, "failure-all-drop-stats"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.8",
                                "dropStats": {
                                    "inDropAsloop": 3,
                                    "inDropClusterIdLoop": 0,
                                    "inDropMalformedMpbgp": 0,
                                    "inDropOrigId": 1,
                                    "inDropNhLocal": 1,
                                    "inDropNhAfV6": 0,
                                    "prefixDroppedMartianV4": 1,
                                    "prefixDroppedMaxRouteLimitViolatedV4": 1,
                                    "prefixDroppedMartianV6": 0,
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.9",
                                "dropStats": {
                                    "inDropAsloop": 2,
                                    "inDropClusterIdLoop": 0,
                                    "inDropMalformedMpbgp": 0,
                                    "inDropOrigId": 1,
                                    "inDropNhLocal": 1,
                                    "inDropNhAfV6": 0,
                                    "prefixDroppedMartianV4": 0,
                                    "prefixDroppedMaxRouteLimitViolatedV4": 0,
                                    "prefixDroppedMartianV6": 0,
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}]},
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - Non-zero NLRI drop statistics counter - inDropAsloop: 3",
                "Peer: 10.100.0.8 VRF: default - Non-zero NLRI drop statistics counter - inDropOrigId: 1",
                "Peer: 10.100.0.8 VRF: default - Non-zero NLRI drop statistics counter - inDropNhLocal: 1",
                "Peer: 10.100.0.8 VRF: default - Non-zero NLRI drop statistics counter - prefixDroppedMartianV4: 1",
                "Peer: 10.100.0.8 VRF: default - Non-zero NLRI drop statistics counter - prefixDroppedMaxRouteLimitViolatedV4: 1",
                "Peer: 10.100.0.9 VRF: MGMT - Non-zero NLRI drop statistics counter - inDropAsloop: 2",
                "Peer: 10.100.0.9 VRF: MGMT - Non-zero NLRI drop statistics counter - inDropOrigId: 1",
                "Peer: 10.100.0.9 VRF: MGMT - Non-zero NLRI drop statistics counter - inDropNhLocal: 1",
            ],
        },
    },
    (VerifyBGPPeerDropStats, "failure-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "fd00:dc:1::1",
                                "dropStats": {
                                    "inDropAsloop": 0,
                                    "inDropClusterIdLoop": 0,
                                    "inDropMalformedMpbgp": 0,
                                    "inDropOrigId": 0,
                                    "inDropNhLocal": 0,
                                    "inDropNhAfV6": 0,
                                    "prefixDroppedMartianV4": 4,
                                    "prefixDroppedMaxRouteLimitViolatedV4": 0,
                                    "prefixDroppedMartianV6": 2,
                                },
                            },
                            {
                                "peerAddress": "fe80::250:56ff:fe01:112%Vl4094",
                                "dropStats": {
                                    "inDropAsloop": 0,
                                    "inDropClusterIdLoop": 0,
                                    "inDropMalformedMpbgp": 0,
                                    "inDropOrigId": 0,
                                    "inDropNhLocal": 0,
                                    "inDropNhAfV6": 0,
                                    "prefixDroppedMartianV4": 0,
                                    "prefixDroppedMaxRouteLimitViolatedV4": 3,
                                    "prefixDroppedMartianV6": 2,
                                },
                            },
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "dropStats": {
                                    "inDropAsloop": 0,
                                    "inDropClusterIdLoop": 0,
                                    "inDropMalformedMpbgp": 0,
                                    "inDropOrigId": 3,
                                    "inDropNhLocal": 0,
                                    "inDropNhAfV6": 0,
                                    "prefixDroppedMartianV4": 0,
                                    "prefixDroppedMaxRouteLimitViolatedV4": 0,
                                    "prefixDroppedMartianV6": 0,
                                },
                                "ifName": "Ethernet1",
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {
                    "peer_address": "fd00:dc:1::1",
                    "vrf": "default",
                    "drop_stats": ["prefixDroppedMartianV4", "prefixDroppedMaxRouteLimitViolatedV4", "prefixDroppedMartianV6"],
                },
                {
                    "peer_address": "fe80::250:56ff:fe01:112%Vl4094",
                    "vrf": "default",
                    "drop_stats": ["prefixDroppedMartianV4", "prefixDroppedMaxRouteLimitViolatedV4", "prefixDroppedMartianV6"],
                },
                {"interface": "Ethernet1", "vrf": "MGMT", "drop_stats": ["inDropClusterIdLoop", "inDropOrigId", "inDropNhLocal"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: fd00:dc:1::1 VRF: default - Non-zero NLRI drop statistics counter - prefixDroppedMartianV4: 4",
                "Peer: fd00:dc:1::1 VRF: default - Non-zero NLRI drop statistics counter - prefixDroppedMartianV6: 2",
                "Peer: fe80::250:56ff:fe01:112%Vl4094 VRF: default - Non-zero NLRI drop statistics counter - prefixDroppedMaxRouteLimitViolatedV4: 3",
                "Peer: fe80::250:56ff:fe01:112%Vl4094 VRF: default - Non-zero NLRI drop statistics counter - prefixDroppedMartianV6: 2",
                "Interface: Ethernet1 VRF: MGMT - Non-zero NLRI drop statistics counter - inDropOrigId: 3",
            ],
        },
    },
    (VerifyBGPPeerUpdateErrors, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.8",
                                "peerInUpdateErrors": {
                                    "inUpdErrWithdraw": 0,
                                    "inUpdErrIgnore": 0,
                                    "inUpdErrDisableAfiSafi": 0,
                                    "disabledAfiSafi": "None",
                                    "lastUpdErrTime": 0,
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.9",
                                "peerInUpdateErrors": {
                                    "inUpdErrWithdraw": 0,
                                    "inUpdErrIgnore": 0,
                                    "inUpdErrDisableAfiSafi": 0,
                                    "disabledAfiSafi": "None",
                                    "lastUpdErrTime": 0,
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "update_errors": ["inUpdErrWithdraw", "inUpdErrIgnore", "disabledAfiSafi"]},
                {"peer_address": "10.100.0.9", "vrf": "MGMT", "update_errors": ["inUpdErrWithdraw", "inUpdErrIgnore", "disabledAfiSafi"]},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerUpdateErrors, "success-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "fd00:dc:1::1",
                                "peerInUpdateErrors": {
                                    "inUpdErrWithdraw": 0,
                                    "inUpdErrIgnore": 0,
                                    "inUpdErrDisableAfiSafi": 0,
                                    "disabledAfiSafi": "None",
                                    "lastUpdErrTime": 0,
                                },
                            },
                            {
                                "peerAddress": "fe80::250:56ff:fe01:112%Vl4094",
                                "peerInUpdateErrors": {
                                    "inUpdErrWithdraw": 0,
                                    "inUpdErrIgnore": 0,
                                    "inUpdErrDisableAfiSafi": 0,
                                    "disabledAfiSafi": "None",
                                    "lastUpdErrTime": 0,
                                },
                            },
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerInUpdateErrors": {
                                    "inUpdErrWithdraw": 0,
                                    "inUpdErrIgnore": 0,
                                    "inUpdErrDisableAfiSafi": 0,
                                    "disabledAfiSafi": "None",
                                    "lastUpdErrTime": 0,
                                },
                                "ifName": "Ethernet1",
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default", "update_errors": ["inUpdErrWithdraw", "inUpdErrIgnore", "disabledAfiSafi"]},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default", "update_errors": ["inUpdErrWithdraw", "inUpdErrIgnore", "disabledAfiSafi"]},
                {"interface": "Ethernet1", "vrf": "MGMT", "update_errors": ["inUpdErrWithdraw", "inUpdErrIgnore", "disabledAfiSafi"]},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerUpdateErrors, "failure-not-found"): {
        "eos_data": [{"vrfs": {}}],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "update_errors": ["inUpdErrWithdraw", "inUpdErrIgnore", "disabledAfiSafi"]},
                {"peer_address": "10.100.0.9", "vrf": "MGMT", "update_errors": ["inUpdErrWithdraw", "inUpdErrIgnore", "disabledAfiSafi"]},
            ]
        },
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 10.100.0.8 VRF: default - Not found", "Peer: 10.100.0.9 VRF: MGMT - Not found"]},
    },
    (VerifyBGPPeerUpdateErrors, "failure-errors"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.8",
                                "peerInUpdateErrors": {
                                    "inUpdErrWithdraw": 0,
                                    "inUpdErrIgnore": 0,
                                    "inUpdErrDisableAfiSafi": 0,
                                    "disabledAfiSafi": "ipv4Unicast",
                                    "lastUpdErrTime": 0,
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.9",
                                "peerInUpdateErrors": {
                                    "inUpdErrWithdraw": 1,
                                    "inUpdErrIgnore": 0,
                                    "inUpdErrDisableAfiSafi": 0,
                                    "disabledAfiSafi": "None",
                                    "lastUpdErrTime": 0,
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "update_errors": ["inUpdErrWithdraw", "inUpdErrIgnore", "disabledAfiSafi"]},
                {"peer_address": "10.100.0.9", "vrf": "MGMT", "update_errors": ["inUpdErrWithdraw", "inUpdErrIgnore", "disabledAfiSafi"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - Non-zero update error counter - disabledAfiSafi: ipv4Unicast",
                "Peer: 10.100.0.9 VRF: MGMT - Non-zero update error counter - inUpdErrWithdraw: 1",
            ],
        },
    },
    (VerifyBGPPeerUpdateErrors, "success-all-error-counters"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.8",
                                "peerInUpdateErrors": {
                                    "inUpdErrWithdraw": 0,
                                    "inUpdErrIgnore": 0,
                                    "inUpdErrDisableAfiSafi": 0,
                                    "disabledAfiSafi": "None",
                                    "lastUpdErrTime": 0,
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.9",
                                "peerInUpdateErrors": {
                                    "inUpdErrWithdraw": 0,
                                    "inUpdErrIgnore": 0,
                                    "inUpdErrDisableAfiSafi": 0,
                                    "disabledAfiSafi": "None",
                                    "lastUpdErrTime": 0,
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerUpdateErrors, "failure-all-error-counters"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.8",
                                "peerInUpdateErrors": {
                                    "inUpdErrWithdraw": 1,
                                    "inUpdErrIgnore": 0,
                                    "inUpdErrDisableAfiSafi": 0,
                                    "disabledAfiSafi": "ipv4Unicast",
                                    "lastUpdErrTime": 0,
                                },
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.9",
                                "peerInUpdateErrors": {
                                    "inUpdErrWithdraw": 1,
                                    "inUpdErrIgnore": 0,
                                    "inUpdErrDisableAfiSafi": 1,
                                    "disabledAfiSafi": "None",
                                    "lastUpdErrTime": 0,
                                },
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "update_errors": ["inUpdErrWithdraw", "inUpdErrIgnore", "disabledAfiSafi"]},
                {"peer_address": "10.100.0.9", "vrf": "MGMT", "update_errors": ["inUpdErrWithdraw", "inUpdErrIgnore", "disabledAfiSafi", "inUpdErrDisableAfiSafi"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - Non-zero update error counter - inUpdErrWithdraw: 1",
                "Peer: 10.100.0.8 VRF: default - Non-zero update error counter - disabledAfiSafi: ipv4Unicast",
                "Peer: 10.100.0.9 VRF: MGMT - Non-zero update error counter - inUpdErrWithdraw: 1",
                "Peer: 10.100.0.9 VRF: MGMT - Non-zero update error counter - inUpdErrDisableAfiSafi: 1",
            ],
        },
    },
    (VerifyBGPPeerUpdateErrors, "failure-all-not-found"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.8",
                                "peerInUpdateErrors": {"inUpdErrIgnore": 0, "inUpdErrDisableAfiSafi": 0, "disabledAfiSafi": "ipv4Unicast", "lastUpdErrTime": 0},
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.9",
                                "peerInUpdateErrors": {"inUpdErrWithdraw": 1, "inUpdErrIgnore": 0, "disabledAfiSafi": "None", "lastUpdErrTime": 0},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "update_errors": ["inUpdErrWithdraw", "inUpdErrIgnore", "disabledAfiSafi"]},
                {"peer_address": "10.100.0.9", "vrf": "MGMT", "update_errors": ["inUpdErrWithdraw", "inUpdErrIgnore", "disabledAfiSafi", "inUpdErrDisableAfiSafi"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - Non-zero update error counter - inUpdErrWithdraw: Not Found",
                "Peer: 10.100.0.8 VRF: default - Non-zero update error counter - disabledAfiSafi: ipv4Unicast",
                "Peer: 10.100.0.9 VRF: MGMT - Non-zero update error counter - inUpdErrWithdraw: 1",
                "Peer: 10.100.0.9 VRF: MGMT - Non-zero update error counter - inUpdErrDisableAfiSafi: Not Found",
            ],
        },
    },
    (VerifyBGPPeerUpdateErrors, "failure-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "fd00:dc:1::1",
                                "peerInUpdateErrors": {
                                    "inUpdErrWithdraw": 3,
                                    "inUpdErrIgnore": 0,
                                    "inUpdErrDisableAfiSafi": 0,
                                    "disabledAfiSafi": "None",
                                    "lastUpdErrTime": 0,
                                },
                            },
                            {
                                "peerAddress": "fe80::250:56ff:fe01:112%Vl4094",
                                "peerInUpdateErrors": {
                                    "inUpdErrWithdraw": 0,
                                    "inUpdErrIgnore": 3,
                                    "inUpdErrDisableAfiSafi": 0,
                                    "disabledAfiSafi": "None",
                                    "lastUpdErrTime": 0,
                                },
                            },
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerInUpdateErrors": {
                                    "inUpdErrWithdraw": 0,
                                    "inUpdErrIgnore": 0,
                                    "inUpdErrDisableAfiSafi": 0,
                                    "disabledAfiSafi": "ipv4Unicast",
                                    "lastUpdErrTime": 0,
                                },
                                "ifName": "Ethernet1",
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default", "update_errors": ["inUpdErrWithdraw", "inUpdErrIgnore", "disabledAfiSafi"]},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default", "update_errors": ["inUpdErrWithdraw", "inUpdErrIgnore", "disabledAfiSafi"]},
                {"interface": "Ethernet1", "vrf": "MGMT", "update_errors": ["inUpdErrWithdraw", "inUpdErrIgnore", "disabledAfiSafi"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: fd00:dc:1::1 VRF: default - Non-zero update error counter - inUpdErrWithdraw: 3",
                "Peer: fe80::250:56ff:fe01:112%Vl4094 VRF: default - Non-zero update error counter - inUpdErrIgnore: 3",
                "Interface: Ethernet1 VRF: MGMT - Non-zero update error counter - disabledAfiSafi: ipv4Unicast",
            ],
        },
    },
    (VerifyBgpRouteMaps, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.100.0.8", "routeMapInbound": "RM-MLAG-PEER-IN", "routeMapOutbound": "RM-MLAG-PEER-OUT"}]},
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.10", "routeMapInbound": "RM-MLAG-PEER-IN", "routeMapOutbound": "RM-MLAG-PEER-OUT"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "inbound_route_map": "RM-MLAG-PEER-IN", "outbound_route_map": "RM-MLAG-PEER-OUT"},
                {"peer_address": "10.100.0.10", "vrf": "MGMT", "inbound_route_map": "RM-MLAG-PEER-IN", "outbound_route_map": "RM-MLAG-PEER-OUT"},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBgpRouteMaps, "success-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "routeMapInbound": "RM-MLAG-PEER-IN", "routeMapOutbound": "RM-MLAG-PEER-OUT"},
                            {"peerAddress": "fe80::250:56ff:fe01:112%Vl4094", "routeMapInbound": "RM-MLAG-PEER-IN", "routeMapOutbound": "RM-MLAG-PEER-OUT"},
                        ]
                    },
                    "MGMT": {"peerList": [{"routeMapInbound": "RM-MLAG-PEER-IN", "routeMapOutbound": "RM-MLAG-PEER-OUT", "ifName": "Ethernet1"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default", "inbound_route_map": "RM-MLAG-PEER-IN", "outbound_route_map": "RM-MLAG-PEER-OUT"},
                {
                    "peer_address": "fe80::250:56ff:fe01:112%Vl4094",
                    "vrf": "default",
                    "inbound_route_map": "RM-MLAG-PEER-IN",
                    "outbound_route_map": "RM-MLAG-PEER-OUT",
                },
                {"interface": "Ethernet1", "vrf": "MGMT", "inbound_route_map": "RM-MLAG-PEER-IN", "outbound_route_map": "RM-MLAG-PEER-OUT"},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBgpRouteMaps, "failure-incorrect-route-map"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.100.0.8", "routeMapInbound": "RM-MLAG-PEER", "routeMapOutbound": "RM-MLAG-PEER"}]},
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.10", "routeMapInbound": "RM-MLAG-PEER", "routeMapOutbound": "RM-MLAG-PEER"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "inbound_route_map": "RM-MLAG-PEER-IN", "outbound_route_map": "RM-MLAG-PEER-OUT"},
                {"peer_address": "10.100.0.10", "vrf": "MGMT", "inbound_route_map": "RM-MLAG-PEER-IN", "outbound_route_map": "RM-MLAG-PEER-OUT"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - Inbound route-map mismatch - Expected: RM-MLAG-PEER-IN Actual: RM-MLAG-PEER",
                "Peer: 10.100.0.8 VRF: default - Outbound route-map mismatch - Expected: RM-MLAG-PEER-OUT Actual: RM-MLAG-PEER",
                "Peer: 10.100.0.10 VRF: MGMT - Inbound route-map mismatch - Expected: RM-MLAG-PEER-IN Actual: RM-MLAG-PEER",
                "Peer: 10.100.0.10 VRF: MGMT - Outbound route-map mismatch - Expected: RM-MLAG-PEER-OUT Actual: RM-MLAG-PEER",
            ],
        },
    },
    (VerifyBgpRouteMaps, "failure-incorrect-inbound-map"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.100.0.8", "routeMapInbound": "RM-MLAG-PEER", "routeMapOutbound": "RM-MLAG-PEER"}]},
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.10", "routeMapInbound": "RM-MLAG-PEER", "routeMapOutbound": "RM-MLAG-PEER"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "inbound_route_map": "RM-MLAG-PEER-IN"},
                {"peer_address": "10.100.0.10", "vrf": "MGMT", "inbound_route_map": "RM-MLAG-PEER-IN"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - Inbound route-map mismatch - Expected: RM-MLAG-PEER-IN Actual: RM-MLAG-PEER",
                "Peer: 10.100.0.10 VRF: MGMT - Inbound route-map mismatch - Expected: RM-MLAG-PEER-IN Actual: RM-MLAG-PEER",
            ],
        },
    },
    (VerifyBgpRouteMaps, "failure-route-maps-not-configured"): {
        "eos_data": [{"vrfs": {"default": {"peerList": [{"peerAddress": "10.100.0.8"}]}, "MGMT": {"peerList": [{"peerAddress": "10.100.0.10"}]}}}],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "inbound_route_map": "RM-MLAG-PEER-IN", "outbound_route_map": "RM-MLAG-PEER-OUT"},
                {"peer_address": "10.100.0.10", "vrf": "MGMT", "inbound_route_map": "RM-MLAG-PEER-IN", "outbound_route_map": "RM-MLAG-PEER-OUT"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - Inbound route-map mismatch - Expected: RM-MLAG-PEER-IN Actual: Not Configured",
                "Peer: 10.100.0.8 VRF: default - Outbound route-map mismatch - Expected: RM-MLAG-PEER-OUT Actual: Not Configured",
                "Peer: 10.100.0.10 VRF: MGMT - Inbound route-map mismatch - Expected: RM-MLAG-PEER-IN Actual: Not Configured",
                "Peer: 10.100.0.10 VRF: MGMT - Outbound route-map mismatch - Expected: RM-MLAG-PEER-OUT Actual: Not Configured",
            ],
        },
    },
    (VerifyBgpRouteMaps, "failure-peer-not-found"): {
        "eos_data": [{"vrfs": {"default": {"peerList": []}, "MGMT": {"peerList": []}}}],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "inbound_route_map": "RM-MLAG-PEER-IN"},
                {"peer_address": "10.100.0.10", "vrf": "MGMT", "inbound_route_map": "RM-MLAG-PEER-IN"},
            ]
        },
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 10.100.0.8 VRF: default - Not found", "Peer: 10.100.0.10 VRF: MGMT - Not found"]},
    },
    (VerifyBgpRouteMaps, "failure-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "routeMapInbound": "RM-MLAG-PEER-IN1", "routeMapOutbound": "RM-MLAG-PEER-OUT"},
                            {"peerAddress": "fe80::250:56ff:fe01:112%Vl4094", "routeMapInbound": "RM-MLAG-PEER-IN", "routeMapOutbound": "RM-MLAG-PEER-OUT1"},
                        ]
                    },
                    "MGMT": {"peerList": [{"routeMapInbound": "RM-MLAG-PEER-IN1", "routeMapOutbound": "RM-MLAG-PEER-OUT1", "ifName": "Ethernet1"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default", "inbound_route_map": "RM-MLAG-PEER-IN", "outbound_route_map": "RM-MLAG-PEER-OUT"},
                {
                    "peer_address": "fe80::250:56ff:fe01:112%Vl4094",
                    "vrf": "default",
                    "inbound_route_map": "RM-MLAG-PEER-IN",
                    "outbound_route_map": "RM-MLAG-PEER-OUT",
                },
                {"interface": "Ethernet1", "vrf": "MGMT", "inbound_route_map": "RM-MLAG-PEER-IN", "outbound_route_map": "RM-MLAG-PEER-OUT"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: fd00:dc:1::1 VRF: default - Inbound route-map mismatch - Expected: RM-MLAG-PEER-IN Actual: RM-MLAG-PEER-IN1",
                "Peer: fe80::250:56ff:fe01:112%Vl4094 VRF: default - Outbound route-map mismatch - Expected: RM-MLAG-PEER-OUT Actual: RM-MLAG-PEER-OUT1",
                "Interface: Ethernet1 VRF: MGMT - Inbound route-map mismatch - Expected: RM-MLAG-PEER-IN Actual: RM-MLAG-PEER-IN1",
                "Interface: Ethernet1 VRF: MGMT - Outbound route-map mismatch - Expected: RM-MLAG-PEER-OUT Actual: RM-MLAG-PEER-OUT1",
            ],
        },
    },
    (VerifyBGPPeerRouteLimit, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.100.0.8", "maxTotalRoutes": 12000, "totalRoutesWarnLimit": 10000}]},
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.9", "maxTotalRoutes": 10000, "totalRoutesWarnLimit": 9000}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "maximum_routes": 12000, "warning_limit": 10000},
                {"peer_address": "10.100.0.9", "vrf": "MGMT", "maximum_routes": 10000},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerRouteLimit, "success-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "maxTotalRoutes": 12000, "totalRoutesWarnLimit": 10000},
                            {"peerAddress": "fe80::250:56ff:fe01:112%Vl4094", "maxTotalRoutes": 12000, "totalRoutesWarnLimit": 10000},
                        ]
                    },
                    "MGMT": {"peerList": [{"maxTotalRoutes": 10000, "totalRoutesWarnLimit": 9000, "ifName": "Ethernet1"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default", "maximum_routes": 12000, "warning_limit": 10000},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default", "maximum_routes": 12000, "warning_limit": 10000},
                {"interface": "Ethernet1", "vrf": "MGMT", "maximum_routes": 10000},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerRouteLimit, "success-no-warning-limit"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.100.0.8", "maxTotalRoutes": 12000}]},
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.9", "maxTotalRoutes": 10000}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "maximum_routes": 12000, "warning_limit": 0},
                {"peer_address": "10.100.0.9", "vrf": "MGMT", "maximum_routes": 10000},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerRouteLimit, "failure-peer-not-found"): {
        "eos_data": [{"vrfs": {"default": {}, "MGMT": {}}}],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "maximum_routes": 12000, "warning_limit": 10000},
                {"peer_address": "10.100.0.9", "vrf": "MGMT", "maximum_routes": 10000, "warning_limit": 9000},
            ]
        },
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 10.100.0.8 VRF: default - Not found", "Peer: 10.100.0.9 VRF: MGMT - Not found"]},
    },
    (VerifyBGPPeerRouteLimit, "failure-incorrect-max-routes"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.100.0.8", "maxTotalRoutes": 13000, "totalRoutesWarnLimit": 11000}]},
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.9", "maxTotalRoutes": 11000, "totalRoutesWarnLimit": 10000}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "maximum_routes": 12000, "warning_limit": 10000},
                {"peer_address": "10.100.0.9", "vrf": "MGMT", "maximum_routes": 10000, "warning_limit": 9000},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - Maximum routes mismatch - Expected: 12000 Actual: 13000",
                "Peer: 10.100.0.8 VRF: default - Maximum routes warning limit mismatch - Expected: 10000 Actual: 11000",
                "Peer: 10.100.0.9 VRF: MGMT - Maximum routes mismatch - Expected: 10000 Actual: 11000",
                "Peer: 10.100.0.9 VRF: MGMT - Maximum routes warning limit mismatch - Expected: 9000 Actual: 10000",
            ],
        },
    },
    (VerifyBGPPeerRouteLimit, "failure-routes-not-found"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.100.0.8", "maxTotalRoutes": 12000}]},
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.9", "maxTotalRoutes": 10000}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "maximum_routes": 12000, "warning_limit": 10000},
                {"peer_address": "10.100.0.9", "vrf": "MGMT", "maximum_routes": 10000, "warning_limit": 9000},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - Maximum routes warning limit mismatch - Expected: 10000 Actual: 0",
                "Peer: 10.100.0.9 VRF: MGMT - Maximum routes warning limit mismatch - Expected: 9000 Actual: 0",
            ],
        },
    },
    (VerifyBGPPeerRouteLimit, "failure-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "maxTotalRoutes": 10000, "totalRoutesWarnLimit": 9000},
                            {"peerAddress": "fe80::250:56ff:fe01:112%Vl4094", "maxTotalRoutes": 10000, "totalRoutesWarnLimit": 9000},
                        ]
                    },
                    "MGMT": {"peerList": [{"maxTotalRoutes": 11000, "totalRoutesWarnLimit": 9000, "ifName": "Ethernet1"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default", "maximum_routes": 12000, "warning_limit": 10000},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default", "maximum_routes": 12000, "warning_limit": 10000},
                {"interface": "Ethernet1", "vrf": "MGMT", "maximum_routes": 10000},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: fd00:dc:1::1 VRF: default - Maximum routes mismatch - Expected: 12000 Actual: 10000",
                "Peer: fd00:dc:1::1 VRF: default - Maximum routes warning limit mismatch - Expected: 10000 Actual: 9000",
                "Peer: fe80::250:56ff:fe01:112%Vl4094 VRF: default - Maximum routes mismatch - Expected: 12000 Actual: 10000",
                "Peer: fe80::250:56ff:fe01:112%Vl4094 VRF: default - Maximum routes warning limit mismatch - Expected: 10000 Actual: 9000",
                "Interface: Ethernet1 VRF: MGMT - Maximum routes mismatch - Expected: 10000 Actual: 11000",
            ],
        },
    },
    (VerifyBGPPeerSession, "success-no-check-tcp-queues"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [{"peerAddress": "10.100.0.8", "state": "Established", "peerTcpInfo": {"outputQueueLength": 10, "inputQueueLength": 5}}]
                    },
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.9", "state": "Established", "peerTcpInfo": {"outputQueueLength": 10, "inputQueueLength": 5}}]},
                }
            }
        ],
        "inputs": {"check_tcp_queues": False, "bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerSession, "success-check-tcp-queues"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.100.0.8", "state": "Established", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]},
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.9", "state": "Established", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]},
                }
            }
        ],
        "inputs": {"check_tcp_queues": True, "bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerSession, "success-min-established-time"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.8",
                                "state": "Established",
                                "establishedTime": 169883,
                                "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.9",
                                "state": "Established",
                                "establishedTime": 169883,
                                "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "minimum_established_time": 10000,
            "check_tcp_queues": True,
            "bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}],
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerSession, "success-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "fd00:dc:1::1",
                                "state": "Established",
                                "establishedTime": 169883,
                                "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0},
                            },
                            {
                                "peerAddress": "fe80::250:56ff:fe01:112%Vl4094",
                                "state": "Established",
                                "establishedTime": 169883,
                                "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0},
                            },
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "state": "Established",
                                "establishedTime": 169883,
                                "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0},
                                "ifName": "Ethernet1",
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "minimum_established_time": 11000,
            "check_tcp_queues": True,
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default"},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default"},
                {"interface": "Ethernet1", "vrf": "MGMT"},
            ],
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerSession, "failure-peer-not-found"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.100.0.8", "state": "Established", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]}
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 10.100.0.9 VRF: MGMT - Not found"]},
    },
    (VerifyBGPPeerSession, "failure-not-established"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.100.0.8", "state": "Active", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]},
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.9", "state": "Active", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]},
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}]},
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - Incorrect session state - Expected: Established Actual: Active",
                "Peer: 10.100.0.9 VRF: MGMT - Incorrect session state - Expected: Established Actual: Active",
            ],
        },
    },
    (VerifyBGPPeerSession, "failure-check-tcp-queues"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [{"peerAddress": "10.100.0.8", "state": "Established", "peerTcpInfo": {"outputQueueLength": 10, "inputQueueLength": 5}}]
                    },
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.9", "state": "Established", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]},
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 10.100.0.8 VRF: default - Session has non-empty message queues - InQ: 5 OutQ: 10"]},
    },
    (VerifyBGPPeerSession, "failure-min-established-time"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.8",
                                "state": "Established",
                                "establishedTime": 9883,
                                "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.9",
                                "state": "Established",
                                "establishedTime": 9883,
                                "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "minimum_established_time": 10000,
            "check_tcp_queues": True,
            "bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}],
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - BGP session not established for the minimum required duration - Expected: 10000s Actual: 9883s",
                "Peer: 10.100.0.9 VRF: MGMT - BGP session not established for the minimum required duration - Expected: 10000s Actual: 9883s",
            ],
        },
    },
    (VerifyBGPPeerGroup, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "10.100.0.8", "peerGroupName": "IPv4-UNDERLAY-PEERS"},
                            {"peerAddress": "10.100.4.5", "peerGroupName": "MLAG-IPv4-UNDERLAY-PEER"},
                            {"peerAddress": "10.100.1.1", "peerGroupName": "EVPN-OVERLAY-PEERS"},
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {"peerAddress": "10.100.0.10", "peerGroupName": "IPv4-UNDERLAY-PEERS"},
                            {"peerAddress": "10.100.1.2", "peerGroupName": "EVPN-OVERLAY-PEERS"},
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "peer_group": "IPv4-UNDERLAY-PEERS"},
                {"peer_address": "10.100.0.10", "vrf": "MGMT", "peer_group": "IPv4-UNDERLAY-PEERS"},
                {"peer_address": "10.100.1.1", "vrf": "default", "peer_group": "EVPN-OVERLAY-PEERS"},
                {"peer_address": "10.100.1.2", "vrf": "MGMT", "peer_group": "EVPN-OVERLAY-PEERS"},
                {"peer_address": "10.100.4.5", "vrf": "default", "peer_group": "MLAG-IPv4-UNDERLAY-PEER"},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerGroup, "success-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "peerGroupName": "IPv4-UNDERLAY-PEERS"},
                            {"peerAddress": "fe80::250:56ff:fe01:112%Vl4094", "peerGroupName": "EVPN-OVERLAY-PEERS"},
                        ]
                    },
                    "MGMT": {"peerList": [{"peerGroupName": "EVPN-OVERLAY-PEERS", "ifName": "Ethernet1"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default", "peer_group": "IPv4-UNDERLAY-PEERS"},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default", "peer_group": "EVPN-OVERLAY-PEERS"},
                {"interface": "Ethernet1", "vrf": "MGMT", "peer_group": "EVPN-OVERLAY-PEERS"},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerGroup, "failure-incorrect-peer-group"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "10.100.0.8", "peerGroupName": "UNDERLAY-PEERS"},
                            {"peerAddress": "10.100.1.1", "peerGroupName": "OVERLAY-PEERS"},
                            {"peerAddress": "10.100.4.5", "peerGroupName": "UNDERLAY-PEER"},
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {"peerAddress": "10.100.0.10", "peerGroupName": "UNDERLAY-PEERS"},
                            {"peerAddress": "10.100.1.2", "peerGroupName": "OVERLAY-PEERS"},
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "peer_group": "IPv4-UNDERLAY-PEERS"},
                {"peer_address": "10.100.0.10", "vrf": "MGMT", "peer_group": "IPv4-UNDERLAY-PEERS"},
                {"peer_address": "10.100.1.1", "vrf": "default", "peer_group": "EVPN-OVERLAY-PEERS"},
                {"peer_address": "10.100.1.2", "vrf": "MGMT", "peer_group": "EVPN-OVERLAY-PEERS"},
                {"peer_address": "10.100.4.5", "vrf": "default", "peer_group": "MLAG-IPv4-UNDERLAY-PEER"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - Incorrect peer group configured - Expected: IPv4-UNDERLAY-PEERS Actual: UNDERLAY-PEERS",
                "Peer: 10.100.0.10 VRF: MGMT - Incorrect peer group configured - Expected: IPv4-UNDERLAY-PEERS Actual: UNDERLAY-PEERS",
                "Peer: 10.100.1.1 VRF: default - Incorrect peer group configured - Expected: EVPN-OVERLAY-PEERS Actual: OVERLAY-PEERS",
                "Peer: 10.100.1.2 VRF: MGMT - Incorrect peer group configured - Expected: EVPN-OVERLAY-PEERS Actual: OVERLAY-PEERS",
                "Peer: 10.100.4.5 VRF: default - Incorrect peer group configured - Expected: MLAG-IPv4-UNDERLAY-PEER Actual: UNDERLAY-PEER",
            ],
        },
    },
    (VerifyBGPPeerGroup, "failure-peers-not-found"): {
        "eos_data": [{"vrfs": {"default": {"peerList": []}, "MGMT": {"peerList": []}}}],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "peer_group": "IPv4-UNDERLAY-PEERS"},
                {"peer_address": "10.100.0.10", "vrf": "MGMT", "peer_group": "IPv4-UNDERLAY-PEERS"},
                {"peer_address": "10.100.1.1", "vrf": "default", "peer_group": "EVPN-OVERLAY-PEERS"},
                {"peer_address": "10.100.1.2", "vrf": "MGMT", "peer_group": "EVPN-OVERLAY-PEERS"},
                {"peer_address": "10.100.4.5", "vrf": "default", "peer_group": "MLAG-IPv4-UNDERLAY-PEER"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - Not found",
                "Peer: 10.100.0.10 VRF: MGMT - Not found",
                "Peer: 10.100.1.1 VRF: default - Not found",
                "Peer: 10.100.1.2 VRF: MGMT - Not found",
                "Peer: 10.100.4.5 VRF: default - Not found",
            ],
        },
    },
    (VerifyBGPPeerGroup, "failure-peer-group-not-found"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.100.0.8"}, {"peerAddress": "10.100.1.1"}, {"peerAddress": "10.100.4.5"}]},
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.10"}, {"peerAddress": "10.100.1.2"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "peer_group": "IPv4-UNDERLAY-PEERS"},
                {"peer_address": "10.100.0.10", "vrf": "MGMT", "peer_group": "IPv4-UNDERLAY-PEERS"},
                {"peer_address": "10.100.1.1", "vrf": "default", "peer_group": "EVPN-OVERLAY-PEERS"},
                {"peer_address": "10.100.1.2", "vrf": "MGMT", "peer_group": "EVPN-OVERLAY-PEERS"},
                {"peer_address": "10.100.4.5", "vrf": "default", "peer_group": "MLAG-IPv4-UNDERLAY-PEER"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - Incorrect peer group configured - Expected: IPv4-UNDERLAY-PEERS Actual: Not Found",
                "Peer: 10.100.0.10 VRF: MGMT - Incorrect peer group configured - Expected: IPv4-UNDERLAY-PEERS Actual: Not Found",
                "Peer: 10.100.1.1 VRF: default - Incorrect peer group configured - Expected: EVPN-OVERLAY-PEERS Actual: Not Found",
                "Peer: 10.100.1.2 VRF: MGMT - Incorrect peer group configured - Expected: EVPN-OVERLAY-PEERS Actual: Not Found",
                "Peer: 10.100.4.5 VRF: default - Incorrect peer group configured - Expected: MLAG-IPv4-UNDERLAY-PEER Actual: Not Found",
            ],
        },
    },
    (VerifyBGPPeerGroup, "failure-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "peerGroupName": "IPv6-UNDERLAY-PEERS"},
                            {"peerAddress": "fe80::250:56ff:fe01:112%Vl4094", "peerGroupName": "EVPN-UNDERLAY-PEERS"},
                        ]
                    },
                    "MGMT": {"peerList": [{"peerGroupName": "EVPN-UNDERLAY-PEERS", "ifName": "Ethernet1"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default", "peer_group": "IPv4-UNDERLAY-PEERS"},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default", "peer_group": "EVPN-OVERLAY-PEERS"},
                {"interface": "Ethernet1", "vrf": "MGMT", "peer_group": "EVPN-OVERLAY-PEERS"},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: fd00:dc:1::1 VRF: default - Incorrect peer group configured - Expected: IPv4-UNDERLAY-PEERS Actual: IPv6-UNDERLAY-PEERS",
                "Peer: fe80::250:56ff:fe01:112%Vl4094 VRF: default - Incorrect peer group configured - Expected: EVPN-OVERLAY-PEERS Actual: EVPN-UNDERLAY-PEERS",
                "Interface: Ethernet1 VRF: MGMT - Incorrect peer group configured - Expected: EVPN-OVERLAY-PEERS Actual: EVPN-UNDERLAY-PEERS",
            ],
        },
    },
    (VerifyBGPPeerSessionRibd, "success-no-check-tcp-queues"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [{"peerAddress": "10.100.0.8", "state": "Established", "peerTcpInfo": {"outputQueueLength": 10, "inputQueueLength": 5}}]
                    },
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.9", "state": "Established", "peerTcpInfo": {"outputQueueLength": 10, "inputQueueLength": 5}}]},
                }
            }
        ],
        "inputs": {"check_tcp_queues": False, "bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerSessionRibd, "success-check-tcp-queues"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.8",
                                "state": "Established",
                                "establishedTime": 169883,
                                "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.9",
                                "state": "Established",
                                "establishedTime": 169883,
                                "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "minimum_established_time": 10000,
            "check_tcp_queues": True,
            "bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}],
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerSessionRibd, "success-min-established-time"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.100.0.8", "state": "Established", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]},
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.9", "state": "Established", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]},
                }
            }
        ],
        "inputs": {"check_tcp_queues": True, "bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerSessionRibd, "success-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "state": "Established", "peerTcpInfo": {"outputQueueLength": 10, "inputQueueLength": 5}},
                            {
                                "peerAddress": "fe80::250:56ff:fe01:112%Vl4094",
                                "state": "Established",
                                "peerTcpInfo": {"outputQueueLength": 10, "inputQueueLength": 5},
                            },
                        ]
                    },
                    "MGMT": {"peerList": [{"state": "Established", "peerTcpInfo": {"outputQueueLength": 10, "inputQueueLength": 5}, "ifName": "Ethernet1"}]},
                }
            }
        ],
        "inputs": {
            "check_tcp_queues": False,
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default"},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default"},
                {"interface": "Ethernet1", "vrf": "MGMT"},
            ],
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerSessionRibd, "failure-peer-not-found"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.100.0.8", "state": "Established", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]}
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 10.100.0.9 VRF: MGMT - Not found"]},
    },
    (VerifyBGPPeerSessionRibd, "failure-not-established"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.100.0.8", "state": "Active", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]},
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.9", "state": "Active", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]},
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}]},
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - Incorrect session state - Expected: Established Actual: Active",
                "Peer: 10.100.0.9 VRF: MGMT - Incorrect session state - Expected: Established Actual: Active",
            ],
        },
    },
    (VerifyBGPPeerSessionRibd, "failure-check-tcp-queues"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [{"peerAddress": "10.100.0.8", "state": "Established", "peerTcpInfo": {"outputQueueLength": 10, "inputQueueLength": 5}}]
                    },
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.9", "state": "Established", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]},
                }
            }
        ],
        "inputs": {"bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 10.100.0.8 VRF: default - Session has non-empty message queues - InQ: 5 OutQ: 10"]},
    },
    (VerifyBGPPeerSessionRibd, "failure-min-established-time"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.8",
                                "state": "Established",
                                "establishedTime": 9883,
                                "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                    "MGMT": {
                        "peerList": [
                            {
                                "peerAddress": "10.100.0.9",
                                "state": "Established",
                                "establishedTime": 9883,
                                "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0},
                            }
                        ]
                    },
                }
            }
        ],
        "inputs": {
            "minimum_established_time": 10000,
            "bgp_peers": [{"peer_address": "10.100.0.8", "vrf": "default"}, {"peer_address": "10.100.0.9", "vrf": "MGMT"}],
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - BGP session not established for the minimum required duration - Expected: 10000s Actual: 9883s",
                "Peer: 10.100.0.9 VRF: MGMT - BGP session not established for the minimum required duration - Expected: 10000s Actual: 9883s",
            ],
        },
    },
    (VerifyBGPPeerSessionRibd, "failure-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "fd00:dc:1::1", "state": "Active", "peerTcpInfo": {"outputQueueLength": 10, "inputQueueLength": 5}},
                            {"peerAddress": "fe80::250:56ff:fe01:112%Vl4094", "state": "Active", "peerTcpInfo": {"outputQueueLength": 10, "inputQueueLength": 5}},
                        ]
                    },
                    "MGMT": {"peerList": [{"state": "Active", "peerTcpInfo": {"outputQueueLength": 10, "inputQueueLength": 5}, "ifName": "Ethernet1"}]},
                }
            }
        ],
        "inputs": {
            "check_tcp_queues": False,
            "bgp_peers": [
                {"peer_address": "fd00:dc:1::1", "vrf": "default"},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default"},
                {"interface": "Ethernet1", "vrf": "MGMT"},
            ],
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: fd00:dc:1::1 VRF: default - Incorrect session state - Expected: Established Actual: Active",
                "Peer: fe80::250:56ff:fe01:112%Vl4094 VRF: default - Incorrect session state - Expected: Established Actual: Active",
                "Interface: Ethernet1 VRF: MGMT - Incorrect session state - Expected: Established Actual: Active",
            ],
        },
    },
    (VerifyBGPPeersHealthRibd, "success-no-check-tcp-queues"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [{"peerAddress": "10.100.0.8", "state": "Established", "peerTcpInfo": {"outputQueueLength": 10, "inputQueueLength": 5}}]
                    },
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.9", "state": "Established", "peerTcpInfo": {"outputQueueLength": 10, "inputQueueLength": 5}}]},
                }
            }
        ],
        "inputs": {"check_tcp_queues": False},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeersHealthRibd, "success-check-tcp-queues"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.100.0.8", "state": "Established", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]},
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.9", "state": "Established", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]},
                }
            }
        ],
        "inputs": {"check_tcp_queues": True},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeersHealthRibd, "failure-not-established"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.100.0.8", "state": "Active", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]},
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.9", "state": "Active", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]},
                }
            }
        ],
        "inputs": {},
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - Incorrect session state - Expected: Established Actual: Active",
                "Peer: 10.100.0.9 VRF: MGMT - Incorrect session state - Expected: Established Actual: Active",
            ],
        },
    },
    (VerifyBGPPeersHealthRibd, "failure-check-tcp-queues"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [{"peerAddress": "10.100.0.8", "state": "Established", "peerTcpInfo": {"outputQueueLength": 10, "inputQueueLength": 5}}]
                    },
                    "MGMT": {"peerList": [{"peerAddress": "10.100.0.9", "state": "Established", "peerTcpInfo": {"outputQueueLength": 0, "inputQueueLength": 0}}]},
                }
            }
        ],
        "inputs": {},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 10.100.0.8 VRF: default - Session has non-empty message queues - InQ: 5 OutQ: 10"]},
    },
    (VerifyBGPNlriAcceptance, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.100.1.5",
                        "asn": "65102",
                        "peers": {
                            "10.100.0.8": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 17, "nlrisAccepted": 17},
                                "l2VpnEvpn": {"afiSafiState": "negotiated", "nlrisReceived": 56, "nlrisAccepted": 56},
                            }
                        },
                    },
                    "MGMT": {
                        "vrf": "MGMT",
                        "routerId": "10.100.1.5",
                        "asn": "65102",
                        "peers": {
                            "10.100.4.5": {
                                "peerState": "Established",
                                "peerAsn": "65102",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 14, "nlrisAccepted": 14},
                                "l2VpnEvpn": {"afiSafiState": "negotiated", "nlrisReceived": 56, "nlrisAccepted": 56},
                            }
                        },
                    },
                }
            },
            {},
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "capabilities": ["Ipv4 Unicast", "L2vpnEVPN"]},
                {"peer_address": "10.100.4.5", "vrf": "MGMT", "capabilities": ["ipv4 Unicast", "L2vpnEVPN"]},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPNlriAcceptance, "success-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "1.1.1.1",
                        "asn": "65001",
                        "peers": {
                            "2001:db8:1::2": {
                                "peerState": "Established",
                                "peerAsn": "65003",
                                "ipv6Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 2, "nlrisAccepted": 2},
                            },
                            "fe80::2%Et1": {
                                "peerState": "Established",
                                "peerAsn": "65002",
                                "ipv6Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 1, "nlrisAccepted": 1},
                            },
                            "fe80::3%Et2": {
                                "peerState": "Established",
                                "peerAsn": "65002",
                                "ipv6Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 1, "nlrisAccepted": 1},
                            },
                        },
                    }
                }
            },
            {"vrfs": {"default": {"peerList": [{"peerAddress": "fe80::3%Et2", "ifName": "Ethernet2"}]}}},
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "2001:db8:1::2", "vrf": "default", "capabilities": ["ipv6Unicast"]},
                {"peer_address": "fe80::2%Et1", "vrf": "default", "capabilities": ["ipv6Unicast"]},
                {"interface": "Ethernet2", "vrf": "default", "capabilities": ["ipv6Unicast"]},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPNlriAcceptance, "failure-vrf-not-configured"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"vrf": "default", "routerId": "10.100.1.5", "asn": "65102", "peers": {}},
                    "MGMT": {"vrf": "MGMT", "routerId": "10.100.1.5", "asn": "65102", "peers": {}},
                }
            },
            {},
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "capabilities": ["Ipv4 Unicast", "L2vpnEVPN"]},
                {"peer_address": "10.100.4.5", "vrf": "MGMT", "capabilities": ["ipv4 Unicast", "L2vpnEVPN"]},
            ]
        },
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 10.100.0.8 VRF: default - Not found", "Peer: 10.100.4.5 VRF: MGMT - Not found"]},
    },
    (VerifyBGPNlriAcceptance, "failure-capability-not-found"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.100.1.5",
                        "asn": "65102",
                        "peers": {
                            "10.100.0.8": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 17, "nlrisAccepted": 17},
                            }
                        },
                    },
                    "MGMT": {
                        "vrf": "MGMT",
                        "routerId": "10.100.1.5",
                        "asn": "65102",
                        "peers": {
                            "10.100.4.5": {
                                "peerState": "Established",
                                "peerAsn": "65102",
                                "l2VpnEvpn": {"afiSafiState": "negotiated", "nlrisReceived": 56, "nlrisAccepted": 56},
                            }
                        },
                    },
                }
            },
            {},
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "capabilities": ["Ipv4 Unicast", "L2vpnEVPN"]},
                {"peer_address": "10.100.4.5", "vrf": "MGMT", "capabilities": ["ipv4 Unicast", "L2vpnEVPN"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": ["Peer: 10.100.0.8 VRF: default - l2VpnEvpn not found", "Peer: 10.100.4.5 VRF: MGMT - ipv4Unicast not found"],
        },
    },
    (VerifyBGPNlriAcceptance, "failure-capability-not-negotiated"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.100.1.5",
                        "asn": "65102",
                        "peers": {
                            "10.100.0.8": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4Unicast": {"afiSafiState": "configured", "nlrisReceived": 17, "nlrisAccepted": 17},
                            }
                        },
                    },
                    "MGMT": {
                        "vrf": "MGMT",
                        "routerId": "10.100.1.5",
                        "asn": "65102",
                        "peers": {
                            "10.100.4.5": {
                                "peerState": "Established",
                                "peerAsn": "65102",
                                "l2VpnEvpn": {"afiSafiState": "configured", "nlrisReceived": 56, "nlrisAccepted": 56},
                            }
                        },
                    },
                }
            },
            {},
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "capabilities": ["Ipv4 Unicast", "L2vpnEVPN"]},
                {"peer_address": "10.100.4.5", "vrf": "MGMT", "capabilities": ["ipv4 Unicast", "L2vpnEVPN"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default - ipv4Unicast not negotiated",
                "Peer: 10.100.0.8 VRF: default - l2VpnEvpn not found",
                "Peer: 10.100.4.5 VRF: MGMT - ipv4Unicast not found",
                "Peer: 10.100.4.5 VRF: MGMT - l2VpnEvpn not negotiated",
            ],
        },
    },
    (VerifyBGPNlriAcceptance, "failure-nlris-not-accepted"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.100.1.5",
                        "asn": "65102",
                        "peers": {
                            "10.100.0.8": {
                                "peerState": "Established",
                                "peerAsn": "65100",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 17, "nlrisAccepted": 16},
                                "l2VpnEvpn": {"afiSafiState": "negotiated", "nlrisReceived": 58, "nlrisAccepted": 56},
                            }
                        },
                    },
                    "MGMT": {
                        "vrf": "MGMT",
                        "routerId": "10.100.1.5",
                        "asn": "65102",
                        "peers": {
                            "10.100.4.5": {
                                "peerState": "Established",
                                "peerAsn": "65102",
                                "ipv4Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 15, "nlrisAccepted": 14},
                                "l2VpnEvpn": {"afiSafiState": "negotiated", "nlrisReceived": 59, "nlrisAccepted": 56},
                            }
                        },
                    },
                }
            },
            {},
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.100.0.8", "vrf": "default", "capabilities": ["Ipv4 Unicast", "L2vpnEVPN"]},
                {"peer_address": "10.100.4.5", "vrf": "MGMT", "capabilities": ["ipv4 Unicast", "L2vpnEVPN"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.100.0.8 VRF: default AFI/SAFI: ipv4Unicast - Some NLRI were filtered or rejected - Accepted: 16 Received: 17",
                "Peer: 10.100.0.8 VRF: default AFI/SAFI: l2VpnEvpn - Some NLRI were filtered or rejected - Accepted: 56 Received: 58",
                "Peer: 10.100.4.5 VRF: MGMT AFI/SAFI: ipv4Unicast - Some NLRI were filtered or rejected - Accepted: 14 Received: 15",
                "Peer: 10.100.4.5 VRF: MGMT AFI/SAFI: l2VpnEvpn - Some NLRI were filtered or rejected - Accepted: 56 Received: 59",
            ],
        },
    },
    (VerifyBGPNlriAcceptance, "failure-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "1.1.1.1",
                        "asn": "65001",
                        "peers": {
                            "2001:db8:1::2": {
                                "peerState": "Established",
                                "peerAsn": "65003",
                                "ipv6Unicast": {"afiSafiState": "configured", "nlrisReceived": 2, "nlrisAccepted": 3},
                            },
                            "fe80::2%Et1": {
                                "peerState": "Established",
                                "peerAsn": "65002",
                                "ipv6Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 2, "nlrisAccepted": 1},
                            },
                            "fe80::3%Et2": {
                                "peerState": "Established",
                                "peerAsn": "65002",
                                "ipv6Unicast": {"afiSafiState": "negotiated", "nlrisReceived": 3, "nlrisAccepted": 1},
                            },
                        },
                    }
                }
            },
            {"vrfs": {"default": {"peerList": [{"peerAddress": "fe80::3%Et2", "ifName": "Ethernet2"}]}}},
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "2001:db8:1::2", "vrf": "default", "capabilities": ["ipv6Unicast"]},
                {"peer_address": "fe80::2%Et1", "vrf": "default", "capabilities": ["ipv6Unicast"]},
                {"interface": "Ethernet2", "vrf": "default", "capabilities": ["ipv6Unicast"]},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 2001:db8:1::2 VRF: default - ipv6Unicast not negotiated",
                "Peer: 2001:db8:1::2 VRF: default AFI/SAFI: ipv6Unicast - Some NLRI were filtered or rejected - Accepted: 3 Received: 2",
                "Peer: fe80::2%Et1 VRF: default AFI/SAFI: ipv6Unicast - Some NLRI were filtered or rejected - Accepted: 1 Received: 2",
                "Interface: Ethernet2 VRF: default AFI/SAFI: ipv6Unicast - Some NLRI were filtered or rejected - Accepted: 1 Received: 3",
            ],
        },
    },
    (VerifyBGPNlriAcceptance, "failure-rfc5549-not-found"): {
        "eos_data": [{"vrfs": {"default": {}}}, {"vrfs": {"default": {"peerList": []}}}],
        "inputs": {"bgp_peers": [{"interface": "Ethernet2", "vrf": "default", "capabilities": ["ipv6Unicast"]}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Interface: Ethernet2 VRF: default - Not found"]},
    },
    (VerifyBGPRoutePaths, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "10.100.0.128/31": {
                                "bgpRoutePaths": [
                                    {"nextHop": "10.100.0.10", "routeType": {"origin": "Igp"}},
                                    {"nextHop": "10.100.4.5", "routeType": {"origin": "Incomplete"}},
                                ]
                            }
                        }
                    },
                    "MGMT": {
                        "bgpRouteEntries": {
                            "10.100.0.130/31": {
                                "bgpRoutePaths": [
                                    {"nextHop": "10.100.0.8", "routeType": {"origin": "Igp"}},
                                    {"nextHop": "10.100.0.10", "routeType": {"origin": "Igp"}},
                                ]
                            }
                        }
                    },
                }
            }
        ],
        "inputs": {
            "route_entries": [
                {
                    "prefix": "10.100.0.128/31",
                    "vrf": "default",
                    "paths": [{"nexthop": "10.100.0.10", "origin": "Igp"}, {"nexthop": "10.100.4.5", "origin": "Incomplete"}],
                },
                {"prefix": "10.100.0.130/31", "vrf": "MGMT", "paths": [{"nexthop": "10.100.0.8", "origin": "Igp"}, {"nexthop": "10.100.0.10", "origin": "Igp"}]},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPRoutePaths, "failure-origin-not-correct"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "bgpRouteEntries": {
                            "10.100.0.128/31": {
                                "bgpRoutePaths": [
                                    {"nextHop": "10.100.0.10", "routeType": {"origin": "Igp"}},
                                    {"nextHop": "10.100.4.5", "routeType": {"origin": "Incomplete"}},
                                ]
                            }
                        }
                    },
                    "MGMT": {
                        "bgpRouteEntries": {
                            "10.100.0.130/31": {
                                "bgpRoutePaths": [
                                    {"nextHop": "10.100.0.8", "routeType": {"origin": "Igp"}},
                                    {"nextHop": "10.100.0.10", "routeType": {"origin": "Igp"}},
                                ]
                            }
                        }
                    },
                }
            }
        ],
        "inputs": {
            "route_entries": [
                {
                    "prefix": "10.100.0.128/31",
                    "vrf": "default",
                    "paths": [{"nexthop": "10.100.0.10", "origin": "Incomplete"}, {"nexthop": "10.100.4.5", "origin": "Igp"}],
                },
                {
                    "prefix": "10.100.0.130/31",
                    "vrf": "MGMT",
                    "paths": [{"nexthop": "10.100.0.8", "origin": "Incomplete"}, {"nexthop": "10.100.0.10", "origin": "Incomplete"}],
                },
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Prefix: 10.100.0.128/31 VRF: default Next-hop: 10.100.0.10 Origin: Incomplete - Origin mismatch - Actual: Igp",
                "Prefix: 10.100.0.128/31 VRF: default Next-hop: 10.100.4.5 Origin: Igp - Origin mismatch - Actual: Incomplete",
                "Prefix: 10.100.0.130/31 VRF: MGMT Next-hop: 10.100.0.8 Origin: Incomplete - Origin mismatch - Actual: Igp",
                "Prefix: 10.100.0.130/31 VRF: MGMT Next-hop: 10.100.0.10 Origin: Incomplete - Origin mismatch - Actual: Igp",
            ],
        },
    },
    (VerifyBGPRoutePaths, "failure-path-not-found"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"bgpRouteEntries": {"10.100.0.128/31": {"bgpRoutePaths": [{"nextHop": "10.100.0.15", "routeType": {"origin": "Igp"}}]}}},
                    "MGMT": {"bgpRouteEntries": {"10.100.0.130/31": {"bgpRoutePaths": [{"nextHop": "10.100.0.15", "routeType": {"origin": "Igp"}}]}}},
                }
            }
        ],
        "inputs": {
            "route_entries": [
                {
                    "prefix": "10.100.0.128/31",
                    "vrf": "default",
                    "paths": [{"nexthop": "10.100.0.10", "origin": "Incomplete"}, {"nexthop": "10.100.4.5", "origin": "Igp"}],
                },
                {
                    "prefix": "10.100.0.130/31",
                    "vrf": "MGMT",
                    "paths": [{"nexthop": "10.100.0.8", "origin": "Incomplete"}, {"nexthop": "10.100.0.10", "origin": "Incomplete"}],
                },
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Prefix: 10.100.0.128/31 VRF: default Next-hop: 10.100.0.10 Origin: Incomplete - Path not found",
                "Prefix: 10.100.0.128/31 VRF: default Next-hop: 10.100.4.5 Origin: Igp - Path not found",
                "Prefix: 10.100.0.130/31 VRF: MGMT Next-hop: 10.100.0.8 Origin: Incomplete - Path not found",
                "Prefix: 10.100.0.130/31 VRF: MGMT Next-hop: 10.100.0.10 Origin: Incomplete - Path not found",
            ],
        },
    },
    (VerifyBGPRoutePaths, "failure-prefix-not-found"): {
        "eos_data": [{"vrfs": {"default": {"bgpRouteEntries": {}}, "MGMT": {"bgpRouteEntries": {}}}}],
        "inputs": {
            "route_entries": [
                {
                    "prefix": "10.100.0.128/31",
                    "vrf": "default",
                    "paths": [{"nexthop": "10.100.0.10", "origin": "Incomplete"}, {"nexthop": "10.100.4.5", "origin": "Igp"}],
                },
                {
                    "prefix": "10.100.0.130/31",
                    "vrf": "MGMT",
                    "paths": [{"nexthop": "10.100.0.8", "origin": "Incomplete"}, {"nexthop": "10.100.0.10", "origin": "Incomplete"}],
                },
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": ["Prefix: 10.100.0.128/31 VRF: default - Prefix not found", "Prefix: 10.100.0.130/31 VRF: MGMT - Prefix not found"],
        },
    },
    (VerifyBGPRouteECMP, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.111.254.1",
                        "asn": "65101",
                        "bgpRouteEntries": {
                            "10.111.134.0/24": {
                                "address": "10.111.134.0",
                                "maskLength": 24,
                                "bgpRoutePaths": [
                                    {"nextHop": "10.111.2.0", "routeType": {"valid": True, "active": True, "ecmpHead": True, "ecmp": True, "ecmpContributor": True}},
                                    {
                                        "nextHop": "10.111.1.0",
                                        "routeType": {"valid": True, "active": False, "ecmpHead": False, "ecmp": True, "ecmpContributor": True},
                                    },
                                ],
                                "totalPaths": 2,
                            }
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "routes": {
                            "10.111.112.0/24": {"routeType": "eBGP", "vias": [{"interface": "Vlan112"}]},
                            "10.111.134.0/24": {
                                "routeType": "eBGP",
                                "vias": [{"nexthopAddr": "10.111.1.0", "interface": "Ethernet2"}, {"nexthopAddr": "10.111.2.0", "interface": "Ethernet3"}],
                                "directlyConnected": False,
                            },
                        }
                    }
                }
            },
        ],
        "inputs": {"route_entries": [{"prefix": "10.111.134.0/24", "vrf": "default", "ecmp_count": 2}]},
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPRouteECMP, "failure-prefix-not-found-bgp-table"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.111.254.1",
                        "asn": "65101",
                        "bgpRouteEntries": {
                            "10.111.134.0/24": {
                                "address": "10.111.134.0",
                                "maskLength": 24,
                                "bgpRoutePaths": [
                                    {"nextHop": "10.111.1.0", "routeType": {"valid": True, "active": True, "ecmpHead": True, "ecmp": True, "ecmpContributor": True}},
                                    {
                                        "nextHop": "10.111.2.0",
                                        "routeType": {"valid": True, "active": False, "ecmpHead": False, "ecmp": True, "ecmpContributor": True},
                                    },
                                    {
                                        "nextHop": "10.255.255.2",
                                        "routeType": {"valid": True, "active": False, "ecmpHead": False, "ecmp": False, "ecmpContributor": False},
                                    },
                                ],
                                "totalPaths": 3,
                            }
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "routes": {
                            "10.111.112.0/24": {"routeType": "eBGP", "vias": [{"interface": "Vlan112"}]},
                            "10.111.134.0/24": {
                                "routeType": "eBGP",
                                "vias": [{"nexthopAddr": "10.111.1.0", "interface": "Ethernet2"}, {"nexthopAddr": "10.111.2.0", "interface": "Ethernet3"}],
                                "directlyConnected": False,
                            },
                        }
                    }
                }
            },
        ],
        "inputs": {"route_entries": [{"prefix": "10.111.124.0/24", "vrf": "default", "ecmp_count": 2}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Prefix: 10.111.124.0/24 VRF: default - Prefix not found in BGP table"]},
    },
    (VerifyBGPRouteECMP, "failure-valid-active-ecmp-head-not-found"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.111.254.1",
                        "asn": "65101",
                        "bgpRouteEntries": {
                            "10.111.134.0/24": {
                                "address": "10.111.134.0",
                                "maskLength": 24,
                                "bgpRoutePaths": [
                                    {
                                        "nextHop": "10.111.1.0",
                                        "routeType": {"valid": False, "active": True, "ecmpHead": False, "ecmp": True, "ecmpContributor": True},
                                    },
                                    {
                                        "nextHop": "10.111.2.0",
                                        "routeType": {"valid": False, "active": True, "ecmpHead": True, "ecmp": True, "ecmpContributor": True},
                                    },
                                    {
                                        "nextHop": "10.255.255.2",
                                        "routeType": {"valid": True, "active": False, "ecmpHead": False, "ecmp": False, "ecmpContributor": False},
                                    },
                                ],
                                "totalPaths": 3,
                            }
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "routes": {
                            "10.111.112.0/24": {"routeType": "eBGP", "vias": [{"interface": "Vlan112"}]},
                            "10.111.134.0/24": {
                                "routeType": "eBGP",
                                "vias": [{"nexthopAddr": "10.111.1.0", "interface": "Ethernet2"}, {"nexthopAddr": "10.111.2.0", "interface": "Ethernet3"}],
                                "directlyConnected": False,
                            },
                        }
                    }
                }
            },
        ],
        "inputs": {"route_entries": [{"prefix": "10.111.134.0/24", "vrf": "default", "ecmp_count": 2}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Prefix: 10.111.134.0/24 VRF: default - Valid and active ECMP head not found"]},
    },
    (VerifyBGPRouteECMP, "failure-ecmp-count-mismatch"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.111.254.1",
                        "asn": "65101",
                        "bgpRouteEntries": {
                            "10.111.134.0/24": {
                                "address": "10.111.134.0",
                                "maskLength": 24,
                                "bgpRoutePaths": [
                                    {"nextHop": "10.111.1.0", "routeType": {"valid": True, "active": True, "ecmpHead": True, "ecmp": True, "ecmpContributor": True}},
                                    {
                                        "nextHop": "10.111.2.0",
                                        "routeType": {"valid": False, "active": True, "ecmpHead": True, "ecmp": True, "ecmpContributor": True},
                                    },
                                    {
                                        "nextHop": "10.255.255.2",
                                        "routeType": {"valid": True, "active": False, "ecmpHead": False, "ecmp": False, "ecmpContributor": False},
                                    },
                                ],
                                "totalPaths": 3,
                            }
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "routes": {
                            "10.111.112.0/24": {"routeType": "eBGP", "vias": [{"interface": "Vlan112"}]},
                            "10.111.134.0/24": {
                                "routeType": "eBGP",
                                "vias": [{"nexthopAddr": "10.111.1.0", "interface": "Ethernet2"}, {"nexthopAddr": "10.111.2.0", "interface": "Ethernet3"}],
                                "directlyConnected": False,
                            },
                        }
                    }
                }
            },
        ],
        "inputs": {"route_entries": [{"prefix": "10.111.134.0/24", "vrf": "default", "ecmp_count": 2}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Prefix: 10.111.134.0/24 VRF: default - ECMP count mismatch - Expected: 2 Actual: 1"]},
    },
    (VerifyBGPRouteECMP, "failure-prefix-not-found-routing-table"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.111.254.1",
                        "asn": "65101",
                        "bgpRouteEntries": {
                            "10.111.134.0/24": {
                                "address": "10.111.134.0",
                                "maskLength": 24,
                                "bgpRoutePaths": [
                                    {"nextHop": "10.111.1.0", "routeType": {"valid": True, "active": True, "ecmpHead": True, "ecmp": True, "ecmpContributor": True}},
                                    {
                                        "nextHop": "10.111.2.0",
                                        "routeType": {"valid": True, "active": False, "ecmpHead": False, "ecmp": True, "ecmpContributor": True},
                                    },
                                    {
                                        "nextHop": "10.255.255.2",
                                        "routeType": {"valid": True, "active": False, "ecmpHead": False, "ecmp": False, "ecmpContributor": False},
                                    },
                                ],
                                "totalPaths": 3,
                            }
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "routes": {
                            "10.111.112.0/24": {"routeType": "eBGP", "vias": [{"interface": "Vlan112"}]},
                            "10.111.114.0/24": {
                                "routeType": "eBGP",
                                "vias": [{"nexthopAddr": "10.111.1.0", "interface": "Ethernet2"}, {"nexthopAddr": "10.111.2.0", "interface": "Ethernet3"}],
                                "directlyConnected": False,
                            },
                        }
                    }
                }
            },
        ],
        "inputs": {"route_entries": [{"prefix": "10.111.134.0/24", "vrf": "default", "ecmp_count": 2}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Prefix: 10.111.134.0/24 VRF: default - Prefix not found in routing table"]},
    },
    (VerifyBGPRouteECMP, "failure-nexthops-mismatch"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "vrf": "default",
                        "routerId": "10.111.254.1",
                        "asn": "65101",
                        "bgpRouteEntries": {
                            "10.111.134.0/24": {
                                "address": "10.111.134.0",
                                "maskLength": 24,
                                "bgpRoutePaths": [
                                    {"nextHop": "10.111.1.0", "routeType": {"valid": True, "active": True, "ecmpHead": True, "ecmp": True, "ecmpContributor": True}},
                                    {
                                        "nextHop": "10.111.2.0",
                                        "routeType": {"valid": True, "active": False, "ecmpHead": False, "ecmp": True, "ecmpContributor": True},
                                    },
                                    {
                                        "nextHop": "10.255.255.2",
                                        "routeType": {"valid": True, "active": False, "ecmpHead": False, "ecmp": False, "ecmpContributor": False},
                                    },
                                ],
                                "totalPaths": 3,
                            }
                        },
                    }
                }
            },
            {
                "vrfs": {
                    "default": {
                        "routes": {
                            "10.111.112.0/24": {"routeType": "eBGP", "vias": [{"interface": "Vlan112"}]},
                            "10.111.134.0/24": {"routeType": "eBGP", "vias": [{"nexthopAddr": "10.111.1.0", "interface": "Ethernet2"}], "directlyConnected": False},
                        }
                    }
                }
            },
        ],
        "inputs": {"route_entries": [{"prefix": "10.111.134.0/24", "vrf": "default", "ecmp_count": 2}]},
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Prefix: 10.111.134.0/24 VRF: default - Nexthops count mismatch - BGP: 2 RIB: 1"]},
    },
    (VerifyBGPRedistribution, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "afiSafiConfig": {
                            "v4u": {
                                "redistributedRoutes": [
                                    {"proto": "Connected", "includeLeaked": True, "routeMap": "RM-CONN-2-BGP"},
                                    {"proto": "Static", "includeLeaked": True, "routeMap": "RM-CONN-2-BGP"},
                                ]
                            },
                            "v6m": {
                                "redistributedRoutes": [
                                    {"proto": "OSPFv3 External", "routeMap": "RM-CONN-2-BGP"},
                                    {"proto": "IS-IS", "includeLeaked": True, "routeMap": "RM-CONN-2-BGP"},
                                ]
                            },
                        }
                    },
                    "test": {
                        "afiSafiConfig": {
                            "v4m": {
                                "redistributedRoutes": [
                                    {"proto": "AttachedHost", "routeMap": "RM-CONN-2-BGP"},
                                    {"proto": "OSPF Internal", "includeLeaked": True, "routeMap": "RM-CONN-2-BGP"},
                                ]
                            },
                            "v6u": {
                                "redistributedRoutes": [
                                    {"proto": "DHCP", "routeMap": "RM-CONN-2-BGP"},
                                    {"proto": "Bgp", "includeLeaked": True, "routeMap": "RM-CONN-2-BGP"},
                                ]
                            },
                        }
                    },
                }
            }
        ],
        "inputs": {
            "vrfs": [
                {
                    "vrf": "default",
                    "address_families": [
                        {
                            "afi_safi": "ipv4Unicast",
                            "redistributed_routes": [
                                {"proto": "Connected", "include_leaked": True, "route_map": "RM-CONN-2-BGP"},
                                {"proto": "Static", "include_leaked": True, "route_map": "RM-CONN-2-BGP"},
                            ],
                        },
                        {
                            "afi_safi": "IPv6 multicast",
                            "redistributed_routes": [
                                {"proto": "OSPFv3 External", "route_map": "RM-CONN-2-BGP"},
                                {"proto": "IS-IS", "include_leaked": True, "route_map": "RM-CONN-2-BGP"},
                            ],
                        },
                    ],
                },
                {
                    "vrf": "test",
                    "address_families": [
                        {
                            "afi_safi": "ipv4 Multicast",
                            "redistributed_routes": [
                                {"proto": "AttachedHost", "route_map": "RM-CONN-2-BGP"},
                                {"proto": "OSPF Internal", "include_leaked": True, "route_map": "RM-CONN-2-BGP"},
                            ],
                        },
                        {
                            "afi_safi": "IPv6Unicast",
                            "redistributed_routes": [
                                {"proto": "DHCP", "route_map": "RM-CONN-2-BGP"},
                                {"proto": "Bgp", "include_leaked": True, "route_map": "RM-CONN-2-BGP"},
                            ],
                        },
                    ],
                },
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPRedistribution, "failure-vrf-not-found"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"afiSafiConfig": {"v6m": {"redistributedRoutes": [{"proto": "Connected", "routeMap": "RM-CONN-2-BGP"}]}}},
                    "tenant": {"afiSafiConfig": {"v4u": {"redistributedRoutes": [{"proto": "Connected"}]}}},
                }
            }
        ],
        "inputs": {
            "vrfs": [
                {
                    "vrf": "default",
                    "address_families": [
                        {"afi_safi": "ipv6 Multicast", "redistributed_routes": [{"proto": "Connected", "include_leaked": False, "route_map": "RM-CONN-2-BGP"}]}
                    ],
                },
                {
                    "vrf": "test",
                    "address_families": [
                        {"afi_safi": "ipv6 Multicast", "redistributed_routes": [{"proto": "Connected", "include_leaked": True, "route_map": "RM-CONN-2-BGP"}]}
                    ],
                },
            ]
        },
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["VRF: test - Not configured"]},
    },
    (VerifyBGPRedistribution, "failure-afi-safi-config-not-found"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"afiSafiConfig": {"v6m": {}}},
                    "test": {"afiSafiConfig": {"v4u": {"redistributedRoutes": [{"proto": "Connected", "routeMap": "RM-CONN-2-BGP"}]}}},
                }
            }
        ],
        "inputs": {
            "vrfs": [
                {
                    "vrf": "default",
                    "address_families": [
                        {
                            "afi_safi": "ipv6 Multicast",
                            "redistributed_routes": [
                                {"proto": "Connected", "include_leaked": True, "route_map": "RM-CONN-2-BGP"},
                                {"proto": "Static", "include_leaked": True, "route_map": "RM-CONN-2-BGP"},
                            ],
                        }
                    ],
                }
            ]
        },
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["VRF: default, AFI-SAFI: IPv6 Multicast - Not redistributed"]},
    },
    (VerifyBGPRedistribution, "failure-expected-proto-not-found"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "afiSafiConfig": {
                            "v4m": {
                                "redistributedRoutes": [{"proto": "AttachedHost", "routeMap": "RM-CONN-2-BGP"}, {"proto": "IS-IS", "routeMap": "RM-MLAG-PEER-IN"}]
                            }
                        }
                    },
                    "test": {"afiSafiConfig": {"v6u": {"redistributedRoutes": [{"proto": "Static", "routeMap": "RM-CONN-2-BGP"}]}}},
                }
            }
        ],
        "inputs": {
            "vrfs": [
                {
                    "vrf": "default",
                    "address_families": [
                        {
                            "afi_safi": "ipv4 multicast",
                            "redistributed_routes": [
                                {"proto": "OSPFv3 External", "include_leaked": True, "route_map": "RM-CONN-2-BGP"},
                                {"proto": "OSPFv3 Nssa-External", "include_leaked": True, "route_map": "RM-CONN-2-BGP"},
                            ],
                        }
                    ],
                },
                {
                    "vrf": "test",
                    "address_families": [
                        {
                            "afi_safi": "IPv6Unicast",
                            "redistributed_routes": [
                                {"proto": "DHCP", "route_map": "RM-CONN-2-BGP"},
                                {"proto": "Bgp", "include_leaked": True, "route_map": "RM-CONN-2-BGP"},
                            ],
                        }
                    ],
                },
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "VRF: default, AFI-SAFI: IPv4 Multicast, Proto: OSPFv3 External - Not configured",
                "VRF: default, AFI-SAFI: IPv4 Multicast, Proto: OSPFv3 Nssa-External - Not configured",
                "VRF: test, AFI-SAFI: IPv6 Unicast, Proto: DHCP - Not configured",
                "VRF: test, AFI-SAFI: IPv6 Unicast, Proto: Bgp - Not configured",
            ],
        },
    },
    (VerifyBGPRedistribution, "failure-route-map-not-found"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"afiSafiConfig": {"v4u": {"redistributedRoutes": [{"proto": "Connected", "routeMap": "RM-CONN-10-BGP"}, {"proto": "Static"}]}}},
                    "test": {"afiSafiConfig": {"v6u": {"redistributedRoutes": [{"proto": "EOS SDK", "routeMap": "RM-MLAG-PEER-IN"}, {"proto": "DHCP"}]}}},
                }
            }
        ],
        "inputs": {
            "vrfs": [
                {
                    "vrf": "default",
                    "address_families": [
                        {
                            "afi_safi": "ipv4 UNicast",
                            "redistributed_routes": [{"proto": "Connected", "route_map": "RM-CONN-2-BGP"}, {"proto": "Static", "route_map": "RM-CONN-2-BGP"}],
                        }
                    ],
                },
                {
                    "vrf": "test",
                    "address_families": [
                        {
                            "afi_safi": "ipv6-Unicast",
                            "redistributed_routes": [{"proto": "User", "route_map": "RM-CONN-2-BGP"}, {"proto": "DHCP", "route_map": "RM-CONN-2-BGP"}],
                        }
                    ],
                },
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "VRF: default, AFI-SAFI: IPv4 Unicast, Proto: Connected, Route Map: RM-CONN-2-BGP - Route map mismatch - Actual: RM-CONN-10-BGP",
                "VRF: default, AFI-SAFI: IPv4 Unicast, Proto: Static, Route Map: RM-CONN-2-BGP - Route map mismatch - Actual: Not Found",
                "VRF: test, AFI-SAFI: IPv6 Unicast, Proto: EOS SDK, Route Map: RM-CONN-2-BGP - Route map mismatch - Actual: RM-MLAG-PEER-IN",
                "VRF: test, AFI-SAFI: IPv6 Unicast, Proto: DHCP, Route Map: RM-CONN-2-BGP - Route map mismatch - Actual: Not Found",
            ],
        },
    },
    (VerifyBGPRedistribution, "failure-incorrect-value-include-leaked"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "afiSafiConfig": {
                            "v4m": {
                                "redistributedRoutes": [
                                    {"proto": "Connected", "routeMap": "RM-CONN-2-BGP"},
                                    {"proto": "IS-IS", "includeLeaked": False, "routeMap": "RM-CONN-2-BGP"},
                                ]
                            }
                        }
                    },
                    "test": {
                        "afiSafiConfig": {
                            "v6u": {
                                "redistributedRoutes": [
                                    {"proto": "Dynamic", "routeMap": "RM-CONN-2-BGP"},
                                    {"proto": "Bgp", "includeLeaked": True, "routeMap": "RM-CONN-2-BGP"},
                                ]
                            }
                        }
                    },
                }
            }
        ],
        "inputs": {
            "vrfs": [
                {
                    "vrf": "default",
                    "address_families": [
                        {"afi_safi": "ipv4-multicast", "redistributed_routes": [{"proto": "IS-IS", "include_leaked": True, "route_map": "RM-CONN-2-BGP"}]}
                    ],
                },
                {
                    "vrf": "test",
                    "address_families": [
                        {
                            "afi_safi": "IPv6_unicast",
                            "redistributed_routes": [
                                {"proto": "Dynamic", "route_map": "RM-CONN-2-BGP"},
                                {"proto": "Bgp", "include_leaked": False, "route_map": "RM-CONN-2-BGP"},
                            ],
                        }
                    ],
                },
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "VRF: default, AFI-SAFI: IPv4 Multicast, Proto: IS-IS, Include Leaked: True, Route Map: RM-CONN-2-BGP - Include leaked mismatch - Actual: False",
                "VRF: test, AFI-SAFI: IPv6 Unicast, Proto: Bgp, Route Map: RM-CONN-2-BGP - Include leaked mismatch - Actual: True",
            ],
        },
    },
    (VerifyBGPPeerTtlMultiHops, "success"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.111.0.1", "ttl": 2, "maxTtlHops": 2}, {"peerAddress": "10.111.0.2", "ttl": 1, "maxTtlHops": 1}]},
                    "Test": {"peerList": [{"peerAddress": "10.111.0.3", "ttl": 255, "maxTtlHops": 255}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.111.0.1", "vrf": "default", "ttl": 2, "max_ttl_hops": 2},
                {"peer_address": "10.111.0.2", "vrf": "default", "ttl": 1, "max_ttl_hops": 1},
                {"peer_address": "10.111.0.3", "vrf": "Test", "ttl": 255, "max_ttl_hops": 255},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerTtlMultiHops, "success-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "10.111.0.1", "ttl": 2, "maxTtlHops": 2},
                            {"peerAddress": "fe80::250:56ff:fe01:112%Vl4094", "ttl": 1, "maxTtlHops": 1},
                        ]
                    },
                    "Test": {"peerList": [{"ttl": 255, "maxTtlHops": 255, "ifName": "Ethernet1"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.111.0.1", "vrf": "default", "ttl": 2, "max_ttl_hops": 2},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default", "ttl": 1, "max_ttl_hops": 1},
                {"interface": "Ethernet1", "vrf": "Test", "ttl": 255, "max_ttl_hops": 255},
            ]
        },
        "expected": {"result": AntaTestStatus.SUCCESS},
    },
    (VerifyBGPPeerTtlMultiHops, "failure-peer-not-found"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.111.0.4", "ttl": 2, "maxTtlHops": 2}, {"peerAddress": "10.111.0.5", "ttl": 1, "maxTtlHops": 1}]},
                    "Test": {"peerList": [{"peerAddress": "10.111.0.6", "ttl": 255, "maxTtlHops": 255}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.111.0.1", "vrf": "default", "ttl": 2, "max_ttl_hops": 2},
                {"peer_address": "10.111.0.2", "vrf": "Test", "ttl": 255, "max_ttl_hops": 255},
            ]
        },
        "expected": {"result": AntaTestStatus.FAILURE, "messages": ["Peer: 10.111.0.1 VRF: default - Not found", "Peer: 10.111.0.2 VRF: Test - Not found"]},
    },
    (VerifyBGPPeerTtlMultiHops, "failure-ttl-time-mismatch"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.111.0.1", "ttl": 12, "maxTtlHops": 2}, {"peerAddress": "10.111.0.2", "ttl": 120, "maxTtlHops": 1}]},
                    "Test": {"peerList": [{"peerAddress": "10.111.0.3", "ttl": 205, "maxTtlHops": 255}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.111.0.1", "vrf": "default", "ttl": 2, "max_ttl_hops": 2},
                {"peer_address": "10.111.0.2", "vrf": "default", "ttl": 1, "max_ttl_hops": 1},
                {"peer_address": "10.111.0.3", "vrf": "Test", "ttl": 255, "max_ttl_hops": 255},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.111.0.1 VRF: default - TTL mismatch - Expected: 2 Actual: 12",
                "Peer: 10.111.0.2 VRF: default - TTL mismatch - Expected: 1 Actual: 120",
                "Peer: 10.111.0.3 VRF: Test - TTL mismatch - Expected: 255 Actual: 205",
            ],
        },
    },
    (VerifyBGPPeerTtlMultiHops, "failure-max-ttl-hops-mismatch"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {"peerList": [{"peerAddress": "10.111.0.1", "ttl": 2, "maxTtlHops": 12}, {"peerAddress": "10.111.0.2", "ttl": 1, "maxTtlHops": 100}]},
                    "Test": {"peerList": [{"peerAddress": "10.111.0.3", "ttl": 255, "maxTtlHops": 205}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.111.0.1", "vrf": "default", "ttl": 2, "max_ttl_hops": 2},
                {"peer_address": "10.111.0.2", "vrf": "default", "ttl": 1, "max_ttl_hops": 1},
                {"peer_address": "10.111.0.3", "vrf": "Test", "ttl": 255, "max_ttl_hops": 255},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.111.0.1 VRF: default - Max TTL Hops mismatch - Expected: 2 Actual: 12",
                "Peer: 10.111.0.2 VRF: default - Max TTL Hops mismatch - Expected: 1 Actual: 100",
                "Peer: 10.111.0.3 VRF: Test - Max TTL Hops mismatch - Expected: 255 Actual: 205",
            ],
        },
    },
    (VerifyBGPPeerTtlMultiHops, "failure-ipv6-rfc5549"): {
        "eos_data": [
            {
                "vrfs": {
                    "default": {
                        "peerList": [
                            {"peerAddress": "10.111.0.1", "ttl": 3, "maxTtlHops": 3},
                            {"peerAddress": "fe80::250:56ff:fe01:112%Vl4094", "ttl": 2, "maxTtlHops": 1},
                        ]
                    },
                    "Test": {"peerList": [{"ttl": 250, "maxTtlHops": 250, "ifName": "Ethernet1"}]},
                }
            }
        ],
        "inputs": {
            "bgp_peers": [
                {"peer_address": "10.111.0.1", "vrf": "default", "ttl": 2, "max_ttl_hops": 2},
                {"peer_address": "fe80::250:56ff:fe01:112%Vl4094", "vrf": "default", "ttl": 1, "max_ttl_hops": 1},
                {"interface": "Ethernet1", "vrf": "Test", "ttl": 255, "max_ttl_hops": 255},
            ]
        },
        "expected": {
            "result": AntaTestStatus.FAILURE,
            "messages": [
                "Peer: 10.111.0.1 VRF: default - TTL mismatch - Expected: 2 Actual: 3",
                "Peer: 10.111.0.1 VRF: default - Max TTL Hops mismatch - Expected: 2 Actual: 3",
                "Peer: fe80::250:56ff:fe01:112%Vl4094 VRF: default - TTL mismatch - Expected: 1 Actual: 2",
                "Interface: Ethernet1 VRF: Test - TTL mismatch - Expected: 255 Actual: 250",
                "Interface: Ethernet1 VRF: Test - Max TTL Hops mismatch - Expected: 255 Actual: 250",
            ],
        },
    },
}
