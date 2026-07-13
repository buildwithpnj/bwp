"""add_rag_tables

Revision ID: hd093578553f
Revises: gd093578553f
Create Date: 2026-07-13 16:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'hd093578553f'
down_revision: Union[str, None] = 'gd093578553f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # knowledge_documents
    op.create_table('knowledge_documents',
    sa.Column('tenant_id', sa.String(length=36), nullable=False),
    sa.Column('source_type', sa.String(length=50), nullable=False),
    sa.Column('source_path', sa.String(length=255), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('slug', sa.String(length=255), nullable=False),
    sa.Column('content_hash', sa.String(length=64), nullable=False),
    sa.Column('canonical_text', sa.Text(), nullable=False),
    sa.Column('visibility_scope', sa.String(length=20), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_knowledge_documents_tenant_id'), 'knowledge_documents', ['tenant_id'], unique=False)

    # knowledge_chunks
    op.create_table('knowledge_chunks',
    sa.Column('document_id', sa.String(length=36), nullable=False),
    sa.Column('tenant_id', sa.String(length=36), nullable=False),
    sa.Column('chunk_text', sa.Text(), nullable=False),
    sa.Column('chunk_summary', sa.Text(), nullable=False),
    sa.Column('token_count', sa.Integer(), nullable=False),
    sa.Column('heading_hierarchy', sa.String(length=255), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_knowledge_chunks_tenant_id'), 'knowledge_chunks', ['tenant_id'], unique=False)

    # knowledge_sources
    op.create_table('knowledge_sources',
    sa.Column('tenant_id', sa.String(length=36), nullable=False),
    sa.Column('source_type', sa.String(length=50), nullable=False),
    sa.Column('uri', sa.String(length=255), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_knowledge_sources_tenant_id'), 'knowledge_sources', ['tenant_id'], unique=False)

    # knowledge_index_runs
    op.create_table('knowledge_index_runs',
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('documents_added', sa.Integer(), nullable=False),
    sa.Column('chunks_created', sa.Integer(), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    # retrieval_traces
    op.create_table('retrieval_traces',
    sa.Column('query_text', sa.Text(), nullable=False),
    sa.Column('rewritten_query', sa.Text(), nullable=True),
    sa.Column('strategy_used', sa.String(length=50), nullable=False),
    sa.Column('latency_ms', sa.Float(), nullable=False),
    sa.Column('confidence_score', sa.Float(), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    # retrieval_feedbacks
    op.create_table('retrieval_feedbacks',
    sa.Column('trace_id', sa.String(length=36), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.Column('notes', sa.String(length=255), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_retrieval_feedbacks_trace_id'), 'retrieval_feedbacks', ['trace_id'], unique=False)

def downgrade() -> None:
    op.drop_table('retrieval_feedbacks')
    op.drop_table('retrieval_traces')
    op.drop_table('knowledge_index_runs')
    op.drop_table('knowledge_sources')
    op.drop_table('knowledge_chunks')
    op.drop_table('knowledge_documents')
