"""
Tests d'erreur pour la classe WeatherForecast
Teste les scénarios d'erreur et d'exception
"""
import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from loguru import logger
from tests.logging_setup import configure_for

sys.path.insert(0, str(Path(__file__).parent.parent))

from classes.WeatherForecast import WeatherForecast
from classes.APIKey import APIKey


class TestWeatherForecastErrors(unittest.TestCase):
    """Tests pour les erreurs de WeatherForecast"""

    def setUp(self):
        """Initialisation avant chaque test"""
        configure_for(Path(__file__).stem)
        logger.info("🧪 Démarrage test erreur WeatherForecast")
        self.api_key = APIKey.key

    def tearDown(self):
        """Nettoyage après chaque test"""
        logger.info("✅ Fin test erreur WeatherForecast\n")

    def test_get_forecast_invalid_city(self):
        """Test get_forecast avec une ville inexistante"""
        logger.info("Test : get_forecast() - Ville inexistante")
        forecast = WeatherForecast("CityDoesNotExistXYZ123456", "XX", self.api_key)
        
        with self.assertRaises(Exception) as context:
            forecast.get_forecast()
        
        logger.error(f"❌ Exception levée (attendue) : {context.exception}")
        self.assertIn("Erreur API", str(context.exception))
        logger.success("✓ Exception correctement levée pour ville invalide")

    def test_get_forecast_invalid_api_key(self):
        """Test get_forecast avec une clé API invalide"""
        logger.info("Test : get_forecast() - Clé API invalide")
        forecast = WeatherForecast("Paris", "FR", "invalid_api_key_12345")
        
        with self.assertRaises(Exception) as context:
            forecast.get_forecast()
        
        logger.error(f"❌ Exception levée (attendue) : {context.exception}")
        self.assertIn("Erreur API", str(context.exception))
        logger.success("✓ Exception correctement levée pour clé API invalide")

    @patch('requests.get')
    def test_get_forecast_network_error(self, mock_get):
        """Test get_forecast avec erreur réseau"""
        logger.info("Test : get_forecast() - Erreur réseau")
        mock_get.side_effect = Exception("Network error")
        
        forecast = WeatherForecast("Paris", "FR", self.api_key)
        
        with self.assertRaises(Exception):
            forecast.get_forecast()
        
        logger.error("❌ Exception réseau levée (attendue)")
        logger.success("✓ Exception réseau correctement propagée")

    def test_process_forecast_without_data(self):
        """Test process_forecast sans données (forecast_data = None)"""
        logger.info("Test : process_forecast() - Sans données")
        forecast = WeatherForecast("Paris", "FR", self.api_key)
        
        with self.assertRaises(Exception):
            forecast.process_forecast()
        
        logger.error("❌ Exception levée pour absence de données")
        logger.success("✓ Exception correctement levée")

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_save_forecast_permission_error(self, mock_open):
        """Test save_forecast avec erreur de permission"""
        logger.info("Test : save_forecast() - Erreur permission fichier")
        forecast = WeatherForecast("Paris", "FR", self.api_key)
        
        # Créer des données simulées
        forecast.forecast_data = {
            "city": {"name": "Paris", "country": "FR"},
            "list": []
        }
        
        with self.assertRaises(Exception):
            forecast.save_forecast("test.json")
        
        logger.error("❌ Exception permission levée (attendue)")
        logger.success("✓ Exception permission correctement propagée")

    def test_get_forecast_empty_response(self):
        """Test get_forecast avec une réponse vide"""
        logger.info("Test : get_forecast() - Réponse vide")
        
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {}
            mock_get.return_value = mock_response
            
            forecast = WeatherForecast("Paris", "FR", self.api_key)
            
            with self.assertRaises(Exception):
                forecast.get_forecast()
            
            logger.error("❌ Exception levée pour réponse vide")
            logger.success("✓ Exception correctement levée")

    def test_process_forecast_invalid_json_structure(self):
        """Test process_forecast avec structure JSON invalide"""
        logger.info("Test : process_forecast() - Structure JSON invalide")
        
        forecast = WeatherForecast("Paris", "FR", self.api_key)
        forecast.forecast_data = {
            "city": {"name": "Paris", "country": "FR"},
            "list": [
                {
                    "dt_txt": "2025-11-17 00:00:00",
                    # Données manquantes : weather, main
                }
            ]
        }
        
        with self.assertRaises(Exception):
            forecast.process_forecast()
        
        logger.error("❌ Exception levée pour structure invalide")
        logger.success("✓ Exception correctement levée")

    def test_save_forecast_invalid_directory(self):
        """Test save_forecast avec répertoire invalide"""
        logger.info("Test : save_forecast() - Répertoire invalide")
        
        forecast = WeatherForecast("Paris", "FR", self.api_key)
        forecast.forecast_data = {
            "city": {"name": "Paris", "country": "FR"},
            "list": []
        }
        
        with patch('builtins.open', side_effect=FileNotFoundError("No such directory")):
            with self.assertRaises(Exception):
                forecast.save_forecast("test.json")
        
        logger.error("❌ Exception FileNotFoundError levée (attendue)")
        logger.success("✓ Exception correctement levée")


if __name__ == "__main__":
    unittest.main()
