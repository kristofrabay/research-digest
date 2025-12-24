import pandas as pd
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ResearchDeduplicator:
    """Manages deduplication of research items against an existing CSV."""
    
    def __init__(
        self,
        main_csv_path: str | Path = "data/research_items.csv",
    ):
        self.main_csv_path = Path(main_csv_path)
        self.skipped_csv_path = Path(str(main_csv_path).replace("research_items", "skipped_items"))
        
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
    
    def load_existing_skipped(self) -> pd.DataFrame:
        """Load existing skipped items CSV, or create empty DataFrame if not exists."""
        if self.skipped_csv_path.exists():
            df = pd.read_csv(self.skipped_csv_path)
            logger.info(f"Loaded {len(df)} existing skipped items from {self.skipped_csv_path}")
            return df
        else:
            logger.info(f"No existing skipped CSV found at {self.skipped_csv_path}")
            return pd.DataFrame(columns=self.columns + ["skipped_at"])
    
    def deduplicate(
        self, 
        new_df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Deduplicate new items against existing CSV.
        
        Returns:
            tuple of (updated_main_df, new_items_df, skipped_items_df)
        """
        existing_df = self.load_existing()
        existing_urls = set(existing_df["url"].tolist())
        
        # Split new items into truly new vs already seen
        is_new = ~new_df["url"].isin(existing_urls)
        new_items = new_df[is_new].copy()
        skipped_items = new_df[~is_new].copy()
        
        # Log stats
        logger.info(f"New items: {len(new_items)}, Skipped (duplicates): {len(skipped_items)}")
        
        # Append new items to existing
        if len(new_items) > 0:
            updated_df = pd.concat([existing_df, new_items], ignore_index=True)
        else:
            updated_df = existing_df
        
        return updated_df, new_items, skipped_items
    
    def save(
        self,
        updated_df: pd.DataFrame,
        skipped_df: pd.DataFrame,
    ) -> None:
        """Save updated main CSV and skipped items log."""
        # Save main CSV
        updated_df.to_csv(self.main_csv_path, index=False)
        logger.info(f"Saved {len(updated_df)} items to {self.main_csv_path}")
        
        # Append skipped items to log (with timestamp), but deduplicate first
        if len(skipped_df) > 0:
            skipped_df = skipped_df.copy()
            
            # Remove duplicates within the skipped_df itself first
            skipped_df = skipped_df.drop_duplicates(subset=["url"], keep="first")
            
            skipped_df["skipped_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Load existing skipped items and deduplicate by URL
            existing_skipped = self.load_existing_skipped()
            existing_skipped_urls = set(existing_skipped["url"].tolist()) if len(existing_skipped) > 0 else set()
            
            # Only keep skipped items that haven't been logged before
            is_new_skip = ~skipped_df["url"].isin(existing_skipped_urls)
            new_skipped = skipped_df[is_new_skip].copy()
            
            if len(new_skipped) > 0:
                combined_skipped = pd.concat([existing_skipped, new_skipped], ignore_index=True)
                combined_skipped.to_csv(self.skipped_csv_path, index=False)
                logger.info(f"Logged {len(new_skipped)} new skipped items to {self.skipped_csv_path}")
            else:
                logger.info(f"No new skipped items to log (all already in {self.skipped_csv_path})")
    
    def process(
        self, 
        new_df: pd.DataFrame,
        save: bool = True,
    ) -> dict:
        """
        Full pipeline: load existing, deduplicate, optionally save.
        
        Args:
            new_df: DataFrame with new research items
            save: Whether to save results to CSV
            
        Returns:
            dict with stats and dataframes
        """
        updated_df, new_items, skipped_items = self.deduplicate(new_df)
        
        if save:
            self.save(updated_df, skipped_items)
        
        return {
            "total_after": len(updated_df),
            "new_added": len(new_items),
            "skipped": len(skipped_items),
            "updated_df": updated_df,
            "new_items": new_items,
            "skipped_items": skipped_items,
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

