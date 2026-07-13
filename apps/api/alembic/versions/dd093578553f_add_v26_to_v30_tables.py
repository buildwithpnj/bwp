"""add_v26_to_v30_tables

Revision ID: dd093578553f
Revises: cd093578553f
Create Date: 2026-07-13 12:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'dd093578553f'
down_revision: Union[str, None] = 'cd093578553f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # copilot_sessions
    op.create_table('copilot_sessions',
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('chat_history', sa.JSON(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_copilot_sessions_user_id'), 'copilot_sessions', ['user_id'], unique=False)

    # tenant_modality_quotas
    op.create_table('tenant_modality_quotas',
    sa.Column('tenant_id', sa.String(length=36), nullable=False),
    sa.Column('daily_bytes_limit', sa.BigInteger(), nullable=False),
    sa.Column('daily_bytes_used', sa.BigInteger(), nullable=False),
    sa.Column('requests_count_limit', sa.Integer(), nullable=False),
    sa.Column('requests_count_used', sa.Integer(), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tenant_modality_quotas_tenant_id'), 'tenant_modality_quotas', ['tenant_id'], unique=False)

    # objective_runs
    op.create_table('objective_runs',
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('progress_percent', sa.Float(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('stop_condition', sa.String(length=255), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_objective_runs_user_id'), 'objective_runs', ['user_id'], unique=False)

    # objective_checkpoints
    op.create_table('objective_checkpoints',
    sa.Column('objective_run_id', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('due_at', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_objective_checkpoints_objective_run_id'), 'objective_checkpoints', ['objective_run_id'], unique=False)

    # simulation_runs
    op.create_table('simulation_runs',
    sa.Column('workflow_run_id', sa.String(length=36), nullable=True),
    sa.Column('plan_steps', sa.JSON(), nullable=False),
    sa.Column('predicted_success_score', sa.Float(), nullable=False),
    sa.Column('likely_failures', sa.JSON(), nullable=False),
    sa.Column('risk_score', sa.Float(), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_simulation_runs_workflow_run_id'), 'simulation_runs', ['workflow_run_id'], unique=False)

    # context_compaction_runs
    op.create_table('context_compaction_runs',
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('raw_tokens_count', sa.Integer(), nullable=False),
    sa.Column('compacted_tokens_count', sa.Integer(), nullable=False),
    sa.Column('reduction_ratio', sa.Float(), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_context_compaction_runs_user_id'), 'context_compaction_runs', ['user_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_context_compaction_runs_user_id'), table_name='context_compaction_runs')
    op.drop_table('context_compaction_runs')
    op.drop_index(op.f('ix_simulation_runs_workflow_run_id'), table_name='simulation_runs')
    op.drop_table('simulation_runs')
    op.drop_index(op.f('ix_objective_checkpoints_objective_run_id'), table_name='objective_checkpoints')
    op.drop_table('objective_checkpoints')
    op.drop_index(op.f('ix_objective_runs_user_id'), table_name='objective_runs')
    op.drop_table('objective_runs')
    op.drop_index(op.f('ix_tenant_modality_quotas_tenant_id'), table_name='tenant_modality_quotas')
    op.drop_table('tenant_modality_quotas')
    op.drop_index(op.f('ix_copilot_sessions_user_id'), table_name='copilot_sessions')
    op.drop_table('copilot_sessions')
