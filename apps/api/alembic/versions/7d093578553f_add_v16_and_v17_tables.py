"""add_v16_and_v17_tables

Revision ID: 7d093578553f
Revises: 6c083578553e
Create Date: 2026-07-13 08:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '7d093578553f'
down_revision: Union[str, None] = '6c083578553e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Add V16 columns to action_logs
    op.add_column('action_logs', sa.Column('queued_job_id', sa.String(length=255), nullable=True))
    op.add_column('action_logs', sa.Column('queue_name', sa.String(length=255), nullable=True))
    op.add_column('action_logs', sa.Column('worker_id', sa.String(length=255), nullable=True))
    op.add_column('action_logs', sa.Column('retry_scheduled_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('action_logs', sa.Column('dead_lettered_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('action_logs', sa.Column('execution_source', sa.String(length=50), nullable=False, server_default='api'))

    # Create workflow_runs table
    op.create_table('workflow_runs',
    sa.Column('goal', sa.String(length=500), nullable=True),
    sa.Column('reasoning_summary', sa.Text(), nullable=True),
    sa.Column('steps', sa.JSON(), nullable=False),
    sa.Column('current_step_index', sa.Integer(), nullable=False, server_default='0'),
    sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
    sa.Column('autonomy_tier', sa.Integer(), nullable=False, server_default='1'),
    sa.Column('requires_approval', sa.Boolean(), nullable=False, server_default='true'),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('workflow_runs')
    op.drop_column('action_logs', 'execution_source')
    op.drop_column('action_logs', 'dead_lettered_at')
    op.drop_column('action_logs', 'retry_scheduled_at')
    op.drop_column('action_logs', 'worker_id')
    op.drop_column('action_logs', 'queue_name')
    op.drop_column('action_logs', 'queued_job_id')
