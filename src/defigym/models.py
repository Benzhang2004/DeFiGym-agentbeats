"""
Pydantic data models for DeFiGym Green Agent.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl


class VulnerabilityType(str, Enum):
    """Types of DeFi vulnerabilities."""

    REENTRANCY = "reentrancy"
    FLASH_LOAN = "flash_loan"
    ORACLE_MANIPULATION = "oracle_manipulation"
    PRICE_MANIPULATION = "price_manipulation"
    ACCESS_CONTROL = "access_control"
    LOGIC_ERROR = "logic_error"
    INPUT_VALIDATION = "input_validation"
    REWARD_MANIPULATION = "reward_manipulation"
    ARITHMETIC = "arithmetic"
    FRONTRUNNING = "frontrunning"
    GOVERNANCE = "governance"
    OTHER = "other"


class Network(str, Enum):
    """Blockchain networks."""

    MAINNET = "mainnet"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    POLYGON = "polygon"
    BSC = "bsc"
    BASE = "base"
    AVALANCHE = "avalanche"
    FANTOM = "fantom"
    GNOSIS = "gnosis"
    BLAST = "blast"
    MANTLE = "mantle"
    LINEA = "linea"
    SCROLL = "scroll"
    ZKSYNC = "zksync"


class DifficultyLevel(str, Enum):
    """Difficulty levels for tasks."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Vulnerability(BaseModel):
    """Represents a DeFi vulnerability from DeFiHackLabs."""

    id: str
    date: datetime
    project_name: str
    vulnerability_type: VulnerabilityType
    loss_amount_usd: Optional[float] = None
    network: Network
    block_number: Optional[int] = None
    contract_path: str
    test_command: str
    reference_links: List[str] = Field(default_factory=list)
    attacker_address: Optional[str] = None
    vulnerable_contract: Optional[str] = None
    attack_contract: Optional[str] = None
    transaction_hash: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Task(BaseModel):
    """A benchmark task for agent evaluation."""

    task_id: str
    vulnerability_id: str
    difficulty: DifficultyLevel
    vulnerability_type: VulnerabilityType
    network: Network
    problem_statement: str
    provided_files: Dict[str, str] = Field(default_factory=dict)
    workspace_setup: Dict[str, Any] = Field(default_factory=dict)
    workspace_path: Optional[str] = None
    expected_profit_amount: Optional[float] = None
    expected_profit_token: Optional[str] = None
    validation_criteria: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    tags: List[str] = Field(default_factory=list)


class TestResult(BaseModel):
    """Result from running forge test."""

    passed: bool
    output: str
    gas_used: Optional[int] = None
    events: List[Dict[str, Any]] = Field(default_factory=list)
    balance_changes: Dict[str, float] = Field(default_factory=dict)
    revert_message: Optional[str] = None


class ValidationResult(BaseModel):
    """Result from validating an exploit."""

    success: bool
    test_result: Optional[TestResult] = None
    profit_amount: Optional[float] = None
    profit_token: Optional[str] = None
    profit_matches: bool = False
    compilation_success: bool = False
    test_passed: bool = False
    error: Optional[str] = None


class EvaluationResult(BaseModel):
    """Complete evaluation result for an agent's task execution."""

    task_id: str
    success: bool
    test_passed: bool
    profit_extracted: Optional[float] = None
    profit_matches_expected: bool = False
    execution_time_seconds: float = 0.0
    error_message: Optional[str] = None
    test_output: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)


# Agentbeats-specific models

class EvalRequest(BaseModel):
    """Evaluation request for DeFiGym Green Agent."""

    participants: dict[str, HttpUrl]  # role -> endpoint mapping
    config: dict[str, Any]  # Assessment configuration


class EvalResult(BaseModel):
    """Evaluation result for Agentbeats."""

    winner: str  # Role of winner (or "none")
    detail: dict[str, Any]  # Detailed results
