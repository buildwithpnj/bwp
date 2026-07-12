class ProfileLoader:
    @classmethod
    def format_profile_for_prompt(cls, profile_dict: dict) -> str:
        """Formats the profile database dictionary into structured system instructions context."""
        if not profile_dict:
            return ""
            
        lines = [
            f"- Preferred Tone: {profile_dict.get('tone', 'professional')}",
            f"- Explanation Style: {profile_dict.get('explanation_style', 'detailed')}",
            f"- Target English Level: {profile_dict.get('target_english_level', 'Advanced')}",
            f"- Preferred Support Language: {profile_dict.get('preferred_language', 'English')}"
        ]
        
        weaknesses = profile_dict.get("weaknesses", [])
        if weaknesses:
            lines.append(f"- Known Weaknesses: {', '.join(weaknesses)}")
            
        goals = profile_dict.get("goals", [])
        if goals:
            lines.append(f"- Rewrite Goals: {', '.join(goals)}")
            
        return "\n".join(lines)
