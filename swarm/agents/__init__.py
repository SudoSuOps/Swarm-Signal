"""Swarm Agents — Registry Pattern
===================================
All agents must be registered here. No ad-hoc agent creation.
"""

from .swarmcode import SwarmCodeAgent
from .swarmcre import SwarmCREAgent
from .swarmmed import SwarmMedAgent

AGENTS: dict[str, type] = {
    "swarmcode": SwarmCodeAgent,
    "swarmcre": SwarmCREAgent,
    "swarmmed": SwarmMedAgent,
}
