import subprocess
import sys
import time
import os

# Updated Service List with 3 Transaction Nodes
services = [
    {"path": "api_gateway/app.py", "port": 5000, "name": "API Gateway"},
    {"path": "frontend/app.py", "port": 5001, "name": "Frontend"},
    {"path": "core_service/app.py", "port": 5002, "name": "Core Service"},
    # 3 Instaces of Transaction Service for Load Balancing
    {"path": "transaction_service/app.py", "port": 5003, "name": "Trans Service (Node A)", "args": ["5003"]},
    {"path": "transaction_service/app.py", "port": 5004, "name": "Trans Service (Node B)", "args": ["5004"]},
    {"path": "transaction_service/app.py", "port": 5005, "name": "Trans Service (Node C)", "args": ["5005"]},
]

processes = []

def run_service(service):
    print(f"Starting {service['name']} on port {service['port']}...")
    
    file_path = os.path.abspath(service['path'])
    
    # Construct command with optional args
    cmd = [sys.executable, file_path]
    if "args" in service:
        cmd.extend(service["args"])

    try:
        if sys.platform == "win32":
            # open in new windows
            p = subprocess.Popen(cmd, cwd=os.path.dirname(file_path), creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            p = subprocess.Popen(cmd, cwd=os.path.dirname(file_path))
        return p
    except Exception as e:
        print(f"Error starting {service['name']}: {e}")
        return None

try:
    print("Starting all services (Frontend, Gateway, Core, 3x Transaction)...")
    for service in services:
        p = run_service(service)
        if p:
            processes.append(p)
        time.sleep(1)

    print("\nAll services started!")
    print("API Gateway LB running at http://localhost:5000")
    print("Frontend running at http://localhost:5001")
    print("Transaction Nodes: 5003, 5004, 5005")
    print("Press Ctrl+C to stop all services.")

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping all services...")
    for p in processes:
        p.terminate()
    print("Done.")
