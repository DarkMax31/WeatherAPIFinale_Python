# Weather forecast retrieval and processing class
# Interacts with OpenWeatherMap API to fetch and process weather data.
import os
import requests
import json
import datetime

class WeatherForecast:      # Weather forecast retrieval and processing class 
    def __init__(self, location, country_code, api_key):
        self.location = location
        self.country_code = country_code
        self.api_key = api_key

    def get_forecast(self):     # Fetch weather forecast data from OpenWeatherMap API with metrics units
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={self.location},{self.country_code}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url, verify=False) # Change verify to your certificate path if needed
            response.raise_for_status()
            self.forecast_data = response.json()
        except requests.exceptions.RequestException as e:
            raise
        
        # Verify response for errors
        if "cod" in self.forecast_data and self.forecast_data["cod"] != "200":
            error_message = self.forecast_data.get("message", "Erreur inconnue")
            raise Exception(f"Erreur API: {self.forecast_data['cod']} - {error_message}")
        
        if "list" not in self.forecast_data:
            raise Exception("La réponse API ne contient pas les données attendues. Vérifiez votre clé API.")

    def process_forecast(self):     # Process the fetched forecast data to extract relevant information
        forecast_by_day = {}  # Dictionary to hold daily aggregated data
        total_rain_period_mm = 0
        total_snow_period_mm = 0
        max_humidity_period = 0
        min_temp_period = float('inf')
        max_temp_period = float('-inf')
        previous_temp = None

        for forecast in self.forecast_data["list"]:    # Iterate through each forecast entry
            date_local = datetime.datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S")
            date_str = date_local.strftime("%Y-%m-%d")  # Extract just the date
            
            rain_cumul_mm = 0
            snow_cumul_mm = 0
            major_transitions_count = 0
            temp = forecast["main"]["temp"]

            # Check if temperature changed by ±3°C or more AND weather category changed
            if previous_temp is not None:
                temp_difference = abs(temp - previous_temp)
                current_weather = forecast["weather"][0]["main"]
                
                if temp_difference >= 3:
                    major_transitions_count = 1
            
            previous_temp = temp

            if "rain" in forecast["weather"][0]["description"]:
                rain_cumul_mm += forecast["rain"]["3h"]
            if "snow" in forecast["weather"][0]["description"]:
                snow_cumul_mm += forecast["snow"]["3h"]

            if forecast["main"]["humidity"] > max_humidity_period:
                max_humidity_period = forecast["main"]["humidity"]
            
            if temp < min_temp_period:
                min_temp_period = temp
            if temp > max_temp_period:
                max_temp_period = temp

            # Add or accumulate data for this day
            if date_str not in forecast_by_day:
                forecast_by_day[date_str] = {
                    "rain_cumul_mm": 0,
                    "snow_cumul_mm": 0,
                    "major_transitions_count": 0
                }
            
            forecast_by_day[date_str]["rain_cumul_mm"] += rain_cumul_mm
            forecast_by_day[date_str]["snow_cumul_mm"] += snow_cumul_mm
            forecast_by_day[date_str]["major_transitions_count"] += major_transitions_count

            total_rain_period_mm += rain_cumul_mm
            total_snow_period_mm += snow_cumul_mm

        # Convert the daily data into a list of dictionaries
        forecast_details = []
        for date_str, data in sorted(forecast_by_day.items()):
            forecast_details.append({
                "date_local": date_str,
                "rain_cumul_mm": round(data["rain_cumul_mm"], 2),
                "snow_cumul_mm": round(data["snow_cumul_mm"], 2),
                "major_transitions_count": data["major_transitions_count"]
            })

        return {
            "forecast_location_name": self.forecast_data["city"]["name"],
            "country_code": self.forecast_data["city"]["country"],
            "total_rain_period_mm": round(total_rain_period_mm, 2),
            "total_snow_period_mm": round(total_snow_period_mm, 2),
            "max_humidity_period": max_humidity_period,
            "forecast_details": forecast_details
        }

    def save_forecast(self, filename):      # Save the processed forecast data to a JSON file
        forecast = self.process_forecast()
        os.makedirs("json", exist_ok=True)
        filepath = f"json/{filename}"
        with open(filepath, "w") as f:
            json.dump(forecast, f, indent=4)
        print(f"Prévisions sauvegardées dans {filepath}")
