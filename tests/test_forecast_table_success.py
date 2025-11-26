"""
Tests unitaires pour la classe ForecastTable
Teste l'affichage des prévisions dans un tableau
"""
import unittest     # Tests unitaires
import sys  # Accès aux fonctionnalités système
import io # Pour capturer la sortie standard
from pathlib import Path    # Gestion des chemins de fichiers
from unittest.mock import patch # Mocking pour les tests
from loguru import logger
from tests.logging_setup import configure_for


sys.path.insert(0, str(Path(__file__).parent.parent))

from classes.ForecastTable import ForecastTable


class TestForecastTable(unittest.TestCase):
    """Tests unitaires pour la classe ForecastTable"""

    def setUp(self): 
        """Initialisation avant chaque test"""
        configure_for(Path(__file__).stem)
        logger.info("🧪 Démarrage test ForecastTable")
        
        # Test data for forecast details
        self.forecast_details = [
            {
                "date_local": "2025-11-17",
                "rain_cumul_mm": 0.69,
                "snow_cumul_mm": 0,
                "major_transitions_count": 1
            },
            {
                "date_local": "2025-11-18",
                "rain_cumul_mm": 0,
                "snow_cumul_mm": 0,
                "major_transitions_count": 0
            },
            {
                "date_local": "2025-11-19",
                "rain_cumul_mm": 10.39,
                "snow_cumul_mm": 0,
                "major_transitions_count": 0
            }
        ]
        
        self.table = ForecastTable(self.forecast_details)

    def tearDown(self):
        """Nettoyage après chaque test"""
        logger.info("✅ Fin test ForecastTable\n")

    def test_init(self):
        """Test l'initialisation de ForecastTable"""
        logger.info("Test : __init__")
        self.assertEqual(len(self.table.forecast_details), 3)
        self.assertIsNotNone(self.table.table)
        logger.debug(f"Nombre de détails : {len(self.table.forecast_details)}")
        logger.success("✓ __init__ validé")

    def test_create_table_structure(self):
        """Test la création de la structure du tableau"""
        logger.info("Test : create_table()")
        self.table.create_table()
        
        # Vérifier les propriétés du tableau
        self.assertEqual(self.table.table.title, "Prévisions météorologiques")
        self.assertIsNotNone(self.table.table.field_names)
        
        expected_fields = ["Date", "Pluie (mm)", "Neige (mm)", "Transitions majeures"]
        self.assertEqual(self.table.table.field_names, expected_fields)
        
        logger.debug(f"Titre : {self.table.table.title}")
        logger.debug(f"Colonnes : {self.table.table.field_names}")
        logger.success("✓ create_table() validé")

    def test_add_data(self):
        """Test l'ajout des données dans le tableau"""
        logger.info("Test : add_data()")
        self.table.create_table()
        self.table.add_data()
        
        # Vérifier que les données ont été ajoutées
        self.assertGreater(len(self.table.table._rows), 0)
        logger.debug(f"Nombre de lignes ajoutées : {len(self.table.table._rows)}")
        logger.success("✓ add_data() validé")

    def test_display_table_output(self):
        """Test l'affichage du tableau"""
        logger.info("Test : display_table()")
        
        # Capturer la sortie
        captured_output = io.StringIO()
        
        with patch('sys.stdout', captured_output):
            self.table.display_table()
        
        output = captured_output.getvalue()
        
        # Vérifier que le tableau a été affiché
        self.assertGreater(len(output), 0)
        self.assertIn("Prévisions météorologiques", output)
        self.assertIn("Date", output)
        self.assertIn("Pluie", output)
        
        logger.debug(f"Sortie générée (longueur : {len(output)} caractères)")
        logger.success("✓ display_table() validé")

    def test_display_table_contains_data(self):
        """Test que le tableau affiche les bonnes données"""
        logger.info("Test : display_table() - Vérification données")
        
        captured_output = io.StringIO()
        
        with patch('sys.stdout', captured_output):
            self.table.display_table()
        
        output = captured_output.getvalue()
        
        # Vérifier les dates
        self.assertIn("2025-11-17", output)
        self.assertIn("2025-11-18", output)
        self.assertIn("2025-11-19", output)
        
        logger.debug("Toutes les dates sont présentes")
        logger.success("✓ display_table() données validées")

    def test_empty_forecast_details(self):
        """Test avec une liste vide"""
        logger.info("Test : Gestion liste vide")
        empty_table = ForecastTable([])
        
        self.assertEqual(len(empty_table.forecast_details), 0)
        
        # Le tableau ne doit pas crasher avec des données vides
        try:
            empty_table.create_table()
            empty_table.add_data()
            logger.success("✓ Gestion liste vide réussie")
        except Exception as e:
            logger.error(f"Erreur avec liste vide : {e}")
            raise

    def test_single_forecast_detail(self):
        """Test avec un seul élément"""
        logger.info("Test : Tableau à un élément")
        single_table = ForecastTable([self.forecast_details[0]])
        
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            single_table.display_table()
        
        output = captured_output.getvalue()
        self.assertIn("2025-11-17", output)
        logger.success("✓ Tableau à un élément validé")

    def test_rounding_values(self):
        """Test l'arrondi des valeurs décimales"""
        logger.info("Test : Arrondi des valeurs")
        
        details_with_decimals = [
            {
                "date_local": "2025-11-17",
                "rain_cumul_mm": 0.6900000000000001,
                "snow_cumul_mm": 0.123456789,
                "major_transitions_count": 1
            }
        ]
        
        table = ForecastTable(details_with_decimals)
        captured_output = io.StringIO()
        
        with patch('sys.stdout', captured_output):
            table.display_table()
        
        output = captured_output.getvalue()
        
        # Vérifier que les valeurs sont arrondies (pas de longues décimales)
        self.assertIn("0.69", output)
        self.assertIn("0.12", output)
        
        logger.debug("Valeurs correctement arrondies")
        logger.success("✓ Arrondi des valeurs validé")


if __name__ == "__main__":
    unittest.main()
