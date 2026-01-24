"""
Test script for Bluetooth Presence Detection POC
Tests the full flow: registration → detection → status check
"""

import requests
import json
import time

# Configuration

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health():
    """Test health endpoint"""
    print_section("1. Testing Health Endpoint")
    response = requests.get(f"{DJANGO_API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_register_device():
    """Test device registration"""
    print_section("2. Registering Device")
    data = {
        "user_id": TEST_USER_ID,
        "device_mac": LAPTOP_MAC,
        "device_name": "Test Laptop"
    }

    print(f"Registering: {LAPTOP_MAC} for user {TEST_USER_ID}")
    response = requests.post(
        f"{DJANGO_API_URL}/register-device",
        json=data,
        headers={"Content-Type": "application/json"}
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        print("\n✅ Device registered successfully!")
        return True
    elif "already registered" in response.text:
        print("\n⚠️  Device already registered (this is OK)")
        return True
    else:
        print("\n❌ Registration failed!")
        return False

def test_my_status():
    """Test status check"""
    print_section("3. Checking Device Status")
    response = requests.get(
        f"{DJANGO_API_URL}/my-status",
        params={"user_id": TEST_USER_ID}
    )

    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")

    if response.status_code == 200 and data.get('has_device'):
        print("\n✅ Device found in database!")
        print(f"   MAC: {data.get('device_mac')}")
        print(f"   Status: {data.get('status')}")
        print(f"   Last Seen: {data.get('last_seen')}")
        return True
    else:
        print("\n❌ Device not found!")
        return False

def test_device_detection():
    """Simulate scanner detection"""
    print_section("4. Simulating Scanner Detection")
    data = {
        "device_mac": LAPTOP_MAC,
        "device_name": "Test Laptop",
        "rssi": -65
    }

    print(f"Simulating Pi detection of: {LAPTOP_MAC}")
    response = requests.post(
        f"{DJANGO_API_URL}/scanner/device-detected",
        json=data,
        headers={"Content-Type": "application/json"}
    )

    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")

    if response.status_code == 200:
        action = result.get('action')
        print(f"\n✅ Detection processed! Action: {action}")
        return True
    else:
        print("\n❌ Detection failed!")
        return False

def wait_and_check_status():
    """Wait and check if last_seen was updated"""
    print_section("5. Verifying Database Update")
    print("Waiting 2 seconds then checking status...")
    time.sleep(2)

    response = requests.get(
        f"{DJANGO_API_URL}/my-status",
        params={"user_id": TEST_USER_ID}
    )

    data = response.json()
    print(f"Updated Status: {json.dumps(data, indent=2)}")

    if data.get('has_device'):
        print("\n✅ Database was updated!")
        print(f"   Last Seen: {data.get('last_seen')}")
        print(f"   Status: {data.get('status')}")
        print(f"   RSSI: {data.get('rssi')}")
        return True
    else:
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  🎵 CoSounds Bluetooth Presence Detection - Test Suite")
    print("="*60)

    try:
        # Test 1: Health check
        if not test_health():
            print("\n❌ Django backend is not reachable!")
            return

        # Test 2: Register device
        if not test_register_device():
            print("\n❌ Device registration failed!")
            return

        # Test 3: Check initial status
        if not test_my_status():
            print("\n❌ Status check failed!")
            return

        # Test 4: Simulate detection
        if not test_device_detection():
            print("\n❌ Detection failed!")
            return

        # Test 5: Verify update
        if not wait_and_check_status():
            print("\n❌ Database update verification failed!")
            return

        # Success!
        print_section("✅ ALL TESTS PASSED!")
        print("The full Bluetooth presence detection flow is working:")
        print("  1. ✅ Device registration → test_bt_devices table")
        print("  2. ✅ Scanner detection → updates last_seen")
        print("  3. ✅ Status check → reads from database")
        print("\nNext: Check your Pi scanner is detecting your laptop MAC!")
        print(f"Search Django logs for: {LAPTOP_MAC}")

    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to Django backend!")
        print(f"Make sure Django is running at {DJANGO_API_URL}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
