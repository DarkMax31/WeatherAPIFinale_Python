# Main entry point for the weather application
# Initializes and runs the WeatherApp.
from classes.WeatherApp import WeatherApp 

if __name__ == "__main__":
    app = WeatherApp()
    app.run()