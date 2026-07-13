"""add_v19_control_events_table

Revision ID: 8d093578553f
Revises: 7d093578553f
Create Date: 2026-07-13 08:30:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '8d093578553f'
down_revision: Union[str, None] = '7d093578553f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create workflow_control_events table
    op.create_table('workflow_control_events',
    sa.Column('workflow_run_id', sa.String(length=36), nullable=False),
    sa.Column('action_log_id', sa.String(length=36), nullable=True),
    sa.Column('control_type', sa.String(length=50), nullable=False),
    sa.Column('requested_by_user_id', sa.String(length=36), nullable=False),
    sa.Column('requested_by_role', sa.String(length=50), nullable=False),
    sa.Column('reason', sa.Text(), nullable=True),
    sa.Column('applied_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('result_status', sa.String(length=50), nullable=False, server_default='pending'),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workflow_control_events_workflow_run_id'), 'workflow_control_events', ['workflow_run_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_workflow_control_events_workflow_run_id'), table_name='workflow_control_events')
    op.drop_table('workflow_control_events')
