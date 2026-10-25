MODULE: analysis              STATUS: FINALIZED (pending real-API test)
Purpose : Turn a prepared logo image into a validated, scored analysis (1 AI call).
Input   : await analyze_logo(image: PreparedImage, ai: AIProvider)
Output  : LogoAnalysis(is_logo=True, overall_score, parameters[11 in fixed order], similarity)
          | NotALogo(is_logo=False, message)
Errors  : AnalysisFailed 502 (AI output invalid twice); ai errors pass through unchanged
Depends : upload (PreparedImage), ai (AIProvider), core
Used by : api, logo_status (similarity), recommendations
Test    : pytest tests/analysis   |   python -m scripts.try_analysis path/to/logo.png

Rules
- AI output is never trusted: strict schema check; one retry if invalid.
- Scores 0-10 (out of range = invalid, never clamped); 1 decimal, rounded half up.
- Overall score = average of applicable scores, calculated by the backend from the rounded values.
- Logo with no text: typography + legibility = N/A (score null) and excluded from the average.
- Max 3 positives / 3 negatives per parameter (extras dropped); each point 1-300 chars.