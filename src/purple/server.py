"""
Groundtruth Purple Agent Server.

A2A server for the baseline purple agent that returns actual exploits
from the DeFiHackLabs repository.
"""

import argparse
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uvicorn
from dotenv import load_dotenv

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from purple.agent import GroundtruthAgent
from purple.executor import PurpleExecutor

# Load environment variables
load_dotenv()


def create_agent_card(card_url: str) -> AgentCard:
    """
    Create the Groundtruth Agent card.

    Args:
        card_url: URL to advertise in the agent card

    Returns:
        AgentCard for the Groundtruth Agent
    """
    skill = AgentSkill(
        id="groundtruth_exploit",
        name="Groundtruth Exploit Provider",
        description="""Returns the actual exploit from DeFiHackLabs repository.

This is a baseline/groundtruth agent for testing the evaluation pipeline.
It parses the contract path from the task description and returns the
actual exploit code, providing a 100% accuracy baseline.

Use this agent to:
- Verify the green agent evaluation pipeline works correctly
- Establish baseline metrics for the benchmark
- Test the end-to-end assessment flow""",
        tags=["groundtruth", "baseline", "defi", "exploit"],
    )

    agent_card = AgentCard(
        name="Groundtruth Exploit Agent",
        description="""Groundtruth baseline purple agent for DeFiGym.

This agent returns the actual exploit code from the DeFiHackLabs
repository, providing a 100% accuracy baseline for testing.

It parses the contract path from the green agent's task description
and returns the corresponding exploit file.""",
        url=card_url,
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=False),
        skills=[skill],
    )

    return agent_card


def main():
    parser = argparse.ArgumentParser(description="Run the Groundtruth Purple Agent.")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind the server"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9010,
        help="Port to bind the server"
    )
    parser.add_argument(
        "--card-url",
        type=str,
        help="URL to advertise in the agent card"
    )
    parser.add_argument(
        "--defihacklabs-repo",
        type=str,
        default=os.environ.get("DEFIHACKLABS_REPO", "./data/defihacklabs"),
        help="Path to DeFiHackLabs repository"
    )
    args = parser.parse_args()

    # Create agent
    agent = GroundtruthAgent(defihacklabs_repo=args.defihacklabs_repo)
    executor = PurpleExecutor(agent)

    # Create agent card
    card_url = args.card_url or f"http://{args.host}:{args.port}/"
    agent_card = create_agent_card(card_url)

    # Create request handler and server
    request_handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    print(f"Starting Groundtruth Purple Agent at {card_url}")
    print(f"DeFiHackLabs repo: {args.defihacklabs_repo}")

    uvicorn.run(server.build(), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
