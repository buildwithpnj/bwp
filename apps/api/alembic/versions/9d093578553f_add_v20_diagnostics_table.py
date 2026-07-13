"""add_v20_diagnostics_table

Revision ID: 9d093578553f
Revises: 8d093578553f
Create Date: 2026-07-13 09:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '9d093578553f'
down_revision: Union[str, None] = '8d093578553f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create workflow_diagnostic_reports table
    op.create_table('workflow_diagnostic_reports',
    sa.Column('workflow_run_id', sa.String(length=36), nullable=False),
    sa.Column('action_log_id', sa.String(length=36), nullable=True),
    sa.Column('diagnostic_type', sa.String(length=50), nullable=False),
    sa.Column('severity', sa.String(length=20), nullable=False),
    sa.Column('likely_causes', sa.JSON(), nullable=False),
    sa.Column('evidence_points', sa.JSON(), nullable=False),
    sa.Column('suggested_recovery_options', sa.JSON(), nullable=False),
    sa.Column('confidence_score', sa.Float(), nullable=False, server_default='1.0'),
    sa.Column('requires_human_review', sa.Boolean(), nullable=False, server_default='true'),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workflow_diagnostic_reports_workflow_run_id'), 'workflow_diagnostic_reports', ['workflow_run_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_workflow_diagnostic_reports_workflow_run_id'), table_name='workflow_diagnostic_reports')
    op.drop_table('workflow_diagnostic_reports')
