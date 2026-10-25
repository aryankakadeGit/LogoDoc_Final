MODULES: recommendations/{shared, ai_generated, manual_design}   STATUS: FINALIZED (pending real-API test)
Input   : LogoAnalysis (from the analyze step; when it comes back from the browser it is
          re-validated and its overall score / names are recalculated by the backend)
Depends : analysis, ai, core
Used by : api (recommendation routes)
Test    : pytest tests/recommendations  |  python -m scripts.try_recommendations <file>.analysis.json

shared
  summarize(analysis) -> AnalysisSummary   improve = score < 7 (weakest first; if none, 2 lowest
                                           as fine-tune), keep = score >= 8; N/A skipped. No AI.
  summary_text(summary) -> str             compact <logo_analysis> block for prompts
  generate_validated(ai, prompt, schema)   1 text-only AI call + 1 retry if invalid
  RecommendationFailed 502

ai_generated   ("AI Generated" logos)
  await generate_improved_prompt(analysis, ai) -> ImprovedPrompt(prompt)      1 text-only AI call

manual_design  ("Manually Designed" logos)
  await generate_designer_recommendations(analysis, ai) -> DesignerRecommendations
        recommendations[]: key, name, score, problem, why_it_matters, suggestion, preserve
        overall[]: 3-5 points                                                1 text-only AI call
  build_txt(analysis, recommendations) -> str  (.txt download, FILENAME)     no AI call