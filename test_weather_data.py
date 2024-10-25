import unittest
from weather_data import fetch_weather_data, update_daily_summary
from alert_system import check_alerts

class TestWeatherMonitoringSystem(unittest.TestCase):

    def test_data_retrieval(self):
        # Simulate API call and check if data is correctly retrieved
        data = fetch_weather_data("Delhi")
        self.assertIsNotNone(data)
        self.assertIn('temp', data)

    def test_temperature_conversion(self):
        # Test temperature conversion functions
        temp_celsius = kelvin_to_celsius(300)
        self.assertAlmostEqual(temp_celsius, 26.85, places=2)

    def test_alert_trigger(self):
        # Simulate alert threshold breach
        weather_data = {'city': 'Delhi', 'temp': 36}
        check_alerts(weather_data)
        self.assertEqual(alert_count['Delhi'], 1)

if __name__ == "__main__":
    unittest.main()
