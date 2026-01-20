import requests

BASE_URL = "http://localhost:5000/api/stats"

def test_leaderboard():
    print("Fetching Leaderboard...")
    try:
        res = requests.get(f"{BASE_URL}/leaderboard")
        if res.status_code == 200:
            print("[OK] Leaderboard fetched successfully!")
            data = res.json()
            print(f"Found {len(data)} entries.")
            for i, entry in enumerate(data, 1):
                print(f"{i}. {entry['name']} - Stars: {entry['total_stars']}")
        else:
            print(f"[FAIL] Failed to fetch leaderboard: {res.status_code}")
            print(res.text)
    except Exception as e:
        print(f"[ERR] Error: {e}")

if __name__ == "__main__":
    test_leaderboard()
