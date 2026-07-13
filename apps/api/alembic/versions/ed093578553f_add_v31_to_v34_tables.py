"""add_v31_to_v34_tables

Revision ID: ed093578553f
Revises: dd093578553f
Create Date: 2026-07-13 13:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'ed093578553f'
down_revision: Union[str, None] = 'dd093578553f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # notification_events
    op.create_table('notification_events',
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('source_type', sa.String(length=50), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('priority', sa.String(length=20), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_events_user_id'), 'notification_events', ['user_id'], unique=False)

    # notification_delivery_logs
    op.create_table('notification_delivery_logs',
    sa.Column('notification_event_id', sa.String(length=36), nullable=False),
    sa.Column('channel', sa.String(length=20), nullable=False),
    sa.Column('delivered_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_delivery_logs_notification_event_id'), 'notification_delivery_logs', ['notification_event_id'], unique=False)

    # operating_threads
    op.create_table('operating_threads',
    sa.Column('user_id', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_operating_threads_user_id'), 'operating_threads', ['user_id'], unique=False)

    # thread_context_links
    op.create_table('thread_context_links',
    sa.Column('operating_thread_id', sa.String(length=36), nullable=False),
    sa.Column('linked_entity_type', sa.String(length=50), nullable=False),
    sa.Column('linked_entity_id', sa.String(length=36), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_thread_context_links_operating_thread_id'), 'thread_context_links', ['operating_thread_id'], unique=False)

    # governance_policy_changes
    op.create_table('governance_policy_changes',
    sa.Column('changed_by_user_id', sa.String(length=36), nullable=False),
    sa.Column('target_tenant_id', sa.String(length=36), nullable=False),
    sa.Column('field_name', sa.String(length=100), nullable=False),
    sa.Column('old_value', sa.Text(), nullable=True),
    sa.Column('new_value', sa.Text(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_governance_policy_changes_target_tenant_id'), 'governance_policy_changes', ['target_tenant_id'], unique=False)

    # tenant_agent_policies
    op.create_table('tenant_agent_policies',
    sa.Column('tenant_id', sa.String(length=36), nullable=False),
    sa.Column('agent_type', sa.String(length=50), nullable=False),
    sa.Column('is_enabled', sa.Boolean(), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tenant_agent_policies_tenant_id'), 'tenant_agent_policies', ['tenant_id'], unique=False)

    # tenant_alert_rules
    op.create_table('tenant_alert_rules',
    sa.Column('tenant_id', sa.String(length=36), nullable=False),
    sa.Column('rule_name', sa.String(length=100), nullable=False),
    sa.Column('is_muted', sa.Boolean(), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tenant_alert_rules_tenant_id'), 'tenant_alert_rules', ['tenant_id'], unique=False)

    # tenant_copilot_configs
    op.create_table('tenant_copilot_configs',
    sa.Column('tenant_id', sa.String(length=36), nullable=False),
    sa.Column('voice_enabled', sa.Boolean(), nullable=False),
    sa.Column('proactive_tips_enabled', sa.Boolean(), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tenant_copilot_configs_tenant_id'), 'tenant_copilot_configs', ['tenant_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_tenant_copilot_configs_tenant_id'), table_name='tenant_copilot_configs')
    op.drop_table('tenant_copilot_configs')
    op.drop_index(op.f('ix_tenant_alert_rules_tenant_id'), table_name='tenant_alert_rules')
    op.drop_table('tenant_alert_rules')
    op.drop_index(op.f('ix_tenant_agent_policies_tenant_id'), table_name='tenant_agent_policies')
    op.drop_table('tenant_agent_policies')
    op.drop_index(op.f('ix_governance_policy_changes_target_tenant_id'), table_name='governance_policy_changes')
    op.drop_table('governance_policy_changes')
    op.drop_index(op.f('ix_thread_context_links_operating_thread_id'), table_name='thread_context_links')
    op.drop_table('thread_context_links')
    op.drop_index(op.f('ix_operating_threads_user_id'), table_name='operating_threads')
    op.drop_table('operating_threads')
    op.drop_index(op.f('ix_notification_delivery_logs_notification_event_id'), table_name='notification_delivery_logs')
    op.drop_table('notification_delivery_logs')
    op.drop_index(op.f('ix_notification_events_user_id'), table_name='notification_events')
    op.drop_table('notification_events')
