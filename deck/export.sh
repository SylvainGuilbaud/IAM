
#!/bin/bash
# Export the current Kong configuration to a YAML file
# This script is intended to be run in the context of a Kong Gateway environment    
# where the Kong Admin API is accessible.
export KONG_ADMIN_HOST=localhost
export KONG_ADMIN_PORT=8000 

# export in deck directory with the current configuration in a file named by the current date   
export DECK_DIR=$(pwd)

# get the current date in YYYY-MM-DD format
CURRENT_DATE=$(date +%Y-%m-%d)  

# set the output file name
OUTPUT_FILE="${DECK_DIR}/kong-${CURRENT_DATE}.yaml"

# Run the deck command to dump the current Kong configuration

# deck gateway dump --kong-addr http://$KONG_ADMIN_HOST:$KONG_ADMIN_PORT -o $OUTPUT_FILE
deck gateway dump -o $OUTPUT_FILE 