import requests
import sys
import time
import subprocess
import signal
from subprocess import Popen
import os

def test_app_availability():
    """Basic test to check if app starts and responds"""
    # Start the Flask app
    process = Popen(['python', 'main.py'])
    time.sleep(8)  # Wait for app to start
    
    try:
        # Test home page
        response = requests.get('http://localhost:5000')
        assert response.status_code == 200
        
        # Test prices endpoint
        response = requests.get('http://localhost:5000/api/prices')
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        
        # Test invalid address
        response = requests.post('http://localhost:5000/check_address', 
                               data={'address': 'invalid'})
        assert response.status_code == 200
        assert 'error' in response.json()
        
        print("All basic tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"Test failed: {str(e)}")
        sys.exit(1)
    finally:
        # Cleanup
        process.send_signal(signal.SIGTERM)
        process.wait()

if __name__ == '__main__':
    test_app_availability()