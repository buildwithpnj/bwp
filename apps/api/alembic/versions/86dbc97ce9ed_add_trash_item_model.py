"""add_trash_item_model

Revision ID: 86dbc97ce9ed
Revises: 037df95be222
Create Date: 2026-07-14 00:47:04.543671
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '86dbc97ce9ed'
down_revision: Union[str, None] = '037df95be222'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('trash_items',
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('item_type', sa.String(length=50), nullable=False),
        sa.Column('item_id', sa.String(length=36), nullable=False),
        sa.Column('original_data', sa.JSON(), nullable=False),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trash_items_item_id'), 'trash_items', ['item_id'], unique=False)
    op.create_index(op.f('ix_trash_items_user_id'), 'trash_items', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_trash_items_user_id'), table_name='trash_items')
    op.drop_index(op.f('ix_trash_items_item_id'), table_name='trash_items')
    op.drop_table('trash_items')
