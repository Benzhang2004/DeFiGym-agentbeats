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

# Update foundry.toml to use environment variables for RPC endpoints
# These will be populated at runtime from GitHub secrets
# Note: Using flexible patterns to handle variable whitespace in the original file
RUN sed -i -E 's|^mainnet[[:space:]]*=.*|mainnet = "${ETH_RPC_URL}"|' data/defihacklabs/foundry.toml && \
    sed -i -E 's|^arbitrum[[:space:]]*=.*|arbitrum = "${ARBITRUM_RPC_URL}"|' data/defihacklabs/foundry.toml && \
    sed -i -E 's|^optimism[[:space:]]*=.*|optimism = "${OPTIMISM_RPC_URL}"|' data/defihacklabs/foundry.toml && \
    sed -i -E 's|^polygon[[:space:]]*=.*|polygon = "${POLYGON_RPC_URL}"|' data/defihacklabs/foundry.toml && \
    sed -i -E 's|^bsc[[:space:]]*=.*|bsc = "${BSC_RPC_URL}"|' data/defihacklabs/foundry.toml && \
    sed -i -E 's|^base[[:space:]]*=.*|base = "${BASE_RPC_URL}"|' data/defihacklabs/foundry.toml && \
    sed -i -E 's|^avalanche[[:space:]]*=.*|avalanche = "${AVALANCHE_RPC_URL}"|' data/defihacklabs/foundry.toml && \
    sed -i -E 's|^fantom[[:space:]]*=.*|fantom = "${FANTOM_RPC_URL}"|' data/defihacklabs/foundry.toml

# Environment variables
ENV DEFIHACKLABS_REPO="/home/agent/data/defihacklabs"

# Entrypoint
ENTRYPOINT ["uv", "run", "src/server.py"]
CMD ["--host", "0.0.0.0"]

# Expose default port
EXPOSE 9009
