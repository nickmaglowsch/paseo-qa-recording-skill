#!/usr/bin/env python3
"""Fallback for agents that don't have the browser_record_* MCP tools (created before the
paseo-browser-recorder plugin was installed). Calls the plugin's loopback MCP endpoint directly.

  record.py start <browserId> [outputPath] [fps]
  record.py stop  <browserId>
"""
import json
import os
import sys
import urllib.request

token = open(os.path.expanduser("~/.cache/paseo-browser-recorder/token")).read().strip()
url = f"http://127.0.0.1:{os.environ.get('PASEO_RECORDER_PORT', '6790')}/mcp/{token}"

action, browser_id = sys.argv[1], sys.argv[2]
if action == "start":
    args = {"browserId": browser_id}
    if len(sys.argv) > 3:
        args["outputPath"] = sys.argv[3]
    if len(sys.argv) > 4:
        args["fps"] = float(sys.argv[4])
    name = "browser_record_start"
elif action == "stop":
    args, name = {"browserId": browser_id}, "browser_record_stop"
else:
    sys.exit(__doc__)

body = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": name, "arguments": args}}
request = urllib.request.Request(url, json.dumps(body).encode(), {"content-type": "application/json"})
result = json.loads(urllib.request.urlopen(request).read())["result"]
print(result["content"][0]["text"])
sys.exit(1 if result.get("isError") else 0)
