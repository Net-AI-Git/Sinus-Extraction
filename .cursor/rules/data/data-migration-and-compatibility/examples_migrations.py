"""
Database Migration Pattern Example

This file demonstrates the generic Alembic migration structure pattern.
Reference this example from RULE.mdc using @examples_migrations.py syntax.
"""

from alembic import op
import sqlalchemy as sa


# ============================================================================
# Alembic Migration Pattern
# ============================================================================

def upgrade() -> None:
    """
    Generic migration upgrade pattern.
    
    This demonstrates the pattern for additive migrations:
    - Add new column (nullable for backward compatibility)
    - Create new table
    - Add indexes
    - All changes are additive (low risk)
    """
    # Example: Add new column
    op.add_column(
        'table_name',
        sa.Column('new_column', sa.String(255), nullable=True)
    )
    
    # Example: Create new table
    op.create_table(
        'new_table',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Example: Add index
    op.create_index(
        'idx_table_name_column',
        'table_name',
        ['column_name']
    )


def downgrade() -> None:
    """
    Generic migration downgrade pattern.
    
    This demonstrates the pattern for reverse migrations:
    - Remove indexes
    - Drop tables
    - Remove columns
    - Reverse all changes from upgrade()
    """
    # Example: Remove index
    op.drop_index('idx_table_name_column', table_name='table_name')
    
    # Example: Drop table
    op.drop_table('new_table')
    
    # Example: Remove column
    op.drop_column('table_name', 'new_column')
