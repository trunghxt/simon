import requests
import json

BASE_URL = "http://localhost:5000/api/auth"

def test_auth_flow():
    # 1. Register
    register_data = {
        "name": "Test User 2",
        "email": "test_user_v2@example.com",
        "password": "password123"
    }
    
    print(f"Testing Register with: {register_data['email']}")
    try:
        res = requests.post(f"{BASE_URL}/register", json=register_data)
        if res.status_code == 201:
            print("[OK] Register Success!")
            print(res.json())
        else:
            print(f"[FAIL] Register Failed: {res.status_code}")
            print(res.text)
            # If already exists, try login
            if res.status_code == 400 and "Email already exists" in res.text:
                 print("  -> Email exists, proceeding to Login...")
    except Exception as e:
        print(f"[ERR] Register Error: {e}")
        return

    # 2. Login
    login_data = {
        "email": "test_user_v2@example.com",
        "password": "password123"
    }
    print(f"\nTesting Login with: {login_data['email']}")
    try:
        res = requests.post(f"{BASE_URL}/login", json=login_data)
        if res.status_code == 200:
            print("[OK] Login Success!")
            token = res.json().get("token")
            print(f"  Token received: {token[:20]}...")
            
            # 3. Get Me
            headers = {"Authorization": f"Bearer {token}"}
            me_res = requests.get(f"{BASE_URL}/me", headers=headers)
            if me_res.status_code == 200:
                print("[OK] Get Me Success!")
                print("  User info:", me_res.json())
            else:
                print(f"[FAIL] Get Me Failed: {me_res.status_code}")
        else:
            print(f"[FAIL] Login Failed: {res.status_code}")
            print(res.text)

    except Exception as e:
        print(f"[ERR] Login Error: {e}")

if __name__ == "__main__":
    test_auth_flow()
