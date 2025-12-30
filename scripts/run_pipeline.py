import subprocess
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

SCRIPTS_DIR = Path(__file__).parent
SCRIPTS = [
    "01_research.py",
    "02_scouting.py",
    "03_load_content.py",
    "04_curation.py",
    "05_digest.py",
]

def main():
    for script in SCRIPTS:
        script_path = SCRIPTS_DIR / script
        logger.info(f"{'='*50}")
        logger.info(f"Running {script}")
        logger.info(f"{'='*50}")
        
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=SCRIPTS_DIR.parent,  # run from repo root
        )
        
        if result.returncode != 0:
            logger.error(f"❌ {script} failed with code {result.returncode}")
            sys.exit(result.returncode)
        
        logger.info(f"✅ {script} complete\n")
    
    logger.info("🎉 Pipeline complete!")

if __name__ == "__main__":
    main()