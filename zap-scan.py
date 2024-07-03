import requests
import time

# ZAP API base URL
ZAP_BASE_URL = 'http://localhost:8080'  # Replace with your ZAP instance URL

# API endpoints to scan
API_ENDPOINTS = [
    'https://develop.furaha.financial/auth/v1/auth/signup/',
    'https://develop.furaha.financial/auth/v1/auth/login/'
]

# ZAP API key (optional if enabled in ZAP settings)
ZAP_API_KEY = 'your_zap_api_key_here'

def start_zap_scan(target_url):
    # Start a ZAP scan for the given target URL
    scan_url = f'{ZAP_BASE_URL}/JSON/ascan/action/scan/?url={target_url}&recurse=true'
    headers = {'X-ZAP-API-Key': ZAP_API_KEY} if ZAP_API_KEY else {}

    response = requests.get(scan_url, headers=headers)
    scan_id = response.json()['scan']

    return scan_id

def check_scan_status(scan_id):
    # Check the status of the ZAP scan
    status_url = f'{ZAP_BASE_URL}/JSON/ascan/view/status/?scanId={scan_id}'
    headers = {'X-ZAP-API-Key': ZAP_API_KEY} if ZAP_API_KEY else {}

    while True:
        response = requests.get(status_url, headers=headers)
        scan_status = response.json()['status']
        print(f'Scan ID: {scan_id}, Status: {scan_status}')

        if scan_status == '100':
            print('Scan completed.')
            break
        elif scan_status == '-1':
            print('Scan failed or was aborted.')
            break
        time.sleep(10)

if __name__ == '__main__':
    # Start scanning each API endpoint
    for endpoint in API_ENDPOINTS:
        scan_id = start_zap_scan(endpoint)
        print(f'Started scan for {endpoint}, Scan ID: {scan_id}')
        check_scan_status(scan_id)
