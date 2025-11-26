# Display a table of weather forecast details using PrettyTable
from prettytable import PrettyTable

class ForecastTable:    # Classe for displaying forecast data in a table
    def __init__(self, forecast_details):
        self.forecast_details = forecast_details
        self.table = PrettyTable()

    def create_table(self):   # Create the table structure with headers and title
        self.table.title = "Prévisions météorologiques"
        self.table.field_names = ["Date", "Pluie (mm)", "Neige (mm)", "Transitions majeures"]
        self.table.footer = ["Résumé des prévisions"]

    def add_data(self):  # Add forecast data rows to the table
        for forecast in self.forecast_details:
            self.table.add_row([
                forecast["date_local"], 
                round(forecast["rain_cumul_mm"], 2), 
                round(forecast["snow_cumul_mm"], 2), 
                forecast["major_transitions_count"]
            ])

    def display_table(self):    # Display the table in the console
        self.create_table()
        self.add_data()
        print(self.table)