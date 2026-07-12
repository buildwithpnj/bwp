from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_profile_memory_service import UserProfileMemoryService
from app.services.learning_progress_service import LearningProgressService

# Correct absolute importing from .agents paths
import sys
import os

agents_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.agents"))
if agents_path not in sys.path:
    sys.path.insert(0, agents_path)

from agentEnglish.memory.profile_loader import ProfileLoader
from agentEnglish.memory.progress_loader import ProgressLoader

class AgentMemoryContextBuilder:
    @classmethod
    async def build_context_block(cls, db: AsyncSession, user_id: str) -> str:
        """Gathers profile settings and learning progress statistics, formatting a clean prompt block."""
        profile = await UserProfileMemoryService.get_or_create_profile(db, user_id)
        progress = await LearningProgressService.get_or_create_progress(db, user_id)
        
        # Serialize database object attributes to dictionary safely
        profile_dict = {
            "tone": profile.tone,
            "explanation_style": profile.explanation_style,
            "target_english_level": profile.target_english_level,
            "preferred_language": profile.preferred_language,
            "weaknesses": profile.weaknesses or [],
            "goals": profile.goals or []
        }
        
        progress_dict = {
            "streak": progress.streak,
            "corrections_accepted": progress.corrections_accepted,
            "mastered_patterns": progress.mastered_patterns or [],
            "weak_categories": progress.weak_categories or []
        }
        
        profile_block = ProfileLoader.format_profile_for_prompt(profile_dict)
        progress_block = ProgressLoader.format_progress_for_prompt(progress_dict)
        
        blocks = []
        if profile_block:
            blocks.append("=== USER PERSONALIZATION PROFILE ===\n" + profile_block)
        if progress_block:
            blocks.append("=== USER LEARNING PROGRESS ===\n" + progress_block)
            
        return "\n\n".join(blocks)
