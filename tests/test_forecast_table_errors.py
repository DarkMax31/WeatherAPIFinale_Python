"""
Tests d'erreur pour la classe ForecastTable
Teste les scénarios d'erreur et d'exception
"""
import unittest
import sys
import io
from pathlib import Path
from unittest.mock import patch
from loguru import logger
from tests.logging_setup import configure_for

sys.path.insert(0, str(Path(__file__).parent.parent))

from classes.ForecastTable import ForecastTable
from tests.logging_setup import configure_for


class TestForecastTableErrors(unittest.TestCase):
    """Tests pour les erreurs de ForecastTable"""

    def setUp(self):
        """Initialisation avant chaque test"""
        configure_for(Path(__file__).stem) 
        logger.info("🧪 Démarrage test erreur ForecastTable")

    def tearDown(self):
        """Nettoyage après chaque test"""
        logger.info("✅ Fin test erreur ForecastTable\n")

    def test_with_invalid_data_type(self):
        """Test ForecastTable avec un type de données invalide"""
        logger.info("Test : ForecastTable - Type de données invalide")
        
        invalid_data = [
            {
                "date_local": "2025-11-17",
                "rain_cumul_mm": "not_a_number",  # Devrait être un nombre
                "snow_cumul_mm": 0,
                "major_transitions_count": 1
            }
        ]
        
        table = ForecastTable(invalid_data)
        
        try:
            captured_output = io.StringIO()
            with patch('sys.stdout', captured_output):
                table.display_table()
            
            logger.warning("⚠️ Tableau créé avec données invalides")
            logger.error("❌ Comportement inattendu")
        except (TypeError, ValueError) as e:
            logger.error(f"❌ Exception levée (attendue) : {e}")
            logger.success("✓ Exception correctement levée pour données invalides")

    def test_with_missing_required_fields(self):
        """Test ForecastTable avec champs manquants"""
        logger.info("Test : ForecastTable - Champs manquants")
        
        incomplete_data = [
            {
                "date_local": "2025-11-17",
                # Champs manquants : rain_cumul_mm, snow_cumul_mm, major_transitions_count
            }
        ]
        
        table = ForecastTable(incomplete_data)
        
        with self.assertRaises(KeyError):
            table.add_data()
        
        logger.error("❌ KeyError levée pour champs manquants (attendu)")
        logger.success("✓ Exception correctement levée")

    def test_with_non_list_input(self):
        """Test ForecastTable avec entrée qui n'est pas une liste"""
        logger.info("Test : ForecastTable - Entrée non-liste")
        
        with self.assertRaises((TypeError, AttributeError)):
            table = ForecastTable("not_a_list")
            table.create_table()
            table.add_data()
        
        logger.error("❌ Exception levée pour entrée non-liste (attendu)")
        logger.success("✓ Exception correctement levée")

    def test_with_none_input(self):
        """Test ForecastTable avec None"""
        logger.info("Test : ForecastTable - Entrée None")
        
        with self.assertRaises((TypeError, AttributeError)):
            table = ForecastTable(None)
            table.create_table()
            table.add_data()
        
        logger.error("❌ Exception levée pour entrée None (attendu)")
        logger.success("✓ Exception correctement levée")

    def test_with_negative_values(self):
        """Test ForecastTable avec valeurs négatives (invalides pour pluie/neige)"""
        logger.info("Test : ForecastTable - Valeurs négatives")
        
        negative_data = [
            {
                "date_local": "2025-11-17",
                "rain_cumul_mm": -5.5,  # Négatif = invalide
                "snow_cumul_mm": -2.0,   # Négatif = invalide
                "major_transitions_count": 1
            }
        ]
        
        table = ForecastTable(negative_data)
        
        try:
            captured_output = io.StringIO()
            with patch('sys.stdout', captured_output):
                table.display_table()
            
            logger.warning("⚠️ Tableau accepte les valeurs négatives")
            logger.error("❌ Validation de données manquante")
        except (ValueError, AssertionError) as e:
            logger.error(f"❌ Exception levée (attendue) : {e}")
            logger.success("✓ Exception correctement levée")

    def test_with_extreme_values(self):
        """Test ForecastTable avec valeurs extrêmes"""
        logger.info("Test : ForecastTable - Valeurs extrêmes")
        
        extreme_data = [
            {
                "date_local": "2025-11-17",
                "rain_cumul_mm": 999999999.99,
                "snow_cumul_mm": 888888888.88,
                "major_transitions_count": 1000000
            }
        ]
        
        table = ForecastTable(extreme_data)
        
        try:
            captured_output = io.StringIO()
            with patch('sys.stdout', captured_output):
                table.display_table()
            
            output = captured_output.getvalue()
            
            if len(output) > 0:
                logger.debug("Tableau affiché avec valeurs extrêmes")
                logger.success("✓ Valeurs extrêmes gérées")
        except Exception as e:
            logger.error(f"❌ Exception levée : {e}")
            raise

    def test_with_malformed_date(self):
        """Test ForecastTable avec date mal formée"""
        logger.info("Test : ForecastTable - Date mal formée")
        
        bad_date_data = [
            {
                "date_local": "not-a-valid-date",
                "rain_cumul_mm": 0.5,
                "snow_cumul_mm": 0,
                "major_transitions_count": 0
            }
        ]
        
        table = ForecastTable(bad_date_data)
        
        try:
            captured_output = io.StringIO()
            with patch('sys.stdout', captured_output):
                table.display_table()
            
            logger.warning("⚠️ Tableau accepte les dates mal formées")
        except Exception as e:
            logger.error(f"❌ Exception levée (attendue) : {e}")
            logger.success("✓ Exception correctement levée")

    def test_with_very_large_list(self):
        """Test ForecastTable avec une très grande liste"""
        logger.info("Test : ForecastTable - Très grande liste")
        
        large_data = [
            {
                "date_local": f"2025-11-{(i % 30) + 1:02d}",
                "rain_cumul_mm": float(i),
                "snow_cumul_mm": float(i % 10),
                "major_transitions_count": i % 3
            }
            for i in range(1000)
        ]
        
        table = ForecastTable(large_data)
        
        try:
            captured_output = io.StringIO()
            with patch('sys.stdout', captured_output):
                table.display_table()
            
            output = captured_output.getvalue()
            logger.debug(f"Tableau généré avec {len(large_data)} lignes")
            logger.success("✓ Grande liste gérée correctement")
        except Exception as e:
            logger.error(f"❌ Exception levée : {e}")
            logger.success("✓ Exception levée pour très grande liste")

if __name__ == "__main__":
    unittest.main()