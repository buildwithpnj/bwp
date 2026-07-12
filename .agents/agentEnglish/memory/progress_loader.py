class ProgressLoader:
    @classmethod
    def format_progress_for_prompt(cls, progress_dict: dict) -> str:
        """Formats the learning statistics dictionary into structured feedback parameters."""
        if not progress_dict:
            return ""
            
        lines = [
            f"- Streak Count: {progress_dict.get('streak', 0)} consecutive corrections",
            f"- Total Accepted Corrections: {progress_dict.get('corrections_accepted', 0)}"
        ]
        
        mastered = progress_dict.get("mastered_patterns", [])
        if mastered:
            lines.append(f"- Mastered Skills: {', '.join(mastered)}")
            
        weaks = progress_dict.get("weak_categories", [])
        if weaks:
            lines.append(f"- Active Focus Categories: {', '.join(weaks)}")
            
        return "\n".join(lines)
