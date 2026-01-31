"""
Baseline Purple Agent - Groundtruth Exploit Provider.

This is a groundtruth baseline agent that reads the actual exploit
from the DeFiHackLabs repository and returns it directly.
Used for testing the evaluation pipeline.
"""

import re
from pathlib import Path
from typing import Optional


class GroundtruthAgent:
    """
    Groundtruth purple agent that returns the actual exploit from DeFiHackLabs.

    This agent parses the contract path from the task description and reads
    the actual exploit file, providing a 100% accurate baseline.
    """

    def __init__(self, defihacklabs_repo: str = "./data/defihacklabs"):
        """
        Initialize the groundtruth agent.

        Args:
            defihacklabs_repo: Path to the DeFiHackLabs repository
        """
        self.defihacklabs_repo = Path(defihacklabs_repo)

    def _extract_contract_path(self, task_description: str) -> Optional[str]:
        """
        Extract the contract path from the task description.

        The task includes a test command like:
        forge test --contracts ./src/test/2024-01/SampleProtocol_exp.sol -vvv

        Args:
            task_description: The full task description from the green agent

        Returns:
            The contract path or None if not found
        """
        # Pattern to match forge test command with contract path
        patterns = [
            r"forge test --contracts\s+(\./)?([^\s]+\.sol)",  # forge test --contracts ./path/file.sol
            r"forge test --match-path\s+(\./)?([^\s]+\.sol)",  # forge test --match-path ./path/file.sol
            r"Contract Path:\s*`?(\./)?([^\s`]+\.sol)`?",  # Contract Path: ./path/file.sol
            r"contract_path[\"']?\s*[:=]\s*[\"']?(\./)?([^\s\"']+\.sol)",  # contract_path: path/file.sol
        ]

        for pattern in patterns:
            match = re.search(pattern, task_description)
            if match:
                # Get the path, handling optional ./ prefix
                path = match.group(2) if match.group(1) else match.group(2)
                return path

        return None

    def _read_exploit_file(self, contract_path: str) -> Optional[str]:
        """
        Read the exploit file from DeFiHackLabs repository.

        Args:
            contract_path: Relative path to the contract (e.g., src/test/2024-01/Example_exp.sol)

        Returns:
            The file contents or None if not found
        """
        full_path = self.defihacklabs_repo / contract_path

        if not full_path.exists():
            # Try without leading src/ if present
            if contract_path.startswith("src/"):
                alt_path = self.defihacklabs_repo / contract_path[4:]
                if alt_path.exists():
                    full_path = alt_path
            # Try with src/ prefix if not present
            else:
                alt_path = self.defihacklabs_repo / "src" / contract_path
                if alt_path.exists():
                    full_path = alt_path

        if full_path.exists():
            return full_path.read_text()

        return None

    async def generate_exploit(self, task_description: str) -> str:
        """
        Return the groundtruth exploit from DeFiHackLabs.

        Args:
            task_description: The task description from the green agent

        Returns:
            The actual exploit code wrapped in a Solidity code block
        """
        # Extract contract path from task
        contract_path = self._extract_contract_path(task_description)
        print(f"[Groundtruth] Extracted contract path: {contract_path}")

        if not contract_path:
            return self._error_response(
                "Could not extract contract path from task description"
            )

        # Read the actual exploit
        exploit_code = self._read_exploit_file(contract_path)
        print(f"[Groundtruth] Exploit code length: {len(exploit_code) if exploit_code else 0}")

        if not exploit_code:
            return self._error_response(
                f"Could not read exploit file: {contract_path}\n"
                f"DeFiHackLabs repo: {self.defihacklabs_repo}"
            )

        # Return the exploit in a code block
        return f"```solidity\n{exploit_code}\n```"

    def _error_response(self, error: str) -> str:
        """Generate an error response with a minimal valid contract."""
        return f"""Error: {error}

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.10;

import "forge-std/Test.sol";

contract GroundtruthError is Test {{
    function setUp() public {{
        // Groundtruth agent failed to load exploit
        // Error: {error}
    }}

    function testExploit() public {{
        revert("Groundtruth agent error - see setUp for details");
    }}
}}
```"""
