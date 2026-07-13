"""add_v22_delegations_table

Revision ID: ad093578553f
Revises: 9d093578553f
Create Date: 2026-07-13 10:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'ad093578553f'
down_revision: Union[str, None] = '9d093578553f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create delegation_runs table
    op.create_table('delegation_runs',
    sa.Column('workflow_run_id', sa.String(length=36), nullable=False),
    sa.Column('action_log_id', sa.String(length=36), nullable=True),
    sa.Column('parent_step_id', sa.String(length=36), nullable=True),
    sa.Column('requesting_agent', sa.String(length=50), nullable=False),
    sa.Column('specialist_type', sa.String(length=50), nullable=False),
    sa.Column('delegation_reason', sa.Text(), nullable=False),
    sa.Column('bounded_goal', sa.Text(), nullable=False),
    sa.Column('outcome_status', sa.String(length=50), nullable=False, server_default='delegated'),
    sa.Column('reasoning_summary', sa.Text(), nullable=True),
    sa.Column('structured_findings', sa.JSON(), nullable=False),
    sa.Column('suggested_next_step', sa.JSON(), nullable=False),
    sa.Column('confidence_score', sa.Float(), nullable=False, server_default='1.0'),
    sa.Column('token_cost', sa.Float(), nullable=False, server_default='0.0'),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_delegation_runs_workflow_run_id'), 'delegation_runs', ['workflow_run_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_delegation_runs_workflow_run_id'), table_name='delegation_runs')
    op.drop_table('delegation_runs')
