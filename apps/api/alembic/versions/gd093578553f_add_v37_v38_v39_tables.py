"""add_v37_v38_v39_tables

Revision ID: gd093578553f
Revises: fd093578553f
Create Date: 2026-07-13 15:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'gd093578553f'
down_revision: Union[str, None] = 'fd093578553f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # telemetry_events
    op.create_table('telemetry_events',
    sa.Column('tenant_id', sa.String(length=36), nullable=False),
    sa.Column('node_id', sa.String(length=50), nullable=False),
    sa.Column('service_name', sa.String(length=50), nullable=False),
    sa.Column('environment', sa.String(length=50), nullable=False),
    sa.Column('signal_type', sa.String(length=20), nullable=False),
    sa.Column('payload', sa.Text(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_telemetry_events_tenant_id'), 'telemetry_events', ['tenant_id'], unique=False)

    # telemetry_metric_snapshots
    op.create_table('telemetry_metric_snapshots',
    sa.Column('tenant_id', sa.String(length=36), nullable=False),
    sa.Column('node_id', sa.String(length=50), nullable=False),
    sa.Column('metric_name', sa.String(length=100), nullable=False),
    sa.Column('metric_value', sa.Float(), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_telemetry_metric_snapshots_tenant_id'), 'telemetry_metric_snapshots', ['tenant_id'], unique=False)

    # anomaly_incidents
    op.create_table('anomaly_incidents',
    sa.Column('tenant_id', sa.String(length=36), nullable=False),
    sa.Column('signal_type', sa.String(length=50), nullable=False),
    sa.Column('severity', sa.String(length=20), nullable=False),
    sa.Column('incident_status', sa.String(length=20), nullable=False),
    sa.Column('correlation_key', sa.String(length=100), nullable=True),
    sa.Column('summary', sa.Text(), nullable=False),
    sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_anomaly_incidents_tenant_id'), 'anomaly_incidents', ['tenant_id'], unique=False)

    # anomaly_correlation_links
    op.create_table('anomaly_correlation_links',
    sa.Column('parent_incident_id', sa.String(length=36), nullable=False),
    sa.Column('child_incident_id', sa.String(length=36), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_anomaly_correlation_links_parent_incident_id'), 'anomaly_correlation_links', ['parent_incident_id'], unique=False)
    op.create_index(op.f('ix_anomaly_correlation_links_child_incident_id'), 'anomaly_correlation_links', ['child_incident_id'], unique=False)

    # resilience_states
    op.create_table('resilience_states',
    sa.Column('trigger_type', sa.String(length=50), nullable=False),
    sa.Column('affected_scope', sa.String(length=100), nullable=False),
    sa.Column('degradation_level', sa.String(length=20), nullable=False),
    sa.Column('token_budget_reduction_factor', sa.Float(), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    # degraded_mode_activations
    op.create_table('degraded_mode_activations',
    sa.Column('affected_scope', sa.String(length=100), nullable=False),
    sa.Column('activated_features', sa.Text(), nullable=True),
    sa.Column('disabled_features', sa.Text(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    # recovery_transitions
    op.create_table('recovery_transitions',
    sa.Column('affected_scope', sa.String(length=100), nullable=False),
    sa.Column('recovery_status', sa.String(length=20), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    # ops_risk_snapshots
    op.create_table('ops_risk_snapshots',
    sa.Column('tenant_scope', sa.String(length=36), nullable=False),
    sa.Column('cluster_scope', sa.String(length=100), nullable=False),
    sa.Column('risk_score', sa.Float(), nullable=False),
    sa.Column('confidence_score', sa.Float(), nullable=False),
    sa.Column('recommended_prevention', sa.Text(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ops_risk_snapshots_tenant_scope'), 'ops_risk_snapshots', ['tenant_scope'], unique=False)

    # predictive_incident_signals
    op.create_table('predictive_incident_signals',
    sa.Column('pattern_family', sa.String(length=100), nullable=False),
    sa.Column('leading_signals', sa.Text(), nullable=False),
    sa.Column('projected_impact', sa.Text(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    # pattern_regression_cases
    op.create_table('pattern_regression_cases',
    sa.Column('pattern_family', sa.String(length=100), nullable=False),
    sa.Column('regression_score', sa.Float(), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('pattern_regression_cases')
    op.drop_table('predictive_incident_signals')
    op.drop_index(op.f('ix_ops_risk_snapshots_tenant_scope'), table_name='ops_risk_snapshots')
    op.drop_table('ops_risk_snapshots')
    op.drop_table('recovery_transitions')
    op.drop_table('degraded_mode_activations')
    op.drop_table('resilience_states')
    op.drop_index(op.f('ix_anomaly_correlation_links_child_incident_id'), table_name='anomaly_correlation_links')
    op.drop_index(op.f('ix_anomaly_correlation_links_parent_incident_id'), table_name='anomaly_correlation_links')
    op.drop_table('anomaly_correlation_links')
    op.drop_index(op.f('ix_anomaly_incidents_tenant_id'), table_name='anomaly_incidents')
    op.drop_table('anomaly_incidents')
    op.drop_index(op.f('ix_telemetry_metric_snapshots_tenant_id'), table_name='telemetry_metric_snapshots')
    op.drop_table('telemetry_metric_snapshots')
    op.drop_index(op.f('ix_telemetry_events_tenant_id'), table_name='telemetry_events')
    op.drop_table('telemetry_events')
