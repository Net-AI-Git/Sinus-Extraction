"""
Migration Rollback Pattern Example

This file demonstrates the generic rollback migration structure.
Reference this example from RULE.mdc using @examples_rollback.py syntax.
"""

from alembic import op
import sqlalchemy as sa


# ============================================================================
# Migration Rollback Pattern
# ============================================================================

def rollback_migration() -> None:
    """
    Generic rollback migration pattern.
    
    This demonstrates the pattern for rolling back migrations:
    - Reverse all changes from the forward migration
    - Restore previous state
    - Handle data loss scenarios
    - Ensure system can return to previous working state
    """
    # Example: Rollback column addition
    # If column was added, remove it
    op.drop_column('table_name', 'new_column')
    
    # Example: Rollback table creation
    # If table was created, drop it
    op.drop_table('new_table')
    
    # Example: Rollback index creation
    # If index was created, remove it
    op.drop_index('idx_table_name_column', table_name='table_name')
    
    # Example: Restore data from backup if needed
    # (This would typically be done separately, not in migration)


def verify_rollback_safety() -> bool:
    """
    Generic pattern for verifying rollback safety.
    
    This demonstrates the pattern for rollback verification:
    - Check if rollback would cause data loss
    - Verify no dependencies on new schema
    - Ensure backward compatibility
    
    Returns:
        bool: True if rollback is safe, False otherwise
    """
    # Example: Check if new column has data
    # If column has critical data, rollback might not be safe
    result = op.get_bind().execute(
        sa.text("SELECT COUNT(*) FROM table_name WHERE new_column IS NOT NULL")
    ).scalar()
    
    # If column has data, rollback might cause data loss
    if result > 0:
        return False
    
    return True
