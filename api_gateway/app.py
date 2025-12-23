from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Core Services (Single Instance) - Use environment variable for production
CORE_URL = os.environ.get('CORE_SERVICE_URL', 'http://localhost:5002')
SERVICES = {
    'auth': f'{CORE_URL}/auth',
    'admin': f'{CORE_URL}/admin',
    'hotel': f'{CORE_URL}/hotel',
}

# Transaction Services (Round Robin Load Balancing)
# For Render: Set TRANS_SERVICE_URLS as comma-separated URLs
trans_urls_str = os.environ.get('TRANS_SERVICE_URLS', 'http://localhost:5003,http://localhost:5004,http://localhost:5005')
TRANS_NODES = [url.strip() for url in trans_urls_str.split(',')]

# Pointer for Round Robin
trans_idx = 0

def get_next_trans_node():
    global trans_idx
    node = TRANS_NODES[trans_idx]
    # Update pointer: (0 -> 1 -> 2 -> 0 ...)
    trans_idx = (trans_idx + 1) % len(TRANS_NODES)
    return node

@app.route('/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(service, path):
    
    # 1. Determine Target URL
    if service in ['order', 'payment', 'notification']:
        # Apply Load Balancer Logic
        base_url = get_next_trans_node()
        url = f"{base_url}/{service}/{path}"
        print(f"LB: Routing '{service}' request to {base_url} (Index: {(trans_idx - 1) % len(TRANS_NODES)})")
        
    elif service in SERVICES:
        # Static Routing for Core
        url = f"{SERVICES[service]}/{path}"
        
    else:
        return jsonify({"error": "Service not found"}), 404
    
    # 2. Forward Request
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]
        
        # Add a custom header to show which server handled it (debug info)
        headers.append(('X-Handled-By', url))
        
        return resp.content, resp.status_code, headers
    except Exception as e:
        return jsonify({"error": str(e)}), 502

if __name__ == '__main__':
    # Render provides PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    print(f"Gateway running on port {port} with Round Robin LB")
    # host='0.0.0.0' is required for Render to accept external connections
    app.run(host='0.0.0.0', port=port, debug=False)
