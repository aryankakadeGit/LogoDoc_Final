"""
Public API of recommendations.ai_generated.
"""

from app.modules.recommendations.ai_generated.schemas import ImprovedPrompt
from app.modules.recommendations.ai_generated.service import generate_improved_prompt

__all__ = ["generate_improved_prompt", "ImprovedPrompt"]