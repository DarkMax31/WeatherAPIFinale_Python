"""
Tests unitaires pour la classe WeatherForecast
Teste la récupération et le traitement des données météorologiques
"""
import unittest
import json
import sys
from pathlib import Path
from loguru import logger
from tests.logging_setup import configure_for

sys.path.insert(0, str(Path(__file__).parent.parent))

from classes.WeatherForecast import WeatherForecast
from classes.APIKey import APIKey


class TestWeatherForecast(unittest.TestCase):
    """Tests unitaires pour la classe WeatherForecast"""

    def setUp(self):
        """Initialisation avant chaque test"""
        configure_for(Path(__file__).stem)
        logger.info("🧪 Démarrage test WeatherForecast")
        self.location = "Paris"
        self.country_code = "FR"
        self.api_key = APIKey.key
        self.forecast = WeatherForecast(self.location, self.country_code, self.api_key)

    def tearDown(self):
        """Nettoyage après chaque test"""
        logger.info("✅ Fin test WeatherForecast\n")

    def test_init(self):
        """Test l'initialisation de WeatherForecast"""
        logger.info("Test : __init__")
        self.assertEqual(self.forecast.location, self.location)
        self.assertEqual(self.forecast.country_code, self.country_code)
        self.assertEqual(self.forecast.api_key, self.api_key)
        self.assertIsNone(self.forecast.forecast_data)
        logger.success("✓ __init__ validé")

    def test_get_forecast_success(self):
        """Test la récupération réussie des prévisions"""
        logger.info("Test : get_forecast() - Cas nominal")
        self.forecast.get_forecast()
        
        self.assertIsNotNone(self.forecast.forecast_data)
        self.assertIn("list", self.forecast.forecast_data)
        self.assertIn("city", self.forecast.forecast_data)
        self.assertGreater(len(self.forecast.forecast_data["list"]), 0)
        
        logger.debug(f"Prévisions reçues : {len(self.forecast.forecast_data['list'])} entrées")
        logger.success("✓ get_forecast() réussie")

    def test_get_forecast_invalid_location(self):
        """Test get_forecast avec un lieu invalide"""
        logger.info("Test : get_forecast() - Lieu invalide")
        invalid_forecast = WeatherForecast("InvalidCityXYZ123", "XX", self.api_key)
        
        with self.assertRaises(Exception) as context:
            invalid_forecast.get_forecast()
        
        logger.debug(f"Exception levée : {context.exception}")
        logger.success("✓ get_forecast() avec erreur validé")

    def test_process_forecast_structure(self):
        """Test la structure du traitement des prévisions"""
        logger.info("Test : process_forecast() - Structure")
        self.forecast.get_forecast()
        data = self.forecast.process_forecast()
        
        # Vérifier les clés principales
        required_keys = [
            "forecast_location_name",
            "country_code",
            "total_rain_period_mm",
            "total_snow_period_mm",
            "max_humidity_period",
            "forecast_details"
        ]
        
        for key in required_keys:
            self.assertIn(key, data, f"Clé manquante : {key}")
        
        logger.debug(f"Lieu : {data['forecast_location_name']}")
        logger.debug(f"Pluie totale : {data['total_rain_period_mm']}mm")
        logger.debug(f"Neige totale : {data['total_snow_period_mm']}mm")
        logger.success("✓ process_forecast() structure validée")

    def test_process_forecast_forecast_details(self):
        """Test les détails des prévisions par jour"""
        logger.info("Test : process_forecast() - Détails quotidiens")
        self.forecast.get_forecast()
        data = self.forecast.process_forecast()
        
        self.assertIsInstance(data["forecast_details"], list)
        self.assertGreater(len(data["forecast_details"]), 0)
        
        # Vérifier chaque détail
        for detail in data["forecast_details"]:
            required_keys = ["date_local", "rain_cumul_mm", "snow_cumul_mm", "major_transitions_count"]
            for key in required_keys:
                self.assertIn(key, detail, f"Clé manquante dans détail : {key}")
            
            # Vérifier les types
            self.assertIsInstance(detail["date_local"], str)
            self.assertIsInstance(detail["rain_cumul_mm"], (int, float))
            self.assertIsInstance(detail["snow_cumul_mm"], (int, float))
            self.assertIsInstance(detail["major_transitions_count"], int)
        
        logger.debug(f"Nombre de jours : {len(data['forecast_details'])}")
        logger.success("✓ process_forecast() détails validés")

    def test_process_forecast_values(self):
        """Test les valeurs calculées"""
        logger.info("Test : process_forecast() - Valeurs calculées")
        self.forecast.get_forecast()
        data = self.forecast.process_forecast()
        
        # Vérifier que les totaux sont positifs ou zéro
        self.assertGreaterEqual(data["total_rain_period_mm"], 0)
        self.assertGreaterEqual(data["total_snow_period_mm"], 0)
        self.assertGreaterEqual(data["max_humidity_period"], 0)
        self.assertLessEqual(data["max_humidity_period"], 100)
        
        logger.debug(f"Humidité max : {data['max_humidity_period']}%")
        logger.success("✓ process_forecast() valeurs validées")

    def test_save_forecast(self):
        """Test la sauvegarde en JSON"""
        logger.info("Test : save_forecast()")
        filename = "test_paris_fr.json"
        
        try:
            self.forecast.get_forecast()
            self.forecast.save_forecast(filename)
            
            # Vérifier que le fichier existe
            with open(f"json/{filename}", "r") as f:
                saved_data = json.load(f)
            
            self.assertIsNotNone(saved_data)
            self.assertIn("forecast_details", saved_data)
            
            logger.debug(f"Fichier sauvegardé : {filename}")
            logger.success("✓ save_forecast() validée")
        finally:
            import os
            if os.path.exists(f"json/{filename}"):
                os.remove(f"json/{filename}")
                logger.debug(f"Fichier de test nettoyé")


if __name__ == "__main__":
    unittest.main()
