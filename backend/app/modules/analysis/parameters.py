"""
Single source of truth for the 11 parameters: key, display name and plain-language explanation.
The order here is the order shown to the user.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Parameter:
    key: str
    name: str
    explanation: str
    needs_text: bool = False  # not applicable when the logo has no text


PARAMETERS: tuple[Parameter, ...] = (
    Parameter("visual_simplicity", "Visual Simplicity", "How clean and uncluttered your logo is."),
    Parameter("legibility", "Legibility", "How easy the text in your logo is to read.", needs_text=True),
    Parameter("scalability", "Scalability", "How clear your logo stays when it is very small or very large."),
    Parameter("distinctiveness", "Distinctiveness", "How much your logo stands out from other logos."),
    Parameter(
        "brand_relevance",
        "Brand Relevance",
        "How well your logo fits the kind of business it seems to represent.",
    ),
    Parameter(
        "typography", "Typography", "How well the fonts suit the logo and work together.", needs_text=True
    ),
    Parameter("colors", "Colors", "How well the colors work together and in different settings."),
    Parameter("composition", "Composition", "How well the parts of your logo are arranged and balanced."),
    Parameter("memorability", "Memorability", "How easy your logo is to remember after a quick look."),
    Parameter(
        "versatility",
        "Versatility",
        "How well your logo works on different backgrounds, in one color, and on different products.",
    ),
    Parameter(
        "technical_quality",
        "Technical Quality",
        "How clean the logo is technically: sharp edges, no blur, proper alignment.",
    ),
)

PARAMETER_KEYS: tuple[str, ...] = tuple(p.key for p in PARAMETERS)