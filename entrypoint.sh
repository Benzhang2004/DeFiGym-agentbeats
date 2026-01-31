#!/bin/bash
# Entrypoint script for DeFiGym Green Agent
# Substitutes environment variables into foundry.toml at runtime

FOUNDRY_TOML="${DEFIHACKLABS_REPO}/foundry.toml"

# Debug: print environment variables (redacted)
echo "RPC Environment Variables Status:"
[ -n "$ETH_RPC_URL" ] && echo "  ETH_RPC_URL: set" || echo "  ETH_RPC_URL: not set"
[ -n "$ARBITRUM_RPC_URL" ] && echo "  ARBITRUM_RPC_URL: set" || echo "  ARBITRUM_RPC_URL: not set"
[ -n "$OPTIMISM_RPC_URL" ] && echo "  OPTIMISM_RPC_URL: set" || echo "  OPTIMISM_RPC_URL: not set"
[ -n "$POLYGON_RPC_URL" ] && echo "  POLYGON_RPC_URL: set" || echo "  POLYGON_RPC_URL: not set"
[ -n "$BSC_RPC_URL" ] && echo "  BSC_RPC_URL: set" || echo "  BSC_RPC_URL: not set"
[ -n "$BASE_RPC_URL" ] && echo "  BASE_RPC_URL: set" || echo "  BASE_RPC_URL: not set"
[ -n "$AVALANCHE_RPC_URL" ] && echo "  AVALANCHE_RPC_URL: set" || echo "  AVALANCHE_RPC_URL: not set"
[ -n "$FANTOM_RPC_URL" ] && echo "  FANTOM_RPC_URL: set" || echo "  FANTOM_RPC_URL: not set"

# Update foundry.toml with actual RPC URLs from environment variables
if [ -f "$FOUNDRY_TOML" ]; then
    echo "Updating foundry.toml with RPC endpoints..."

    # Use actual env var values (not placeholders)
    [ -n "$ETH_RPC_URL" ] && sed -i "s|^mainnet.*=.*|mainnet = \"$ETH_RPC_URL\"|" "$FOUNDRY_TOML"
    [ -n "$ARBITRUM_RPC_URL" ] && sed -i "s|^arbitrum.*=.*|arbitrum = \"$ARBITRUM_RPC_URL\"|" "$FOUNDRY_TOML"
    [ -n "$OPTIMISM_RPC_URL" ] && sed -i "s|^optimism.*=.*|optimism = \"$OPTIMISM_RPC_URL\"|" "$FOUNDRY_TOML"
    [ -n "$POLYGON_RPC_URL" ] && sed -i "s|^polygon.*=.*|polygon = \"$POLYGON_RPC_URL\"|" "$FOUNDRY_TOML"
    [ -n "$BSC_RPC_URL" ] && sed -i "s|^bsc.*=.*|bsc = \"$BSC_RPC_URL\"|" "$FOUNDRY_TOML"
    [ -n "$BASE_RPC_URL" ] && sed -i "s|^base.*=.*|base = \"$BASE_RPC_URL\"|" "$FOUNDRY_TOML"
    [ -n "$AVALANCHE_RPC_URL" ] && sed -i "s|^avalanche.*=.*|avalanche = \"$AVALANCHE_RPC_URL\"|" "$FOUNDRY_TOML"
    [ -n "$FANTOM_RPC_URL" ] && sed -i "s|^fantom.*=.*|fantom = \"$FANTOM_RPC_URL\"|" "$FOUNDRY_TOML"

    # Debug: show the rpc_endpoints section
    echo "Updated foundry.toml [rpc_endpoints]:"
    grep -A 20 "\[rpc_endpoints\]" "$FOUNDRY_TOML" | head -15
else
    echo "Warning: foundry.toml not found at $FOUNDRY_TOML"
fi

# Run the main application
exec uv run src/server.py "$@"
