import time
from zapv2 import ZAPv2

# Configuration
zap_api_key = 'your_zap_api_key'  # Set your ZAP API key
zap_base_url = 'http://localhost:8080'  # Update this if ZAP is running on a different host or port
api_base_url = 'https://develop.furaha.financial/auth/'

# Initialize ZAP
zap = ZAPv2(apikey=zap_api_key, proxies={'http': zap_base_url, 'https': zap_base_url})

# Function to start a new session
def start_session(session_name):
    zap.core.new_session(name=session_name, overwrite=True)
    print(f'Started new session: {session_name}')

# Function to handle rule loading
def load_scan_rule(rule_name):
    try:
        zap.pscan.load_scan_rule(rule_name)
        print(f'Loaded scan rule: {rule_name}')
    except Exception as e:
        print(f'Error loading scan rule {rule_name}: {str(e)}')

# Function to perform active scan
def perform_active_scan(target_url):
    print(f'Scanning target: {target_url}')
    scan_id = zap.ascan.scan(target=target_url)
    while int(zap.ascan.status(scan_id)) < 100:
        print(f'Scan progress: {zap.ascan.status(scan_id)}%')
        time.sleep(5)
    print(f'Scan completed for target: {target_url}')

# Start a new session
start_session('Furaha Financial API Scan')

# Load custom scan rules
custom_scan_rules = [
    'org.zaproxy.zap.extension.pscanrules.AntiClickjackingScanRule',
    # Add other rules as needed
]

for rule in custom_scan_rules:
    load_scan_rule(rule)

# Define your API endpoints
api_endpoints = [
    'https://develop.furaha.financial/auth/v1/auth/login',
    'https://develop.furaha.financial/auth/v1/auth/signup',
    'https://develop.furaha.financial/auth/v1/auth/verify-login-otp'
]

# Perform scan for each endpoint
for endpoint in api_endpoints:
    perform_active_scan(endpoint)

# Get the scan results
print('Hosts: ', zap.core.hosts())
print('Alerts: ', zap.core.alerts())
