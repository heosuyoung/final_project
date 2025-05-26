"""
Simple test script to verify CORS settings in the Django application
"""
import requests
import json

def test_cors():
    """
    Test if CORS headers are correctly set for API requests
    """
    print("Testing CORS settings for the AI advisor API...")
    
    # Test the advisor endpoint with OPTIONS request (preflight)
    test_url = "http://localhost:8000/advisor/chat/"
    headers = {
        'Origin': 'http://localhost:5173',  # frontend development server
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type',
    }
    
    try:
        # Send an OPTIONS request
        response = requests.options(test_url, headers=headers, timeout=5)
        print(f"Status code: {response.status_code}")
        print("Response headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
            
        if 'Access-Control-Allow-Origin' in response.headers:
            print("\n✅ CORS is properly configured!")
        else:
            print("\n❌ CORS headers not found! This could cause frontend API calls to fail.")
            print("   Make sure django-cors-headers is installed and configured correctly.")
    
        # Now test actual API request
        print("\nTesting actual POST request...")
        
        test_payload = {
            "message": "API 테스트입니다",
            "context": [],
            "financial_data": None
        }
        
        post_headers = {
            'Origin': 'http://localhost:5173',
            'Content-Type': 'application/json',
        }
        
        post_response = requests.post(
            test_url, 
            headers=post_headers, 
            data=json.dumps(test_payload),
            timeout=10
        )
        
        print(f"POST Status code: {post_response.status_code}")
        if post_response.status_code == 200:
            print("✅ POST request successful")
            print(f"Response: {post_response.json()}")
        else:
            print(f"❌ POST request failed: {post_response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing CORS: {e}")
        print("   Make sure the backend server is running.")
    
if __name__ == "__main__":
    test_cors()
