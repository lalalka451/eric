import requests
import json
import subprocess
import time
import os

# URL of the configuration file
config_url = "https://imperialb.in/r/zfx0pqjn"

# Path to save the configuration file
config_json_path = r"C:\tem\config_test.json"

# Paths to executables
sing_box_exe_path = r"C:\tem\sing-box.exe"
xray_exe_path = r"C:\tem\xray.exe"

# Download and save the configuration file
response = requests.get(config_url)
with open(config_json_path, 'w') as f:
    f.write(response.text)

# Read the saved configuration file
with open(config_json_path, 'r') as f:
    config_data = json.load(f)

# Check if the configuration contains Hysteria2
has_hysteria2 = any('hysteria2' in outbound.get('type', '').lower() for outbound in config_data.get('outbounds', []))

# Run the appropriate executable
if has_hysteria2:
    print("Starting sing-box...")
    command = [sing_box_exe_path, "run", "-c", config_json_path, "--disable-color"]
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
else:
    print("Starting Xray...")
    command = [xray_exe_path, "run", "-c", config_json_path]
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

# Print the command being executed
print(f"Running command: {' '.join(command)}")

# Handle command log and print output in real-time
try:
    while True:
        output = process.stdout.readline()
        if output:
            print(output.strip())
        if process.poll() is not None:
            break
except KeyboardInterrupt:
    print("Stopping the process...")
    process.terminate()
    process.wait()
    print("Process stopped")