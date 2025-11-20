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
from datetime import datetime

LOG_FILE = "load_balancer_test.log"

# Global flag to enable/disable logging
ENABLE_LOG = False

# ---------- Logging ----------
def log_to_file(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    if ENABLE_LOG:
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} {message}\n")
    print(message)

# ---------- Helper ----------
def run_cmd(command, capture_output=True):
    try:
        result = subprocess.run(command, shell=True, capture_output=capture_output, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log_to_file(f"❌ Command failed: {e}")
        sys.exit(1)

# ---------- Argument Parsing ----------
def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    normed = []
    for arg in argv:
        if arg.startswith('--') and ':' in arg:
            name, val = arg.split(':', 1)
            normed.extend([name, val])
        else:
            normed.append(arg)

    parser = argparse.ArgumentParser(description='Kong Gateway load balancer test.')
    parser.add_argument('--upstream', type=str, default='sco_upstream', help="Upstream name (default: sco_upstream)")
    parser.add_argument('--requests', type=int, default=50, help="Number of requests to send (default: 50)")
    parser.add_argument('--purge', action='store_true', help="Purge log files before running")
    parser.add_argument('--log', action='store_true', help="Enable logging to external file")
    return parser.parse_args(normed)

args = parse_args()

# Assign CLI parameters
UPSTREAM_NAME = args.upstream
REQUESTS_COUNT = args.requests
PURGE_LOG = args.purge
ENABLE_LOG = args.log

# ---------- Purge Local Log File ----------
if PURGE_LOG and ENABLE_LOG:
    with open(LOG_FILE, "w") as f:
        f.write("")  # truncate the local log file
    log_to_file("🔄 Purged local log file.")
    log_to_file("Purging Docker container log...")
    subprocess.call("docker exec iam truncate -s 0 /tmp/file.log", shell=True)
elif PURGE_LOG:
    subprocess.call("docker exec iam truncate -s 0 /tmp/file.log", shell=True)
    print("Purged container log file (local logging disabled).")

log_to_file(f"🚀 Testing load balancing for upstream: {UPSTREAM_NAME} with {REQUESTS_COUNT} requests.")

# ---------- Check Dependencies ----------
for tool in ["curl", "jq"]:
    if run_cmd(f"which {tool}") == "":
        log_to_file(f"❌ {tool} is not installed. Please install it.")
        sys.exit(1)

# ---------- Kong Upstream Info ----------
upstreams_json = run_cmd("curl -s http://localhost:8001/upstreams")
upstreams = json.loads(upstreams_json)["data"]

up_found = False
for up in upstreams:
    if up["name"] == UPSTREAM_NAME:
        up_found = True
        config_json = run_cmd(f"curl -s http://localhost:8001/upstreams/{up['name']}")
        config = json.loads(config_json)
        log_to_file(f"🔧 Load balancing algorithm: {config.get('algorithm', 'N/A')}")
        break

if not up_found:
    log_to_file(f"❌ Upstream '{UPSTREAM_NAME}' not found.")
    sys.exit(1)

# ---------- Send Requests ----------
start_time = time.time()
log_to_file("📡 Sending requests to mock server...")
for _ in range(REQUESTS_COUNT):
    print(".", end="", flush=True)
    run_cmd("curl -s http://localhost:8000/iris/api/atelier/ --user _system:SYS")
elapsed_time = time.time() - start_time
log_to_file(f"✅ Sent {REQUESTS_COUNT} requests in {elapsed_time:.2f} seconds.")

# ---------- Analyze Logs ----------
log_json = run_cmd("docker exec iam cat /tmp/file.log")
logs = [json.loads(line) for line in log_json.splitlines()]
ports = [port for log in logs if "tries" in log for port in [t.get("port") for t in log["tries"] if "port" in t]]

nginx1 = ports.count(9080)
nginx2 = ports.count(9082)

log_to_file("📊 Number of responses received from each NGINX server:")
log_to_file(f"  🔹 NGINX1 (port 9093): {nginx1}")
log_to_file(f"  🔹 NGINX2 (port 9094): {nginx2}")

# ---------- Load Balancing Validation ----------
if nginx1 == 0 and nginx2 == 0:
    log_to_file("❌ No responses received from NGINX servers. Please check the Docker container and the log file.")
    sys.exit(1)

smaller = min(nginx1, nginx2)
larger = max(nginx1, nginx2)
total = smaller + larger

if total == 0:
    log_to_file("❌ No traffic distributed. Cannot calculate difference.")
    sys.exit(1)

diff_pct = round((larger - smaller) / total * 100, 2)
log_to_file(f"📈 Difference percentage: {diff_pct}%")

if diff_pct < 10:
    log_to_file("✅ Load balancing is working correctly. Difference is under 10%.")
else:
    log_to_file("❌ Load balancing is NOT working correctly.")
    sys.exit(1)

log_to_file("🎉 Load balancing test completed successfully.")
