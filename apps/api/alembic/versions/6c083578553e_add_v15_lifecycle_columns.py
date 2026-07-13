"""add_v15_lifecycle_columns

Revision ID: 6c083578553e
Revises: 5b073578553e
Create Date: 2026-07-13 07:42:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '6c083578553e'
down_revision: Union[str, None] = '5b073578553e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('action_logs', sa.Column('suggested_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('action_logs', sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('action_logs', sa.Column('queued_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('action_logs', sa.Column('execution_started_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('action_logs', sa.Column('executed_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('action_logs', sa.Column('failed_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('action_logs', sa.Column('rolled_back_at', sa.DateTime(timezone=True), nullable=True))
    
    op.add_column('action_logs', sa.Column('retry_count', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('action_logs', sa.Column('max_retries', sa.Integer(), nullable=False, server_default='3'))
    op.add_column('action_logs', sa.Column('last_error', sa.Text(), nullable=True))
    
    op.add_column('action_logs', sa.Column('execution_status', sa.String(length=50), nullable=False, server_default='suggested'))
    op.add_column('action_logs', sa.Column('recovery_status', sa.String(length=50), nullable=False, server_default='none'))
    op.add_column('action_logs', sa.Column('idempotency_key', sa.String(length=255), nullable=True))
    op.create_index(op.f('ix_action_logs_idempotency_key'), 'action_logs', ['idempotency_key'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_action_logs_idempotency_key'), table_name='action_logs')
    op.drop_column('action_logs', 'idempotency_key')
    op.drop_column('action_logs', 'recovery_status')
    op.drop_column('action_logs', 'execution_status')
    op.drop_column('action_logs', 'last_error')
    op.drop_column('action_logs', 'max_retries')
    op.drop_column('action_logs', 'retry_count')
    
    op.drop_column('action_logs', 'rolled_back_at')
    op.drop_column('action_logs', 'failed_at')
    op.drop_column('action_logs', 'executed_at')
    op.drop_column('action_logs', 'execution_started_at')
    op.drop_column('action_logs', 'queued_at')
    op.drop_column('action_logs', 'approved_at')
    op.drop_column('action_logs', 'suggested_at')
