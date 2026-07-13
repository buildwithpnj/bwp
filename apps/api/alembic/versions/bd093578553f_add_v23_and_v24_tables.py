"""add_v23_and_v24_tables

Revision ID: bd093578553f
Revises: ad093578553f
Create Date: 2026-07-13 11:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'bd093578553f'
down_revision: Union[str, None] = 'ad093578553f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create collaboration_runs table
    op.create_table('collaboration_runs',
    sa.Column('workflow_run_id', sa.String(length=36), nullable=False),
    sa.Column('participating_agents', sa.JSON(), nullable=False),
    sa.Column('coordination_status', sa.String(length=50), nullable=False, server_default='active'),
    sa.Column('max_total_steps', sa.Integer(), nullable=False, server_default='10'),
    sa.Column('max_parallel_branches', sa.Integer(), nullable=False, server_default='3'),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_collaboration_runs_workflow_run_id'), 'collaboration_runs', ['workflow_run_id'], unique=False)

    # Create collaboration_handoffs table
    op.create_table('collaboration_handoffs',
    sa.Column('collaboration_run_id', sa.String(length=36), nullable=False),
    sa.Column('sender_agent', sa.String(length=50), nullable=False),
    sa.Column('receiver_agent', sa.String(length=50), nullable=False),
    sa.Column('payload_contract', sa.JSON(), nullable=False),
    sa.Column('handoff_status', sa.String(length=50), nullable=False, server_default='pending'),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_collaboration_handoffs_collaboration_run_id'), 'collaboration_handoffs', ['collaboration_run_id'], unique=False)

    # Create delegation_policy_feedbacks table
    op.create_table('delegation_policy_feedbacks',
    sa.Column('specialist_type', sa.String(length=50), nullable=False),
    sa.Column('workflow_type', sa.String(length=50), nullable=False),
    sa.Column('usefulness_score', sa.Float(), nullable=False, server_default='1.0'),
    sa.Column('latency_ms', sa.Float(), nullable=False, server_default='0.0'),
    sa.Column('token_cost', sa.Float(), nullable=False, server_default='0.0'),
    sa.Column('user_interventions_count', sa.Integer(), nullable=False, server_default='0'),
    sa.Column('was_successful', sa.Boolean(), nullable=False, server_default='true'),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_delegation_policy_feedbacks_specialist_type'), 'delegation_policy_feedbacks', ['specialist_type'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_delegation_policy_feedbacks_specialist_type'), table_name='delegation_policy_feedbacks')
    op.drop_table('delegation_policy_feedbacks')
    op.drop_index(op.f('ix_collaboration_handoffs_collaboration_run_id'), table_name='collaboration_handoffs')
    op.drop_table('collaboration_handoffs')
    op.drop_index(op.f('ix_collaboration_runs_workflow_run_id'), table_name='collaboration_runs')
    op.drop_table('collaboration_runs')
