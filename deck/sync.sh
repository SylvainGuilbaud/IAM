#!/bin/bash
# deck/sync.sh
# This script is used to synchronize the deck with the gateway.
# with the yaml file deck.yaml
# Usage: ./sync.sh
# Ensure the script is run from the correct directory

# Run the sync command
echo "Syncing deck with gateway..."

deck gateway sync kong.yaml