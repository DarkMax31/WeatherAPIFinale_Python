from pathlib import Path
from loguru import logger
import sys

def configure_for(module_name: str):
    """Configure logging pour un module de test spécifique."""

    # Reset ALL handlers, important for tests
    logger.remove()

    # Console output
    logger.add(sys.stdout, format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")

    # Ensure logs/ exists
    logs_dir = Path(__file__).parent.parent / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Log file per test module
    logfile = logs_dir / f"{module_name}.log"

    logger.add(logfile, format="{time} | {level} | {message}")
    logger.debug(f"Logging configuré pour le module : {module_name}, fichier de log : {logfile}")