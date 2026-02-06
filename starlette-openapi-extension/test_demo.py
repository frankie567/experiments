"""
Quick test of the demo application.

This script starts the demo server in the background, makes some test requests,
and verifies the OpenAPI schema is generated correctly.
"""

import json
import time
import subprocess
import sys
import httpx

def main():
    # Start the demo server in the background
    print("Starting demo server...")
    process = subprocess.Popen(
        [sys.executable, "demo.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(2)
    
    try:
        base_url = "http://localhost:8000"
        
        with httpx.Client() as client:
            # Test 1: Get homepage
            print("\n1. Testing homepage...")
            response = client.get(base_url)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
            # Test 2: Get OpenAPI schema
            print("\n2. Testing OpenAPI schema generation...")
            response = client.get(f"{base_url}/openapi.json")
            print(f"   Status: {response.status_code}")
            schema = response.json()
            print(f"   API Title: {schema['info']['title']}")
            print(f"   API Version: {schema['info']['version']}")
            print(f"   Paths: {list(schema['paths'].keys())}")
            
            # Test 3: List users
            print("\n3. Testing GET /users...")
            response = client.get(f"{base_url}/users?page=1&limit=10")
            print(f"   Status: {response.status_code}")
            print(f"   Users: {response.json()}")
            
            # Test 4: Create user
            print("\n4. Testing POST /users...")
            response = client.post(
                f"{base_url}/users",
                json={"email": "test@example.com", "name": "Test User", "age": 30}
            )
            print(f"   Status: {response.status_code}")
            print(f"   Created user: {response.json()}")
            
            # Test 5: Get specific user
            print("\n5. Testing GET /users/1...")
            response = client.get(f"{base_url}/users/1")
            print(f"   Status: {response.status_code}")
            print(f"   User: {response.json()}")
            
            # Test 6: Get non-existent user
            print("\n6. Testing GET /users/999 (should return 404)...")
            response = client.get(f"{base_url}/users/999")
            print(f"   Status: {response.status_code}")
            print(f"   Error: {response.json()}")
            
            # Test 7: Verify OpenAPI schema structure
            print("\n7. Verifying OpenAPI schema structure...")
            assert "paths" in schema
            assert "/users" in schema["paths"]
            assert "/users/{user_id}" in schema["paths"]
            assert "get" in schema["paths"]["/users"]
            assert "post" in schema["paths"]["/users"]
            assert "components" in schema
            assert "schemas" in schema["components"]
            print("   ✓ Schema structure is correct")
            
            # Test 8: Verify operations have proper metadata
            print("\n8. Verifying operation metadata...")
            create_op = schema["paths"]["/users"]["post"]
            assert create_op["operationId"] == "create_user"
            assert create_op["summary"] == "Create a new user"
            assert "users" in create_op["tags"]
            assert "requestBody" in create_op
            assert "responses" in create_op
            assert "201" in create_op["responses"]
            assert "400" in create_op["responses"]
            print("   ✓ Operation metadata is correct")
            
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Stop the server
        print("\nStopping demo server...")
        process.terminate()
        process.wait(timeout=5)


if __name__ == "__main__":
    main()
