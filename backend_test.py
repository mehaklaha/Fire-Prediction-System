import requests
import sys
import json
import time
from datetime import datetime

class FirePredictionAPITester:
    def __init__(self, base_url="https://inferno-forecast-pro.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=10):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
                except:
                    print(f"   Response: {response.text[:100]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}")

            self.test_results.append({
                "name": name,
                "success": success,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "response_size": len(response.text) if response.text else 0
            })

            return success, response.json() if success and response.text else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.test_results.append({
                "name": name,
                "success": False,
                "error": str(e)
            })
            return False, {}

    def test_root_endpoint(self):
        """Test API root endpoint"""
        return self.run_test("API Root", "GET", "", 200)

    def test_fire_prediction_high_risk(self):
        """Test fire prediction with high risk inputs"""
        high_risk_data = {
            "latitude": 28.6139,
            "longitude": 77.2090,
            "wind_speed": 30.0,
            "vegetation_index": 0.2
        }
        success, response = self.run_test(
            "Fire Prediction (High Risk)",
            "POST",
            "predict",
            200,
            data=high_risk_data
        )
        
        if success:
            print(f"   Risk Level: {response.get('risk_level')}")
            print(f"   Probability: {response.get('probability', 0)*100:.1f}%")
            print(f"   Prediction: {response.get('prediction')}")
        
        return success, response

    def test_fire_prediction_low_risk(self):
        """Test fire prediction with low risk inputs"""
        low_risk_data = {
            "latitude": 20.5,
            "longitude": 78.9,
            "wind_speed": 10.0,
            "vegetation_index": 0.8
        }
        success, response = self.run_test(
            "Fire Prediction (Low Risk)",
            "POST",
            "predict",
            200,
            data=low_risk_data
        )
        
        if success:
            print(f"   Risk Level: {response.get('risk_level')}")
            print(f"   Probability: {response.get('probability', 0)*100:.1f}%")
            print(f"   Prediction: {response.get('prediction')}")
        
        return success, response

    def test_report_fire_incident(self):
        """Test reporting a fire incident"""
        incident_data = {
            "latitude": 19.0760,
            "longitude": 72.8777,
            "description": "Test fire incident for API testing",
            "intensity": "High",
            "reported_by": "API Tester"
        }
        success, response = self.run_test(
            "Report Fire Incident",
            "POST",
            "report-fire",
            200,
            data=incident_data
        )
        
        if success:
            print(f"   Incident ID: {response.get('id')}")
            print(f"   Timestamp: {response.get('timestamp')}")
        
        return success, response

    def test_get_live_fires(self):
        """Test getting live fires"""
        success, response = self.run_test(
            "Get Live Fires",
            "GET",
            "fires/live?limit=10",
            200
        )
        
        if success:
            fires_count = len(response) if isinstance(response, list) else 0
            print(f"   Live fires found: {fires_count}")
            if fires_count > 0:
                print(f"   Sample fire: {response[0].get('satellite', 'N/A')} at {response[0].get('latitude', 0):.3f}, {response[0].get('longitude', 0):.3f}")
        
        return success, response

    def test_get_reported_fires(self):
        """Test getting reported fires"""
        success, response = self.run_test(
            "Get Reported Fires",
            "GET",
            "fires/reported?limit=10",
            200
        )
        
        if success:
            fires_count = len(response) if isinstance(response, list) else 0
            print(f"   Reported fires found: {fires_count}")
            if fires_count > 0:
                print(f"   Sample report: {response[0].get('intensity', 'N/A')} intensity at {response[0].get('latitude', 0):.3f}, {response[0].get('longitude', 0):.3f}")
        
        return success, response

    def test_get_historical_data(self):
        """Test getting historical fire data"""
        success, response = self.run_test(
            "Get Historical Data",
            "GET",
            "fires/historical?days=7",
            200
        )
        
        if success:
            dates = response.get('dates', [])
            counts = response.get('counts', [])
            print(f"   Historical data points: {len(dates)}")
            if dates and counts:
                total_fires = sum(counts)
                print(f"   Total fires in last 7 days: {total_fires}")
        
        return success, response

    def test_invalid_prediction_data(self):
        """Test prediction with invalid data"""
        invalid_data = {
            "latitude": 200,  # Invalid latitude
            "longitude": 77.2090,
            "wind_speed": -10,  # Invalid wind speed
            "vegetation_index": 2.0  # Invalid vegetation index
        }
        success, response = self.run_test(
            "Invalid Prediction Data",
            "POST",
            "predict",
            422,  # Validation error expected
            data=invalid_data
        )
        return success, response

def main():
    print("🔥 Fire Prediction System API Testing")
    print("=" * 50)
    
    # Setup
    tester = FirePredictionAPITester()
    
    # Run all tests
    print("\n📡 Testing API Endpoints...")
    
    # Basic connectivity
    tester.test_root_endpoint()
    
    # Core functionality tests
    tester.test_fire_prediction_high_risk()
    tester.test_fire_prediction_low_risk()
    tester.test_report_fire_incident()
    
    # Data retrieval tests
    tester.test_get_live_fires()
    tester.test_get_reported_fires()
    tester.test_get_historical_data()
    
    # Error handling tests
    tester.test_invalid_prediction_data()
    
    # Print final results
    print(f"\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    # Detailed results
    print(f"\n📋 Detailed Results:")
    for result in tester.test_results:
        status = "✅" if result.get('success') else "❌"
        print(f"{status} {result['name']}")
        if not result.get('success') and 'error' in result:
            print(f"   Error: {result['error']}")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())