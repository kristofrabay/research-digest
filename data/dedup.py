import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ResearchDeduplicator:
    """Manages deduplication of research items against an existing CSV."""
    
    def __init__(self, main_csv_path: str | Path = "data/research_items.csv"):
        self.main_csv_path = Path(main_csv_path)
        self.columns = [
            "focus_area", "provider", "url", "title", 
            "source", "published", "relevance", "date_added"
        ]
    
    def load_existing(self) -> pd.DataFrame:
        """Load existing research items CSV, or create empty DataFrame if not exists."""
        if self.main_csv_path.exists():
            df = pd.read_csv(self.main_csv_path)
            logger.info(f"Loaded {len(df)} existing items from {self.main_csv_path}")
            return df
        else:
            logger.info(f"No existing CSV found at {self.main_csv_path}, starting fresh")
            return pd.DataFrame(columns=self.columns)
    
    def deduplicate(self, new_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Deduplicate new items against existing CSV.
        
        Returns:
            tuple of (updated_main_df, new_items_df)
        """
        existing_df = self.load_existing()
        existing_urls = set(existing_df["url"].tolist())
        
        # Filter to only new items
        is_new = ~new_df["url"].isin(existing_urls)
        new_items = new_df[is_new].copy()
        n_skipped = len(new_df) - len(new_items)
        
        logger.info(f"New items: {len(new_items)}, Skipped (duplicates): {n_skipped}")
        
        # Append new items to existing
        if len(new_items) > 0:
            updated_df = pd.concat([existing_df, new_items], ignore_index=True)
        else:
            updated_df = existing_df
        
        return updated_df, new_items
    
    def save(self, updated_df: pd.DataFrame) -> None:
        """Save updated main CSV."""
        updated_df.to_csv(self.main_csv_path, index=False)
        logger.info(f"Saved {len(updated_df)} items to {self.main_csv_path}")
    
    def process(self, new_df: pd.DataFrame, save: bool = True) -> dict:
        """
        Full pipeline: load existing, deduplicate, optionally save.
        
        Returns:
            dict with stats and dataframes
        """
        updated_df, new_items = self.deduplicate(new_df)
        n_skipped = len(new_df) - len(new_items)
        
        if save:
            self.save(updated_df)
        
        return {
            "total_after": len(updated_df),
            "new_added": len(new_items),
            "skipped": n_skipped,
            "updated_df": updated_df,
            "new_items": new_items,
        }


# Convenience function
def deduplicate_research(
    new_df: pd.DataFrame,
    main_csv: str = "data/research_items.csv",
    save: bool = True,
) -> dict:
    """Quick function to deduplicate new research items."""
    deduper = ResearchDeduplicator(main_csv_path=main_csv)
    return deduper.process(new_df, save=save)
