"""
"AI Generated" recommendation: one text-only AI call that writes an improved prompt.
Uses the existing analysis; the image is not analysed again.
"""

from app.modules.ai import AIProvider
from app.modules.analysis import LogoAnalysis
from app.modules.recommendations.ai_generated.prompts import build_prompt
from app.modules.recommendations.ai_generated.schemas import ImprovedPrompt
from app.modules.recommendations.shared import generate_validated, summarize, summary_text


async def generate_improved_prompt(analysis: LogoAnalysis, ai: AIProvider) -> ImprovedPrompt:
    prompt = build_prompt(summary_text(summarize(analysis)))
    return await generate_validated(ai, prompt, ImprovedPrompt)