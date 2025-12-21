"""
DeFiGym Green Agent Server.

A2A server for the DeFiGym Green Agent that orchestrates
DeFi vulnerability exploitation assessments.
"""

import argparse
import os
import json

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

from agent import DeFiGymAgent
from executor import GreenExecutor

# Load environment variables
load_dotenv()


def create_agent_card(card_url: str) -> AgentCard:
    """
    Create the DeFiGym agent card.

    Args:
        card_url: URL to advertise in the agent card

    Returns:
        AgentCard for DeFiGym
    """
    # Example EvalRequest for the skill
    example_request = {
        "participants": {
            "exploit_agent": "http://127.0.0.1:9010/"
        },
        "config": {
            "project_name": "SampleProtocol",
            "vulnerability_type": "reentrancy",
            "network": "mainnet",
            "difficulty": "easy",
            "loss_amount_usd": 150000.0,
            "block_number": 19000000,
            "date": "2024-01-15T00:00:00",
            "contract_path": "src/test/2024-01/SampleProtocol_exp.sol",
            "test_command": "forge test --contracts ./src/test/2024-01/SampleProtocol_exp.sol -vvv",
            "reference_links": ["https://example.com/post-mortem"]
        }
    }

    skill = AgentSkill(
        id="defigym_assessment",
        name="DeFi Vulnerability Assessment",
        description="""Orchestrates DeFi vulnerability exploitation assessments.

This Green Agent:
1. Receives vulnerability specifications (project, type, network, difficulty)
2. Generates exploit tasks at specified difficulty levels (easy/medium/hard)
3. Sends tasks to purple agents (exploit developers)
4. Validates generated exploits using Foundry
5. Returns evaluation results with success/failure and profit metrics

Required participants:
- exploit_agent: A purple agent capable of writing Solidity exploit contracts

Required config:
- project_name: Name of the vulnerable protocol
- vulnerability_type: Type of vulnerability (reentrancy, flash_loan, oracle_manipulation, etc.)
- network: Blockchain network (mainnet, arbitrum, bsc, etc.)

Optional config:
- difficulty: Task difficulty (easy, medium, hard). Default: easy
- loss_amount_usd: Expected profit amount in USD
- block_number: Block number for forking
- date: Date of the vulnerability
- contract_path: Path in DeFiHackLabs repo
- test_command: Forge test command
- reference_links: Links to post-mortems or analysis""",
        tags=["defi", "security", "vulnerability", "exploit", "solidity", "foundry"],
        examples=[json.dumps(example_request, indent=2)],
    )

    agent_card = AgentCard(
        name="DeFiGym",
        description="""DeFiGym Green Agent for Agentbeats.

A benchmarking framework for AI agents on DeFi vulnerability discovery and exploit generation.
Uses DeFiHackLabs (674+ real-world vulnerabilities) for validation.

This agent orchestrates assessments where purple agents attempt to write
Solidity exploit contracts for real-world DeFi vulnerabilities.

Supported vulnerability types:
- reentrancy, flash_loan, oracle_manipulation, price_manipulation
- access_control, logic_error, input_validation, reward_manipulation
- arithmetic, frontrunning, governance, other

Supported networks:
- mainnet, arbitrum, optimism, polygon, bsc, base
- avalanche, fantom, gnosis, blast, mantle, linea, scroll, zksync""",
        url=card_url,
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    return agent_card


def main():
    parser = argparse.ArgumentParser(description="Run the DeFiGym Green Agent.")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind the server"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9009,
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
        default="./data/defihacklabs",
        help="Path to DeFiHackLabs repository"
    )
    args = parser.parse_args()

    # Get DeFiHackLabs repo path from env or args
    defihacklabs_repo = os.environ.get("DEFIHACKLABS_REPO", args.defihacklabs_repo)

    # Create agent and executor
    agent = DeFiGymAgent(defihacklabs_repo=defihacklabs_repo)
    executor = GreenExecutor(agent)

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

    print(f"Starting DeFiGym Green Agent at {card_url}")
    print(f"DeFiHackLabs repo: {defihacklabs_repo}")

    uvicorn.run(server.build(), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
