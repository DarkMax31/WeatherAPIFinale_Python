# Weather application class
# Manages user input and orchestrates the weather forecast retrieval and saving process.
import re
from classes.APIKey import APIKey
from classes.WeatherForecast import WeatherForecast
from classes.ForecastTable import ForecastTable

class WeatherApp:      # Weather application class
    def __init__(self):
        self.location = None
        self.country_code = None
        self.api_key = None

    def run(self):      # Main method to run the weather application
        # Read and validate inputs
        self.location = input("Entrez la ville : ").strip()
        self.country_code = input("Entrez le code du pays : ").strip()

        if not self.location:
            raise ValueError("Le nom de la ville est requis")

        # Country code should be two letters (ISO-like). Raise if empty or malformed.
        if not self.country_code or not re.match(r'^[A-Za-z]{2}$', self.country_code):
            raise ValueError("Le code pays doit être composé de 2 lettres")

        self.api_key = APIKey.key

        # Orchestrate forecast retrieval and presentation
        forecast = WeatherForecast(self.location, self.country_code, self.api_key)
        forecast.get_forecast()
        forecast_data = forecast.process_forecast()
        forecast.save_forecast(f"{self.location}_{self.country_code}.json")

        table = ForecastTable(forecast_data["forecast_details"])    # Display the forecast table in console
        table.display_table()