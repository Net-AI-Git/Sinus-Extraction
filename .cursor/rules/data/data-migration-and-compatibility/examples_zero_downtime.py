"""
Zero-Downtime Migration Pattern Example

This file demonstrates the generic dual-write and gradual migration pattern.
Reference this example from RULE.mdc using @examples_zero_downtime.py syntax.
"""

from typing import Dict, Any
from alembic import op
import sqlalchemy as sa


# ============================================================================
# Zero-Downtime Migration Pattern
# ============================================================================

def migrate_zero_downtime() -> None:
    """
    Generic zero-downtime migration pattern using dual-write strategy.
    
    This demonstrates the pattern for zero-downtime migrations:
    1. Add new column (nullable)
    2. Application writes to both old and new columns
    3. Backfill existing data to new column
    4. Application reads from new column
    5. Remove old column
    
    This pattern ensures no downtime during migration.
    """
    # Step 1: Add new column (nullable for backward compatibility)
    op.add_column(
        'table_name',
        sa.Column('new_column', sa.String(255), nullable=True)
    )
    
    # Step 2: Application code writes to both old_column and new_column
    # (This is handled in application code, not migration)
    
    # Step 3: Backfill existing data
    op.execute("""
        UPDATE table_name
        SET new_column = old_column
        WHERE new_column IS NULL
    """)
    
    # Step 4: Make new column NOT NULL after backfill
    op.alter_column(
        'table_name',
        'new_column',
        nullable=False
    )
    
    # Step 5: Application code switches to read from new_column
    # (This is handled in application code, not migration)
    
    # Step 6: Remove old column (in separate migration after verification)
    # op.drop_column('table_name', 'old_column')


class DualWriteHandler:
    """
    Generic dual-write handler pattern.
    
    This demonstrates the application-level pattern for dual-write:
    - Write to both old and new formats during migration
    - Read from old format until migration complete
    - Switch to new format after migration verified
    """
    
    def __init__(self, use_new_format: bool = False):
        """
        Initialize dual-write handler.
        
        Args:
            use_new_format: Whether to use new format (set after migration verified)
        """
        self.use_new_format = use_new_format
    
    def write_data(self, data: Dict[str, Any]) -> None:
        """
        Write data to both old and new formats during migration.
        
        This demonstrates the dual-write pattern:
        - Always write to old format (for backward compatibility)
        - Also write to new format (for migration)
        - After migration verified, can stop writing to old format
        
        Args:
            data: Data to write
        """
        # Write to old format (always, for backward compatibility)
        self._write_old_format(data)
        
        # Write to new format (during migration period)
        if not self.use_new_format:
            self._write_new_format(data)
    
    def _write_old_format(self, data: Dict[str, Any]) -> None:
        """Write to old format."""
        pass
    
    def _write_new_format(self, data: Dict[str, Any]) -> None:
        """Write to new format."""
        pass
