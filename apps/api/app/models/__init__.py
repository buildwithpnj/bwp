from app.models.base import Base, TimestampMixin, UUIDMixin
from app.models.books import Book, Highlight
from app.models.finance import Account, Budget, Category, Transaction
from app.models.gdrive import GoogleCredentials
from app.models.habits import Habit, HabitLog, JournalEntry
from app.models.notes import Embedding, Note, NoteLink
from app.models.staging import StagingEntry
from app.models.tools import Automation, ToolRecord, ToolSchema
from app.models.user import User
from app.models.storage_provider import StorageProvider
from app.models.recovery import Addiction, RelapseLog
from app.models.goals import Goal
from app.models.calendar_event import CalendarEvent
from app.models.ai_insight import AICoachInsight
from app.models.governance import AccessRequest, PreviewSession, SystemConfig, AdminAuditLog
from app.models.user_profile_memory import UserProfileMemory
from app.models.learning_progress import LearningProgress
from app.models.action_models import ActionDefinition, ActionLog, ActionApproval, TrashItem
from app.models.project_item import ProjectItem

# V37-V39 Models
from app.models.telemetry_event import TelemetryEvent
from app.models.telemetry_metric_snapshot import TelemetryMetricSnapshot
from app.models.anomaly_incident import AnomalyIncident
from app.models.anomaly_correlation_link import AnomalyCorrelationLink
from app.models.resilience_state import ResilienceState
from app.models.degraded_mode_activation import DegradedModeActivation
from app.models.recovery_transition import RecoveryTransition
from app.models.ops_risk_snapshot import OpsRiskSnapshot
from app.models.predictive_incident_signal import PredictiveIncidentSignal
from app.models.pattern_regression_case import PatternRegressionCase

# RAG Models
from app.models.knowledge_document import KnowledgeDocument
from app.models.knowledge_chunk import KnowledgeChunk
from app.models.knowledge_source import KnowledgeSource
from app.models.knowledge_index_run import KnowledgeIndexRun
from app.models.retrieval_trace import RetrievalTrace
from app.models.retrieval_feedback import RetrievalFeedback

__all__ = [
    "Base",
    "TimestampMixin",
    "UUIDMixin",
    "User",
    "GoogleCredentials",
    "Account",
    "Transaction",
    "Category",
    "Budget",
    "Book",
    "Highlight",
    "Habit",
    "HabitLog",
    "JournalEntry",
    "Note",
    "NoteLink",
    "Embedding",
    "ToolSchema",
    "ToolRecord",
    "Automation",
    "StagingEntry",
    "StorageProvider",
    "Addiction",
    "RelapseLog",
    "Goal",
    "CalendarEvent",
    "AICoachInsight",
    "AccessRequest",
    "PreviewSession",
    "SystemConfig",
    "AdminAuditLog",
    "UserProfileMemory",
    "LearningProgress",
    "ActionDefinition",
    "ActionLog",
    "ActionApproval",
    "ProjectItem",
    "TrashItem",
    
    # V37-V39 Models
    "TelemetryEvent",
    "TelemetryMetricSnapshot",
    "AnomalyIncident",
    "AnomalyCorrelationLink",
    "ResilienceState",
    "DegradedModeActivation",
    "RecoveryTransition",
    "OpsRiskSnapshot",
    "PredictiveIncidentSignal",
    "PatternRegressionCase",
    
    # RAG Models
    "KnowledgeDocument",
    "KnowledgeChunk",
    "KnowledgeSource",
    "KnowledgeIndexRun",
    "RetrievalTrace",
    "RetrievalFeedback",
]
