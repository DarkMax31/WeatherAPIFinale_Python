"""
Tests d'erreur pour la classe WeatherApp
Teste les scénarios d'erreur et d'exception
"""
import unittest
import sys
from pathlib import Path
from unittest.mock import patch
from loguru import logger
from tests.logging_setup import configure_for

sys.path.insert(0, str(Path(__file__).parent.parent))

from classes.WeatherApp import WeatherApp
from classes.APIKey import APIKey
from tests.logging_setup import configure_for



class TestWeatherAppErrors(unittest.TestCase):
    """Tests pour les erreurs de WeatherApp"""

    def setUp(self):
        """Initialisation avant chaque test"""
        configure_for(Path(__file__).stem)
        logger.info("🧪 Démarrage test erreur WeatherApp")
        self.app = WeatherApp()

    def tearDown(self):
        """Nettoyage après chaque test"""
        logger.info("✅ Fin test erreur WeatherApp\n")

    @patch('builtins.input')
    def test_run_with_invalid_city(self, mock_input):
        """Test run() avec une ville invalide"""
        logger.info("Test : run() - Ville invalide")
        mock_input.side_effect = ["InvalidCityXYZ", "XX"]
        
        with self.assertRaises(Exception):
            self.app.run()
        
        logger.error("❌ Exception levée pour ville invalide")
        logger.success("✓ run() correctement échoué avec ville invalide")

    @patch('builtins.input')
    def test_run_empty_city_input(self, mock_input):
        """Test run() avec ville vide"""
        logger.info("Test : run() - Ville vide")
        mock_input.side_effect = ["", "FR"]
        
        with self.assertRaises(Exception):
            self.app.run()
        
        logger.error("❌ Exception levée pour ville vide")
        logger.success("✓ run() échoue avec ville vide")

    @patch('builtins.input')
    def test_run_empty_country_input(self, mock_input):
        """Test run() avec code pays vide"""
        logger.info("Test : run() - Code pays vide")
        mock_input.side_effect = ["Paris", ""]
        
        with self.assertRaises(Exception):
            self.app.run()
        
        logger.error("❌ Exception levée pour code pays vide")
        logger.success("✓ run() échoue avec code pays vide")

    @patch('builtins.input')
    @patch('requests.get', side_effect=Exception("Network error"))
    def test_run_network_error(self, mock_get, mock_input):
        """Test run() avec erreur réseau"""
        logger.info("Test : run() - Erreur réseau")
        mock_input.side_effect = ["Paris", "FR"]
        
        with self.assertRaises(Exception):
            self.app.run()
        
        logger.error("❌ Exception réseau levée (attendue)")
        logger.success("✓ run() correctement échoué en cas d'erreur réseau")

    @patch('builtins.input')
    def test_run_with_invalid_country_code(self, mock_input):
        """Test run() avec code pays invalide"""
        logger.info("Test : run() - Code pays invalide")
        mock_input.side_effect = ["Paris", "INVALID"]
        
        with self.assertRaises(Exception):
            self.app.run()
        
        logger.error("❌ Exception levée pour code pays invalide")
        logger.success("✓ run() échoue avec code pays invalide")

    @patch('builtins.input')
    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_run_file_permission_error(self, mock_open, mock_input):
        """Test run() avec erreur permission fichier"""
        logger.info("Test : run() - Erreur permission fichier")
        mock_input.side_effect = ["Paris", "FR"]
        
        with self.assertRaises(Exception):
            self.app.run()
        
        logger.error("❌ Exception permission levée (attendue)")
        logger.success("✓ run() échoue avec erreur permission")

    def test_api_key_not_configured(self):
        """Test avec clé API non configurée"""
        logger.info("Test : APIKey - Non configurée")
        api_key = APIKey.key
        
        if api_key == "your_api_key_here":
            logger.warning("⚠️ Clé API par défaut détectée")
            logger.error("❌ Clé API doit être configurée")
            self.fail("Clé API doit être configurée pour les tests")
        else:
            logger.success("✓ Clé API correctement configurée")

    @patch('builtins.input')
    @patch('classes.WeatherForecast.WeatherForecast.get_forecast', side_effect=Exception("API error"))
    def test_run_handles_forecast_error(self, mock_forecast, mock_input):
        """Test run() gère les erreurs de get_forecast"""
        logger.info("Test : run() - Gestion erreur get_forecast")
        mock_input.side_effect = ["Paris", "FR"]
        
        with self.assertRaises(Exception):
            self.app.run()
        
        logger.error("❌ Exception de forecast propagée (attendue)")
        logger.success("✓ run() correctement échoué")


if __name__ == "__main__":
    unittest.main()
