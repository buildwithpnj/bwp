"""add_v35_and_v36_tables

Revision ID: fd093578553f
Revises: ed093578553f
Create Date: 2026-07-13 14:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'fd093578553f'
down_revision: Union[str, None] = 'ed093578553f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # policy_sync_jobs
    op.create_table('policy_sync_jobs',
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('source_env', sa.String(length=50), nullable=False),
    sa.Column('target_env', sa.String(length=50), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('signature', sa.String(length=255), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_policy_sync_jobs_user_id'), 'policy_sync_jobs', ['user_id'], unique=False)

    # policy_sync_targets
    op.create_table('policy_sync_targets',
    sa.Column('job_id', sa.String(length=36), nullable=False),
    sa.Column('node_ip', sa.String(length=50), nullable=False),
    sa.Column('tenant_id', sa.String(length=36), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_policy_sync_targets_job_id'), 'policy_sync_targets', ['job_id'], unique=False)
    op.create_index(op.f('ix_policy_sync_targets_tenant_id'), 'policy_sync_targets', ['tenant_id'], unique=False)

    # policy_sync_results
    op.create_table('policy_sync_results',
    sa.Column('target_id', sa.String(length=36), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('error_message', sa.Text(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_policy_sync_results_target_id'), 'policy_sync_results', ['target_id'], unique=False)

    # federated_rollback_bundles
    op.create_table('federated_rollback_bundles',
    sa.Column('job_id', sa.String(length=36), nullable=False),
    sa.Column('snapshot_data', sa.Text(), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_federated_rollback_bundles_job_id'), 'federated_rollback_bundles', ['job_id'], unique=False)

    # release_gates
    op.create_table('release_gates',
    sa.Column('rollout_id', sa.String(length=36), nullable=False),
    sa.Column('gate_type', sa.String(length=50), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_release_gates_rollout_id'), 'release_gates', ['rollout_id'], unique=False)

    # canary_rollouts
    op.create_table('canary_rollouts',
    sa.Column('rollout_id', sa.String(length=36), nullable=False),
    sa.Column('canary_percentage', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('rollout_id')
    )

    # rollout_health_snapshots
    op.create_table('rollout_health_snapshots',
    sa.Column('rollout_id', sa.String(length=36), nullable=False),
    sa.Column('health_score', sa.Float(), nullable=False),
    sa.Column('status_summary', sa.Text(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rollout_health_snapshots_rollout_id'), 'rollout_health_snapshots', ['rollout_id'], unique=False)

    # release_approval_events
    op.create_table('release_approval_events',
    sa.Column('rollout_id', sa.String(length=36), nullable=False),
    sa.Column('approved_by_user_id', sa.String(length=36), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_release_approval_events_rollout_id'), 'release_approval_events', ['rollout_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_release_approval_events_rollout_id'), table_name='release_approval_events')
    op.drop_table('release_approval_events')
    op.drop_index(op.f('ix_rollout_health_snapshots_rollout_id'), table_name='rollout_health_snapshots')
    op.drop_table('rollout_health_snapshots')
    op.drop_table('canary_rollouts')
    op.drop_index(op.f('ix_release_gates_rollout_id'), table_name='release_gates')
    op.drop_table('release_gates')
    op.drop_index(op.f('ix_federated_rollback_bundles_job_id'), table_name='federated_rollback_bundles')
    op.drop_table('federated_rollback_bundles')
    op.drop_index(op.f('ix_policy_sync_results_target_id'), table_name='policy_sync_results')
    op.drop_table('policy_sync_results')
    op.drop_index(op.f('ix_policy_sync_targets_tenant_id'), table_name='policy_sync_targets')
    op.drop_index(op.f('ix_policy_sync_targets_job_id'), table_name='policy_sync_targets')
    op.drop_table('policy_sync_targets')
    op.drop_index(op.f('ix_policy_sync_jobs_user_id'), table_name='policy_sync_jobs')
    op.drop_table('policy_sync_jobs')
