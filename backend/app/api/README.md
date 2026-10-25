MODULE: api                   STATUS: FINALIZED (pending local test)
Purpose : HTTP layer. Connects requests to the finished modules; no business logic here.
Routes  : GET  /api/health
          POST /api/logo/analyze                            raw image body -> {is_logo, analysis, logo_status}
          POST /api/logo/recommendations/ai-prompt          {analysis} -> {prompt}
          POST /api/logo/recommendations/designer           {analysis} -> {recommendations, overall}
          POST /api/logo/recommendations/designer/download  {analysis, recommendations} -> .txt
Errors  : every error -> {"error": {"code", "message"}}   (register_error_handlers)
Limits  : upload stream stopped at MAX_UPLOAD_MB (nothing written to disk);
          RATE_LIMIT_ANALYZE per IP, separate counter per AI endpoint; download not limited
Depends : core, upload, analysis, logo_status, recommendations, ai
Used by : main.py  (include api_router, register_error_handlers, set app.state.ai + app.state.rate_limiter)
Test    : pytest tests/api