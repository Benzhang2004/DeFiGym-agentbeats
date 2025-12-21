# DeFiGym Green Agent for Agentbeats

A Green Agent for [Agentbeats](https://docs.agentbeats.dev/) that orchestrates DeFi vulnerability exploitation assessments. This agent benchmarks AI agents on their ability to discover and exploit real-world DeFi vulnerabilities using [DeFiHackLabs](https://github.com/SunWeb3Sec/DeFiHackLabs) (674+ vulnerabilities).

## Overview

DeFiGym is a benchmarking framework for evaluating AI agents on DeFi security tasks. As a Green Agent, it:

1. **Receives assessment requests** with vulnerability specifications
2. **Generates exploit tasks** at configurable difficulty levels (easy/medium/hard)
3. **Sends tasks to purple agents** (exploit developers)
4. **Validates generated exploits** using Foundry
5. **Returns evaluation results** with success/failure and profit metrics

## Project Structure

```
src/
├── server.py           # A2A server and agent card configuration
├── executor.py         # Green executor for A2A request handling
├── agent.py            # DeFiGymAgent implementation
├── messenger.py        # A2A messaging utilities
└── defigym/
    ├── models.py       # Data models (Vulnerability, Task, EvalResult)
    ├── validator.py    # Exploit validation using Foundry
    └── task_generator.py  # Task generation from vulnerabilities
scenarios/
└── defigym/
    └── scenario.toml   # Example assessment scenario
Dockerfile              # Docker configuration with Foundry
pyproject.toml          # Python dependencies
```

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- [Foundry](https://book.getfoundry.sh/) for Solidity testing
- [DeFiHackLabs](https://github.com/SunWeb3Sec/DeFiHackLabs) repository (for validation)

## Getting Started

### 1. Install Dependencies

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

### 2. Setup DeFiHackLabs

Clone the DeFiHackLabs repository for exploit validation:

```bash
mkdir -p data
git clone https://github.com/SunWeb3Sec/DeFiHackLabs.git data/defihacklabs
```

### 3. Install Foundry

```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

### 4. Run the Server

```bash
# Run with default settings
uv run src/server.py

# Or specify options
uv run src/server.py --host 0.0.0.0 --port 9009 --defihacklabs-repo ./data/defihacklabs
```

## Running with Docker

```bash
# Build the image
docker build -t defigym-agent .

# Run the container
docker run -p 9009:9009 -v $(pwd)/data:/home/agent/data defigym-agent
```

## Assessment Request Format

The agent accepts `EvalRequest` JSON with the following structure:

```json
{
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
```

### Required Fields

| Field | Description |
|-------|-------------|
| `participants.exploit_agent` | URL of the purple agent to evaluate |
| `config.project_name` | Name of the vulnerable protocol |
| `config.vulnerability_type` | Type of vulnerability |
| `config.network` | Blockchain network |

### Optional Fields

| Field | Description | Default |
|-------|-------------|---------|
| `config.difficulty` | Task difficulty (easy/medium/hard) | easy |
| `config.loss_amount_usd` | Expected profit in USD | 0.0 |
| `config.block_number` | Block number for forking | None |
| `config.date` | Date of vulnerability | Now |
| `config.contract_path` | Path in DeFiHackLabs repo | Auto-generated |
| `config.test_command` | Forge test command | Auto-generated |
| `config.reference_links` | Links to post-mortems | [] |

## Supported Vulnerability Types

- `reentrancy` - Reentrancy attacks
- `flash_loan` - Flash loan exploits
- `oracle_manipulation` - Oracle manipulation
- `price_manipulation` - AMM price manipulation
- `access_control` - Missing/broken access control
- `logic_error` - Business logic flaws
- `input_validation` - Input validation issues
- `reward_manipulation` - Reward/incentive manipulation
- `arithmetic` - Integer overflow/underflow
- `frontrunning` - Frontrunning attacks
- `governance` - Governance exploits
- `other` - Other vulnerability types

## Supported Networks

- `mainnet` - Ethereum Mainnet
- `arbitrum` - Arbitrum One
- `optimism` - Optimism
- `polygon` - Polygon
- `bsc` - BNB Smart Chain
- `base` - Base
- `avalanche` - Avalanche C-Chain
- `fantom` - Fantom Opera
- `gnosis` - Gnosis Chain
- `blast` - Blast
- `mantle` - Mantle
- `linea` - Linea
- `scroll` - Scroll
- `zksync` - zkSync Era

## Evaluation Result

The agent returns an `EvalResult` with:

```json
{
  "winner": "exploit_agent",
  "detail": {
    "task_id": "sampleprotocol_20240115_abc12345_easy",
    "success": true,
    "test_passed": true,
    "profit_extracted": 150000.0,
    "profit_matches_expected": true,
    "execution_time_seconds": 45.2,
    "error_message": null,
    "timestamp": "2024-01-15T12:00:00"
  }
}
```

## Running Assessments

### Using the Agentbeats CLI

```bash
# Start agents and run assessment
uv run agentbeats-run scenarios/defigym/scenario.toml

# Start agents only (for manual testing)
uv run agentbeats-run scenarios/defigym/scenario.toml --serve-only
```

### Manual Testing

1. Start the DeFiGym Green Agent:
```bash
uv run src/server.py --port 9009
```

2. Start your purple agent (exploit developer) on port 9010

3. Send an assessment request:
```bash
curl -X POST http://127.0.0.1:9009/message \
  -H "Content-Type: application/json" \
  -d @scenarios/defigym/request.json
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEFIHACKLABS_REPO` | Path to DeFiHackLabs repository | `./data/defihacklabs` |

## Publishing

The repository includes a GitHub Actions workflow that automatically builds and publishes a Docker image to GitHub Container Registry:

- **Push to `main`** → publishes `latest` tag
- **Create a git tag** (e.g., `v1.0.0`) → publishes version tags

```
ghcr.io/<your-username>/defigym-agent:latest
ghcr.io/<your-username>/defigym-agent:1.0.0
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Assessment Request                    │
│  (vulnerability specs, purple agent URL, difficulty)     │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  DeFiGym Green Agent                     │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐   │
│  │   Task      │  │   Messenger  │  │   Validator   │   │
│  │  Generator  │  │  (A2A comm)  │  │   (Foundry)   │   │
│  └─────────────┘  └──────────────┘  └───────────────┘   │
└─────────────────────────────────────────────────────────┘
         │                    │                    │
         │                    ▼                    │
         │         ┌─────────────────────┐         │
         │         │   Purple Agent      │         │
         │         │ (Exploit Developer) │         │
         │         └─────────────────────┘         │
         │                    │                    │
         │                    ▼                    │
         │         ┌─────────────────────┐         │
         │         │  Solidity Exploit   │         │
         │         │      Contract       │         │
         │         └─────────────────────┘         │
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│                    DeFiHackLabs Repo                     │
│           (674+ real-world vulnerability tests)          │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Evaluation Result                      │
│     (success/failure, profit metrics, test output)       │
└─────────────────────────────────────────────────────────┘
```

## License

MIT
