"""
Groundtruth Purple Agent for DeFiGym.

A baseline purple agent that returns the actual exploit from DeFiHackLabs,
providing a 100% accuracy baseline for testing the evaluation pipeline.
"""

from purple.agent import GroundtruthAgent
from purple.executor import PurpleExecutor

__all__ = ["GroundtruthAgent", "PurpleExecutor"]
