# add a parameter to the script to specify :
# 1. the upstream name, 
# 2. the number of requests to send 
# 3. and the purge the log file before running the test

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate load balancing for the specified upstream in Kong Gateway.
This script checks the load balancing configuration, sends requests to the mock server,
and verifies the distribution of responses across multiple NGINX servers.
"""

import sys
import argparse
import subprocess
import time
import json

# Helper function
def run_cmd(command, capture_output=True):
    try:
        result = subprocess.run(command, shell=True, capture_output=capture_output, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        sys.exit(1)
        
# usage: python3 validateLoadBalancing.py --upstream:sco_upstream --requests:50 --purge:True
# Exampl

# get parameters from command line

import argparse
import sys

def str2bool(value):
    return str(value).lower() in ("1", "true", "yes")

def parse_args(argv=None):
    # Conversion du format --name:value en --name value
    if argv is None:
        argv = sys.argv[1:]
    normed = []
    for arg in argv:
        if arg.startswith('--') and ':' in arg:
            name, val = arg.split(':', 1)
            normed.extend([name, val])
        else:
            normed.append(arg)
    parser = argparse.ArgumentParser(description='Votre script.')

    parser.add_argument('--upstream', type=str, default='sco_upstream',
                        help="Nom de l'upstream (défaut: sco_upstream)")
    parser.add_argument('--requests', type=int, default=50,
                        help="Nombre de requêtes (défaut: 50)")
    parser.add_argument('--purge', action='store_true', default=False,
                        help="Activer la purge (utiliser --purge pour activer, sinon inactif)")

    return parser.parse_args(normed)

args = parse_args()

UPSTREAM_NAME = args.upstream
REQUESTS_COUNT = args.requests
PURGE_LOG = args.purge

KONNECT_PROXY_URL = "http://localhost:8000"

print(f"Testing load balancing for upstream: {UPSTREAM_NAME} with {REQUESTS_COUNT} requests.")

# if purge is True, remove the previous log file in the Docker container iam
if PURGE_LOG:
    print("Purging the previous log file...")
    subprocess.call("docker exec iam truncate -s 0 /tmp/file.log", shell=True)
    run_cmd("docker exec iam truncate -s 0 /tmp/file.log")

print("Testing load balancing for sco_upstream")


# Check dependencies
for tool in ["curl", "jq"]:
    if run_cmd(f"which {tool}") == "":
        print(f"{tool} is not installed. Please install it.")
        sys.exit(1)

# Retrieve Kong upstream configuration
upstreams_json = run_cmd("curl -s http://localhost:8001/upstreams")
upstreams = json.loads(upstreams_json)["data"]

for up in upstreams:
    if up["name"] != UPSTREAM_NAME:
        continue

    config_json = run_cmd(f"curl -s http://localhost:8001/upstreams/{up['name']}")
    config = json.loads(config_json)
    print(f"Load balancing algorithm: {config.get('algorithm', 'N/A')}")



# Activate file log plugin (optional: uncomment if needed)
# run_cmd("docker exec iam curl -i -X POST http://localhost:8001/plugins --data \"name=file-log\" --data \"config.path=/tmp/file.log\" --data \"config.reopen=true\"")

# time.sleep(5)

# add an elapsed time to calculate the time taken to send requests
start_time = time.time()
# Send requests 

print("Sending", REQUESTS_COUNT, "requests to the mock server:", end="")
for _ in range(REQUESTS_COUNT):
    print(".", end="", flush=True)
    run_cmd("curl -s http://localhost:8000/iris/api/atelier/ --user _system:SYS")
print(" done")
elapsed_time = time.time() - start_time
print(f"\nSent {REQUESTS_COUNT} requests in {elapsed_time:.2f} seconds.")


# Read logs and count port usage
log_json = run_cmd("docker exec iam cat /tmp/file.log")
logs = [json.loads(line) for line in log_json.splitlines()]
ports = [port for log in logs if "tries" in log for port in [t.get("port") for t in log["tries"] if "port" in t]]

nginx1 = ports.count(9093)
nginx2 = ports.count(9094)

print("Number of responses received from each NGINX server:")
print(f"NGINX1 (port 9093): {nginx1}")
print(f"NGINX2 (port 9094): {nginx2}")

# Validate load balancing
if nginx1 == 0 and nginx2 == 0:
    print("No responses received from NGINX servers. Please check the Docker container and the log file.")
    sys.exit(1)

smaller = min(nginx1, nginx2)
larger = max(nginx1, nginx2)
total = smaller + larger

if total == 0:
    print("Both NGINX1 and NGINX2 have zero responses. Cannot calculate the difference percentage.")
    sys.exit(1)

diff_pct = round((larger - smaller) / total * 100, 2)
print(f"Difference percentage: {diff_pct}%")

if diff_pct < 10:
    print("✅ Load balancing is working correctly. The difference is less than 10%.")
else:
    print("❌ Load balancing is NOT working correctly.")
    sys.exit(1)

print("Load balancing test completed successfully.")
