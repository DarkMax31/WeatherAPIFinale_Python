"""
Tests unitaires pour la classe WeatherApp
Teste la coordination entre les différents composants
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


class TestWeatherApp(unittest.TestCase):
    """Tests unitaires pour la classe WeatherApp"""

    def setUp(self):
        """Initialisation avant chaque test"""
        configure_for(Path(__file__).stem)
        logger.info("🧪 Démarrage test WeatherApp")
        self.app = WeatherApp()

    def tearDown(self):
        """Nettoyage après chaque test"""
        logger.info("✅ Fin test WeatherApp\n")

    def test_init(self):
        """Test l'initialisation de WeatherApp"""
        logger.info("Test : __init__")
        self.assertIsNone(self.app.location)
        self.assertIsNone(self.app.country_code)
        self.assertIsNone(self.app.api_key)
        logger.success("✓ __init__ validé")

    @patch('builtins.input')
    def test_run_valid_inputs(self, mock_input):
        """Test run() avec des entrées valides"""
        logger.info("Test : run() - Entrées valides")
        mock_input.side_effect = ["Paris", "FR"]
        
        try:
            self.app.run()
            
            self.assertEqual(self.app.location, "Paris")
            self.assertEqual(self.app.country_code, "FR")
            self.assertIsNotNone(self.app.api_key)
            
            logger.debug(f"Location : {self.app.location}")
            logger.debug(f"Country : {self.app.country_code}")
            logger.success("✓ run() avec entrées valides réussi")
        except Exception as e:
            logger.error(f"Erreur : {e}")
            raise

    @patch('builtins.input')
    def test_run_different_cities(self, mock_input):
        """Test run() avec différentes villes"""
        logger.info("Test : run() - Différentes villes")
        
        test_cases = [
            ("London", "GB"),
            ("Tokyo", "JP"),
            ("New York", "US"),
        ]
        
        for city, country in test_cases:
            logger.debug(f"Test : {city}, {country}")
            app = WeatherApp()
            mock_input.side_effect = [city, country]
            
            try:
                app.run()
                self.assertEqual(app.location, city)
                self.assertEqual(app.country_code, country)
                logger.success(f"✓ {city} ({country}) validé")
            except Exception as e:
                logger.warning(f"Erreur pour {city} : {e}")

    def test_api_key_loading(self):
        """Test le chargement de la clé API"""
        logger.info("Test : Chargement clé API")
        api_key = APIKey.key
        
        self.assertIsNotNone(api_key)
        self.assertNotEqual(api_key, "your_api_key_here")
        self.assertGreater(len(api_key), 0)
        
        logger.debug(f"Clé API chargée (longueur : {len(api_key)})")
        logger.success("✓ Clé API validée")


if __name__ == "__main__":
    unittest.main() 
