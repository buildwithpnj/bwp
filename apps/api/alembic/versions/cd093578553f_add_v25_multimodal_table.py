"""add_v25_multimodal_table

Revision ID: cd093578553f
Revises: bd093578553f
Create Date: 2026-07-13 11:30:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'cd093578553f'
down_revision: Union[str, None] = 'bd093578553f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create multimodal_ingest_logs table
    op.create_table('multimodal_ingest_logs',
    sa.Column('workflow_run_id', sa.String(length=36), nullable=True),
    sa.Column('media_type', sa.String(length=50), nullable=False),
    sa.Column('raw_filename', sa.String(length=255), nullable=False),
    sa.Column('extracted_text', sa.Text(), nullable=True),
    sa.Column('detected_entities', sa.JSON(), nullable=False),
    sa.Column('safety_flags', sa.JSON(), nullable=False),
    sa.Column('confidence', sa.Float(), nullable=False, server_default='1.0'),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_multimodal_ingest_logs_workflow_run_id'), 'multimodal_ingest_logs', ['workflow_run_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_multimodal_ingest_logs_workflow_run_id'), table_name='multimodal_ingest_logs')
    op.drop_table('multimodal_ingest_logs')
