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

# Install Foundry
RUN curl -L https://foundry.paradigm.xyz | bash
ENV PATH="/root/.foundry/bin:${PATH}"
RUN foundryup

# Create agent user and setup
RUN adduser --disabled-password --gecos "" agent
USER agent
WORKDIR /home/agent

# Copy project files
COPY --chown=agent:agent pyproject.toml uv.lock README.md ./
COPY --chown=agent:agent src src

# Install dependencies
RUN \
    --mount=type=cache,target=/home/agent/.cache/uv,uid=1000 \
    uv sync --locked

# Copy scenario files
COPY --chown=agent:agent scenarios scenarios

# Create data directory for DeFiHackLabs repo
RUN mkdir -p data

# Environment variables
ENV DEFIHACKLABS_REPO="/home/agent/data/defihacklabs"

# Entrypoint
ENTRYPOINT ["uv", "run", "src/server.py"]
CMD ["--host", "0.0.0.0"]

# Expose default port
EXPOSE 9009
