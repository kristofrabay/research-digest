import subprocess
import sys
import logging
import time
from datetime import datetime
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

def format_duration(seconds: float) -> str:
    """Format seconds into human-readable duration."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.1f}m"
    hours = minutes / 60
    return f"{hours:.1f}h"

def main():
    pipeline_start = time.time()
    start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    logger.info(f"{'='*50}")
    logger.info(f"🚀 Pipeline started at {start_timestamp}")
    logger.info(f"{'='*50}\n")
    
    for script in SCRIPTS:
        script_path = SCRIPTS_DIR / script
        logger.info(f"{'='*50}")
        logger.info(f"Running {script}")
        logger.info(f"{'='*50}")
        
        step_start = time.time()
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=SCRIPTS_DIR.parent,  # run from repo root
        )
        step_duration = time.time() - step_start
        
        if result.returncode != 0:
            logger.error(f"❌ {script} failed with code {result.returncode}")
            sys.exit(result.returncode)
        
        logger.info(f"✅ {script} complete ({format_duration(step_duration)})\n")
    
    pipeline_end = time.time()
    end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_duration = pipeline_end - pipeline_start
    total_minutes = total_duration / 60
    
    logger.info(f"{'='*50}")
    logger.info(f"🎉 Pipeline complete!")
    logger.info(f"   Started:  {start_timestamp}")
    logger.info(f"   Finished: {end_timestamp}")
    logger.info(f"   Duration: {total_minutes:.1f} minutes ({format_duration(total_duration)})")
    logger.info(f"{'='*50}")

if __name__ == "__main__":
    main()