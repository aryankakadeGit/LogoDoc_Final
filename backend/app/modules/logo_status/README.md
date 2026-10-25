MODULE: logo_status           STATUS: FINALIZED (pending local test)
Purpose : Turn the AI's similarity findings into a user-facing logo status (no extra AI call).
Input   : get_logo_status(analysis: LogoAnalysis)
Output  : LogoStatus(status, title, message, recognized_brand, notes, sources_checked, disclaimer)
Status  : no_significant_similarity | generic_elements | potentially_similar | matches_known_logo
Depends : analysis (LogoAnalysis, Similarity)
Used by : api (analyze route)
Test    : pytest tests/logo_status

Rules
- Never claims a logo is "original" or "infringing"; always shows sources checked + disclaimer.
- Brand name shown only for strong/exact matches; generic elements are explained as normal.
- Phase 2: add a Cloud Vision checker in service.py and merge its findings into LogoStatus.