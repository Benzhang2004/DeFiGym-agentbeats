# DeFiGym Green Agent Dockerfile
#
# This image includes:
# - Python 3.12 with uv package manager
# - Foundry (forge, cast) for Solidity testing
# - DeFiGym Green Agent code

FROM ghcr.io/astral-sh/uv:python3.12-bookworm

# Install system dependencies
USER root
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create agent user and setup
RUN adduser --disabled-password --gecos "" agent

# Install Foundry as agent user
USER agent
WORKDIR /home/agent
RUN curl -L https://foundry.paradigm.xyz | bash
ENV PATH="/home/agent/.foundry/bin:${PATH}"
RUN /home/agent/.foundry/bin/foundryup

# Copy project files
COPY --chown=agent:agent pyproject.toml uv.lock README.md ./
COPY --chown=agent:agent src src

# Install dependencies (sync will update lock if needed)
RUN \
    --mount=type=cache,target=/home/agent/.cache/uv,uid=1000 \
    uv sync

# Copy scenario files
COPY --chown=agent:agent scenarios scenarios

# Clone DeFiHackLabs repository with submodules
RUN git clone --depth 1 --recurse-submodules --shallow-submodules https://github.com/SunWeb3Sec/DeFiHackLabs.git data/defihacklabs

# Update foundry.toml with Ankr archive RPC endpoints
RUN sed -i 's|mainnet = "https://eth.llamarpc.com"|mainnet = "https://rpc.ankr.com/eth/9aa76d7de0306e4a92cf64b9fdd5f6f6b4aa8b18468610370796ba5d08a02bf7"|g' data/defihacklabs/foundry.toml && \
    sed -i 's|arbitrum = .*|arbitrum = "https://rpc.ankr.com/arbitrum/9aa76d7de0306e4a92cf64b9fdd5f6f6b4aa8b18468610370796ba5d08a02bf7"|g' data/defihacklabs/foundry.toml && \
    sed -i 's|optimism = .*|optimism = "https://rpc.ankr.com/optimism/9aa76d7de0306e4a92cf64b9fdd5f6f6b4aa8b18468610370796ba5d08a02bf7"|g' data/defihacklabs/foundry.toml && \
    sed -i 's|polygon = .*|polygon = "https://rpc.ankr.com/polygon/9aa76d7de0306e4a92cf64b9fdd5f6f6b4aa8b18468610370796ba5d08a02bf7"|g' data/defihacklabs/foundry.toml && \
    sed -i 's|bsc = .*|bsc = "https://rpc.ankr.com/bsc/9aa76d7de0306e4a92cf64b9fdd5f6f6b4aa8b18468610370796ba5d08a02bf7"|g' data/defihacklabs/foundry.toml && \
    sed -i 's|base = .*|base = "https://rpc.ankr.com/base/9aa76d7de0306e4a92cf64b9fdd5f6f6b4aa8b18468610370796ba5d08a02bf7"|g' data/defihacklabs/foundry.toml && \
    sed -i 's|avalanche = .*|avalanche = "https://rpc.ankr.com/avalanche/9aa76d7de0306e4a92cf64b9fdd5f6f6b4aa8b18468610370796ba5d08a02bf7"|g' data/defihacklabs/foundry.toml && \
    sed -i 's|fantom = .*|fantom = "https://rpc.ankr.com/fantom/9aa76d7de0306e4a92cf64b9fdd5f6f6b4aa8b18468610370796ba5d08a02bf7"|g' data/defihacklabs/foundry.toml

# Environment variables
ENV DEFIHACKLABS_REPO="/home/agent/data/defihacklabs"

# Entrypoint
ENTRYPOINT ["uv", "run", "src/server.py"]
CMD ["--host", "0.0.0.0"]

# Expose default port
EXPOSE 9009
